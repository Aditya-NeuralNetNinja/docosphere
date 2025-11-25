import os, tempfile, streamlit as st
from typing import List, IO, Tuple
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from docx import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document as LangchainDocument
from langchain_community.vectorstores import FAISS
from langchain_together.chat_models import ChatTogether
from langchain_together.embeddings import TogetherEmbeddings        # <-- NEW
from langchain.prompts import PromptTemplate

load_dotenv()

# ---------- Helpers ---------------------------------------------------------
def get_together_api_key() -> str:
    key = os.getenv("TOGETHER_API_KEY") or st.secrets.get("TOGETHER_API_KEY", None)
    if not key:
        raise EnvironmentError("TOGETHER_API_KEY not found in env or Streamlit secrets.")
    return key

# ---------- File-reading utilities -----------------------------------------
def get_pdf_text(pdf_docs: List[IO[bytes]]) -> str:
    txt = ""
    for pdf in pdf_docs:
        for page in PdfReader(pdf).pages:
            if (t := page.extract_text()):
                txt += t + "\n"
    return txt

def get_docx_text(docx_docs: List[IO[bytes]]) -> str:
    txt = ""
    for d in docx_docs:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
            tmp.write(d.getvalue()); tmp.flush()
        try:
            doc = Document(tmp.name)
            txt += "\n".join(p.text for p in doc.paragraphs) + "\n"
        finally:
            os.unlink(tmp.name)
    return txt

def get_text_chunks(text: str) -> List[str]:
    return RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200).split_text(text)

# ---------- Vector-store build & save --------------------------------------
def get_vector_store(text_chunks: List[str]) -> None:
    api_key = get_together_api_key()
    embeddings = TogetherEmbeddings(model="BAAI/bge-base-en-v1.5", api_key=api_key)
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")

# ---------- QA chain helpers ----------------------------------------------
def get_conversational_chain() -> Tuple[ChatTogether, PromptTemplate]:
    api_key = get_together_api_key()
    llm = ChatTogether(model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
                       temperature=0.3, api_key=api_key)
    prompt = PromptTemplate(
        template=(
            "As a professional assistant, provide a detailed and formally written "
            "answer to the question using the provided context.\n\nContext:\n{context}\n\n"
            "Question:\n{question}\n\nAnswer:"
        ),
        input_variables=["context", "question"]
    )
    return llm, prompt

def self_assess(question: str) -> str:
    api_key = get_together_api_key()
    llm = ChatTogether(model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
                       temperature=0.3, api_key=api_key)
    msgs = [
        {"role": "system", "content": "You are an expert assistant…"},
        {"role": "user",   "content": (
            "If you can confidently answer the following question from your own "
            "knowledge, do so; otherwise reply with 'NEED_RETRIEVAL'.\n\n"
            f"Question: {question}"
        )}
    ]
    return llm.invoke(msgs).content.strip()

def process_docs_for_query(docs: List[LangchainDocument], question: str) -> str:
    if not docs:
        return "Sorry, I couldn’t find relevant info in the documents."
    ctx = "\n\n".join(d.page_content for d in docs)
    llm, prompt = get_conversational_chain()
    return llm.invoke(prompt.format(context=ctx, question=question)).content

# ---------- Main user-query orchestrator -----------------------------------
def user_input(user_question: str) -> None:
    assessment = self_assess(user_question)
    need_retrieval = assessment.upper() == "NEED_RETRIEVAL"
    st.info("🔍 Searching documents…" if need_retrieval else "💡 Using model knowledge…")

    try:
        if need_retrieval:
            api_key = get_together_api_key()
            embeddings = TogetherEmbeddings(model="BAAI/bge-base-en-v1.5", api_key=api_key)
            vs = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
            docs = vs.similarity_search(user_question)
            answer = process_docs_for_query(docs, user_question)
        else:
            answer = assessment

        st.markdown("### Answer")
        st.markdown(answer)
    except Exception as e:
        st.error(f"⚠️ Error: {e}")