# Docosphere: Where Documents Come Alive

**Docosphere** is an intelligent Retrieval-Augmented Generation (RAG) system prototype designed to deliver precise and efficient responses by combining the intrinsic knowledge of a Large Language Model (LLM) with relevant external data. Its innovative self-assessing mechanism ensures retrieval is invoked only when necessary, optimizing resource utilization and enhancing user experience.

---

## Features

- **Self-Assessing LLMs**: Implements confidence evaluation to decide whether external document retrieval is needed.
- **Custom Retrieval Strategies**: Minimizes redundant database calls, reducing them by 40%, using LangChain and tailored prompt engineering.
- **Document Processing Pipeline**: Handles PDF and Word file processing with Recursive Character Text Splitter for context-preserving chunking.
- **Semantic Search**: Uses FAISS VectorDB integrated with Google Generative AI and Gemini 1.5 Pro embeddings.
- **Model Testing**: Benchmarked alternative LLMs and embeddings (Gemma, Llama, multilingual-e5-large with Pinecone VectorDB) for optimal results.
- **Streamlit UI**: Provides a user-friendly interface deployed on Hugging Face Spaces.

---

## How to Use

1. **Upload Documents**: Drag and drop one or more PDF or Word files using the uploader interface.
2. **Process Documents**: Click `Process Documents` to prepare the documents for semantic search.
3. **Ask Questions**: Enter your question in the chat input box.
4. **Get Answers**: Instantly receive responses based on the uploaded documents or the LLM's internal knowledge.

---

## Testing

Comprehensive testing of **Docosphere** was conducted using the [`FY 2023-24 Indian Economic Survey`](https://github.com/Aditya-NeuralNetNinja/docosphere/blob/main/FY%202023-24%20Indian%20Economic%20Survey.pdf) to validate its performance under real-world scenarios.

### Test Categories:

1. **Dynamic Questions**:
   - Require specific information from the uploaded PDF document.
   - Example: "How did the fiscal deficit of 23 states in FY24 compare to their budgeted amount?"

2. **Static Questions**:
   - Rely on general knowledge within the LLM's internal dataset.
   - Example: "Explain the concept of revenue deficit and fiscal deficit in the context of the Union Budget of India."

3. **Hybrid Questions**:
   - Answerable through either the LLM's intrinsic knowledge or the uploaded document, but was answered using LLM's intrinsic knowledge, to avoid unnecessary database calls.
   - Example: "What happened to India’s merchandise trade deficit in FY24?"

### Test Questions File

The full set of test questions can be found in the `tests` directory:

- **File**: [`tests/test_questions_fy2023-24_indian_economic_survey.md`](./tests/test_questions_fy2023-24_indian_economic_survey.md)
- Use these questions to validate the system's performance across different knowledge requirements.

---

## Architecture

### Key Components:

- **Self-Assessing LLMs**: Dynamically decide between internal knowledge and retrieval-based response.
- **Document Processing**: Ensures semantic integrity using the Recursive Character Text Splitter.
- **Semantic Search**: Powered by FAISS VectorDB and advanced embeddings.
- **LangChain Workflow Orchestration**: Streamlines query handling and response generation.

### Alternative Approaches Tested:

- Models: Gemma, Llama LLM families
- Embeddings: Multilingual-e5-large with Pinecone VectorDB.
- Findings: FAISS + Gemini 1.5 Pro provided superior performance.

---

## Installation

### Prerequisites:

- Python 3.9 or higher.

### Setup:

1. Clone the repository:
   ```python
   git clone https://github.com/your-repo-name/docosphere.git
   cd docosphere
   ```

2. Create and activate a virtual environment (optional but recommended):
```python
python3 -m venv env
source env/bin/activate  # For Linux/Mac
env\Scripts\activate     # For Windows
```

3. Install the required dependencies:
```python
pip install -r requirements.txt
```

4. Running the Application:
Start the application:
```python
streamlit run app.py
```

5. Open the URL displayed in the terminal (usually http://localhost:8501) to interact with the application.

## Deployment
The Docosphere prototype is deployed on Hugging Face Spaces using Streamlit for a user-friendly demonstration.

### Steps to Deploy on Hugging Face Spaces:
1. Set up a [`New Hugging Face Space`](https://huggingface.co/new-space) 
2. Choose Streamlit as the SDK.
3. Upload the necessary files:
```python
app.py
utils.py
requirements.txt
```

4. Run the application:
Your app will automatically build and start running on Hugging Face Spaces.

## Future Enhancements
1. File Format Support: Expand support to include additional formats like Excel, Powerpoint, CSV.
2. Advanced Analytics: Add retrieval usage analytics for better insights.
3. Improved Multilingual Support: Integrate more robust multilingual embeddings and vector databases.
4. Scalability: Optimize for handling larger datasets and concurrent users.
