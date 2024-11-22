import streamlit as st
from utils import (
    get_pdf_text,
    get_docx_text,
    get_text_chunks,
    get_vector_store,
    user_input,
)
from typing import List, IO

def main() -> None:
    """
    Main function to run the Streamlit app.

    Returns:
        None
    """
    # Configure the page
    st.set_page_config(
        page_title="Docosphere",
        page_icon="📄",
        layout="wide"
    )

    # Main header with emoji and subtitle
    st.title("📄 Docosphere")
    st.markdown("*Where Documents Come Alive ...*")

    # Create two columns for better layout
    col1, col2 = st.columns([2, 1])

    with col2:
        st.markdown("### 📁 Document Upload")
        uploaded_files: List[IO[bytes]] = st.file_uploader(
            "Upload your documents (PDFs or Word files)",
            accept_multiple_files=True,
            type=["pdf", "docx"],
            help="Select one or more PDF or Word files to analyze"
        )

        if st.button("🚀 Process Documents"):
            if not uploaded_files:
                st.warning("📋 Please upload at least one file.")
                return

            with st.spinner("🔄 Processing your documents..."):
                raw_text = ""
                pdf_docs = [file for file in uploaded_files if file.name.endswith(".pdf")]
                docx_docs = [file for file in uploaded_files if file.name.endswith(".docx")]

                if pdf_docs:
                    raw_text += get_pdf_text(pdf_docs)
                if docx_docs:
                    raw_text += get_docx_text(docx_docs)

                if raw_text.strip():
                    text_chunks: List[str] = get_text_chunks(raw_text)
                    get_vector_store(text_chunks)
                    st.success(
                        "✅ Documents processed successfully! You can now ask questions about your content."
                    )
                else:
                    st.warning("⚠️ No content could be extracted from the uploaded files.")

        # Add usage instructions
        with st.expander("ℹ️ How to use"):
            st.markdown(
                """
                - Upload one or more PDF or Word files using the uploader above.
                - Click 'Process Documents' to analyze the content.
                - Type your question in the chat input.
                - Get instant answers based on your documents or AI knowledge.
                """
            )

    with col1:
        st.markdown("### 💬 Ask Your Question")
        user_question: str = st.text_input(
            "",
            placeholder="Type your question here...",
            help="Ask anything about your uploaded documents or general knowledge"
        )

        if user_question:
            user_input(user_question)

if __name__ == "__main__":
    main()
