import os
from typing import List, IO, Tuple
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import (
    GoogleGenerativeAIEmbeddings,
    ChatGoogleGenerativeAI,
)
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain.schema import Document
from dotenv import load_dotenv
import google.generativeai as genai
import streamlit as st  # For Streamlit functions used in this file

# Load environment variables and configure Google API
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)


def get_pdf_text(pdf_docs: List[IO[bytes]]) -> str:
    """
    Extract text content from a list of PDF files.

    Args:
        pdf_docs (List[IO[bytes]]): List of uploaded PDF files from Streamlit's file uploader.

    Returns:
        str: A single string containing concatenated text extracted from all PDFs.
    """
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    return text


def get_text_chunks(text: str) -> List[str]:
    """
    Split text into manageable chunks for processing.

    Args:
        text (str): The raw text to split.

    Returns:
        List[str]: A list of text chunks, each as a string.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=10000, chunk_overlap=1000
    )
    chunks = text_splitter.split_text(text)
    return chunks


def get_vector_store(text_chunks: List[str]) -> None:
    """
    Create and save a FAISS vector store from text chunks.

    Args:
        text_chunks (List[str]): List of text chunks.

    Returns:
        None
    """
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    documents = [Document(page_content=chunk) for chunk in text_chunks]
    vector_store = FAISS.from_documents(documents, embedding=embeddings)
    vector_store.save_local("faiss_index")


def get_conversational_chain() -> Tuple[ChatGoogleGenerativeAI, PromptTemplate]:
    """
    Initialize the conversational AI model and prompt template.

    Returns:
        Tuple[ChatGoogleGenerativeAI, PromptTemplate]: A tuple containing the AI model instance and the prompt template.
    """
    prompt_template = """
    As a professional assistant, provide a detailed and formally written answer to the question using the provided context. Ensure that the response is professionally formatted and avoids informal language.

    Context:
    {context}

    Question:
    {question}

    Answer:
    """

    model = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.3)
    prompt = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )
    return model, prompt


def self_assess(question: str) -> str:
    """
    Determine whether the AI can answer the question directly or needs to search the documents.

    Args:
        question (str): The user's question.

    Returns:
        str: The AI's response, which is either the direct answer or 'NEED_RETRIEVAL' if document search is needed.
    """
    assessment_prompt = [
        {
            "role": "system",
            "content": "You are an expert assistant who provides professionally formatted and formally written answers.",
        },
        {
            "role": "user",
            "content": f"""
            If you are confident in answering the following question based on your existing knowledge,
            please provide a detailed and formally written answer directly. If you are not confident or require additional information to answer accurately,
            please respond with 'NEED_RETRIEVAL'.

            Question: {question}
            """,
        },
    ]
    model = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.3)
    response = model.invoke(assessment_prompt)
    return response.content.strip()  # Removed .upper()


def process_docs_for_query(docs: List[Document], question: str) -> str:
    """
    Process documents to generate an answer to the user's question.

    Args:
        docs (List[Document]): Relevant documents retrieved from the vector store.
        question (str): The user's question.

    Returns:
        str: The AI-generated answer based on the documents.
    """
    if not docs:
        return "I apologize, but I couldn't find any relevant information in the provided documents to answer your question."

    context = "\n\n".join([doc.page_content for doc in docs])
    model, prompt = get_conversational_chain()
    formatted_prompt = prompt.format(context=context, question=question)
    response = model.invoke(formatted_prompt)
    return response.content


def user_input(user_question: str) -> None:
    """
    Handle user input, decide whether to search documents or answer directly, and display the response.

    Args:
        user_question (str): The question entered by the user.

    Returns:
        None
    """
    assessment = self_assess(user_question)

    # Display source notification
    if assessment.strip().upper() == "NEED_RETRIEVAL":
        st.info("🔍 Searching through your uploaded documents for the answer...")
        need_retrieval = True
    else:
        need_retrieval = False
        st.info("💡 Answering based on AI's built-in knowledge...")

    try:
        if need_retrieval:
            embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
            vector_store = FAISS.load_local(
                "faiss_index", embeddings, allow_dangerous_deserialization=True
            )
            docs = vector_store.similarity_search(user_question)
            response = process_docs_for_query(docs, user_question)
        else:
            response = assessment

        # Display the response
        st.markdown("### Answer")
        st.markdown(f"{response}")

    except Exception:
        st.error(
            "⚠️ An error occurred while processing your question. Please make sure you've uploaded and processed your documents first."
        )
