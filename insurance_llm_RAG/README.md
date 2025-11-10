# Insurance LLM RAG Workspace

## Overview
This project houses a Retrieval Augmented Generation (RAG) assistant tailored for employees of **Insurellm**, an insurance technology company. The goal is to provide accurate, low-cost question answering over internal knowledge such as product briefs, employee bios, contracts, and company context. The primary workflow lives in `rag_insurance_company.py`, which:
- Loads markdown documents from the `knowledge-base/` hierarchy
- Splits documents into overlapping chunks
- Builds a persistent vector store with Chroma and OpenAI embeddings (or a drop-in Hugging Face alternative)
- Visualizes embeddings in 2D/3D using t-SNE and Plotly
- Exposes a conversational interface backed by LangChain’s `ConversationalRetrievalChain`
- Optionally runs a Gradio chat UI for quick prototyping

A second script, `diy_rag_system.py`, contains earlier experiments and can be used as a sandbox for custom variations.

## Repository Structure
- `rag_insurance_company.py` – main runnable script for the Insurellm RAG assistant, including visualization and Gradio chat.
- `diy_rag_system.py` – reference implementation used during development.
- `knowledge-base/` – curated markdown documents grouped into `company/`, `contracts/`, `employees/`, and `products/`.
- `vector_db/` – Chroma persistence directory created after embeddings are generated (can be deleted to rebuild from scratch).
- `.env` *(not committed)* – expected to store `OPENAI_API_KEY`.

## Prerequisites
- Python 3.10+ (project currently uses Python 3.12 via a virtual environment).
- OpenAI API access if you plan to use `OpenAIEmbeddings` and `ChatOpenAI`.
- Optional: ability to run Gradio in a local browser.

### Recommended Python Packages
Install dependencies inside your preferred virtual environment:
```bash
pip install langchain==0.3.25 langchain-community==0.3.25 \
    langchain-openai==0.3.22 langchain-chroma==0.1.4 chromadb==0.5.23 \
    openai==2.6.0 python-dotenv gradio plotly numpy scikit-learn
```

> **Note:** `langchain-chroma==0.1.4` stays aligned with the LangChain 0.3.x series. Newer `langchain-chroma>=1.0` requires the 1.x LangChain stack, so upgrade intentionally if you move to the latest APIs.

### Environment Variables
Create a `.env` file at the project root (already git-ignored) with:
```
OPENAI_API_KEY=sk-your-key
```
You can override other settings (model names, persistence path, etc.) directly in the script if desired.

## Running the RAG Assistant
1. **Activate your environment** and ensure dependencies are installed.
2. **Prepare the knowledge base** by adding or editing markdown files under `knowledge-base/`. Each subfolder name is used as `doc_type` metadata.
3. **Launch the script**:
   ```bash
   python rag_insurance_company.py
   ```
   The script will:
   - Load and chunk the documents
   - Persist embeddings into `vector_db/`
   - Print summary stats to the console
   - Render 2D and 3D embedding visualizations (these appear in your default browser using Plotly)
   - Open a Gradio chat window (`inbrowser=True`) so you can interact with the assistant

4. **Chat with the agent** via the Gradio UI or by calling the `conversation_chain.invoke` method directly within the script.

## Customization Tips
- **Embeddings**: To use a local model instead of OpenAI, replace `OpenAIEmbeddings()` with `HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")` and remove OpenAI dependencies.
- **LLM Backend**: Swap `ChatOpenAI` with a local Ollama model by uncommenting the provided example and adjusting base URL/API key.
- **Retriever Depth**: The final section of the script shows how to increase `k` (number of chunks retrieved) to improve answer completeness.
- **Visualization**: The t-SNE reduction uses a fixed `random_state` for reproducibility; tune parameters (`perplexity`, `learning_rate`) for different datasets.

## Maintenance
- **Rebuilding the Vector Store**: Delete the `vector_db/` folder to force a clean rebuild with the next run.
- **Version Control**: The repo intentionally omits notebooks and local artifacts (e.g., `.env`, `vector_db/`). Add new files carefully or adjust `.gitignore` if you need to commit additional assets.
- **Dependency Conflicts**: Because LangChain’s ecosystem moves quickly, re-pin requirements if you upgrade major packages. Always check for pip resolver warnings after installs.

## Getting Help
If you encounter issues:
- Verify your OpenAI key is valid and that the `MODEL` constant matches an available deployment.
- Ensure Plotly and Gradio are allowed to open browser windows on your machine.
- Inspect console logs for callback outputs (`StdOutCallbackHandler`) to trace retrieval failures.

Happy experimenting with your insurance RAG assistant!

