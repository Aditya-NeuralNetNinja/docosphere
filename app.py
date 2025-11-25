import streamlit as st
from typing import List, IO

# Import utilities you finalised
from utils import (
    get_pdf_text,
    get_docx_text,
    get_text_chunks,
    get_vector_store,
    user_input,
)

# ---------------------------------------------------------------------------#
#  Main Streamlit application
# ---------------------------------------------------------------------------#
def main() -> None:
    # ----- Page configuration ------------------------------------------------
    st.set_page_config(
        page_title="Docosphere",
        page_icon="📄",
        layout="wide"
    )

    st.title("📄 Docosphere")
    st.markdown("*Where Documents Come Alive …*")

    # Two-column layout: Q&A on left, file upload on right
    col_left, col_right = st.columns([2, 1])

    # --------------------- Right column – document upload -------------------
    with col_right:
        st.markdown("### 📁 Document Upload")
        uploaded_files: List[IO[bytes]] = st.file_uploader(
            "Upload PDF or Word files",
            accept_multiple_files=True,
            type=["pdf", "docx"],
            help="You can select multiple files at once."
        )

        if st.button("🚀 Process Documents"):
            if not uploaded_files:
                st.warning("📋 Please upload at least one file first.")
                return

            with st.spinner("🔄 Extracting text & creating vector index…"):
                combined_text = ""

                pdfs  = [f for f in uploaded_files if f.name.lower().endswith(".pdf")]
                docs  = [f for f in uploaded_files if f.name.lower().endswith(".docx")]

                if pdfs:
                    combined_text += get_pdf_text(pdfs)
                if docs:
                    combined_text += get_docx_text(docs)

                if combined_text.strip():
                    chunks = get_text_chunks(combined_text)
                    get_vector_store(chunks)
                    st.success("✅ Documents processed! Ask away in the left panel.")
                else:
                    st.warning("⚠️ No readable text found in the uploaded files.")

        with st.expander("ℹ️ How to use"):
            st.markdown(
                """
                1. Upload one or more **PDF** or **Word** documents.\n
                2. Click **Process Documents** to build the knowledge index.\n
                3. Ask natural-language questions in the input box (left column).\n
                4. The assistant will either answer from its own model knowledge or
                   retrieve context from your documents when needed.
                """
            )

    # ---------------------- Left column – chat interface --------------------
    with col_left:
        st.markdown("### 💬 Ask Your Question")
        question: str = st.text_input(
            "",
            placeholder="Type a question about your documents or general topics…"
        )

        if question:
            user_input(question)

# Entry-point guard
if __name__ == "__main__":
    main()