# Docosphere

*Where Documents Come Alive*

**Docosphere** is an intelligent Retrieval-Augmented Generation (RAG) system prototype designed to deliver precise and efficient responses by combining the intrinsic knowledge of a Large Language Model (LLM) with relevant external data. Its innovative self-assessing mechanism ensures retrieval is invoked only when necessary, optimizing resource utilization and enhancing user experience.

---

## Live Demo

Webapp hosted on Hugging Face Spaces: [*Live Demo*](https://huggingface.co/spaces/adi-123/docosphere)

![Webapp](https://github.com/Aditya-NeuralNetNinja/docosphere/blob/main/webapp.png)

---

## How to Use

1. **Upload Documents**: Drag and drop one or more PDF or Word files using the uploader interface.
2. **Process Documents**: Click *Process Documents* to prepare the documents for semantic search.
3. **Ask Questions**: Enter your question in the chat input box.
4. **Get Answers**: Instantly receive responses based on the uploaded documents or the LLM's internal knowledge.

---

## Architecture

### Key Components

- **Self-Assessing LLMs**: Implements confidence evaluation to decide whether external document retrieval is needed.
- **Custom Retrieval Strategies**: Minimizes redundant database calls, reducing them by 40%, using LangChain and tailored prompt engineering.
- **Document Processing Pipeline**: Handles PDF and Word file processing with Recursive Character Text Splitter for context-preserving chunking.
- **Semantic Search**: Uses FAISS VectorDB integrated with Google Generative AI embeddings for efficient information retrieval.
- **Best-in-Class Model**: Incorporates Gemini 1.5 Pro, which provided the highest accuracy and relevance during extensive benchmarking.
- **Model Testing**: Benchmarked alternative LLMs (Gemma, Llama family) and embeddings (multilingual-e5-large with Pinecone VectorDB) for comparative analysis.
- **Streamlit UI**: Provides a user-friendly interface deployed on Hugging Face Spaces.

  
### Alternative Approaches Tested

- **Models**: Gemma, Llama LLM families
- **Embeddings**: Multilingual-e5-large with Pinecone VectorDB
- **Findings**: FAISS + Gemini 1.5 Pro provided superior performance.

---

## Installation

### Prerequisites

- Python 3.9 or higher.

### Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Aditya-NeuralNetNinja/docosphere.git
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

4. Set up environment variable:
   
```python
export GOOGLE_API_KEY="your_api_key"
```

5. Running the Application:
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
4. Set up Secret (Google API Key) on Settings page of space.
5. Run the application:
Your app will automatically build and start running on Hugging Face Spaces.

## Future Enhancements
1. File Format Support: Expand support to include additional formats like Excel, Powerpoint, CSV.
2. Advanced Analytics: Add retrieval usage analytics for better insights.
3. Improved Multilingual Support: Integrate more robust multilingual embeddings and vector databases.
4. Scalability: Optimize for handling larger datasets and concurrent users.
