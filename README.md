# Finance Tracker - FrostHack 2025

This repository contains a financial transaction analysis system that processes, parses, and analyzes transaction data using AI agents. It integrates multiple components, including document parsing, retrieval-augmented generation (RAG), and visualization.

## 📂 Project Structure

```
├── aazold
│   ├── adaptive_rag.py  # RAG-based processing
│   ├── app.yaml         # App configuration
│   ├── data            # Sample data
│   └── rag-app
│       └── app.py      # RAG application
├── agent_fetchai.py     # Main agent controller
├── agents
│   ├── DocToGDrive.py  # Upload documents to Google Drive
│   ├── DocumentParsingAgent.py  # Parses documents
│   ├── GetReleventTransaction.py  # Extracts relevant transactions
│   ├── GetUserQueryOutput.py  # Generates response from transaction data
│   ├── IsContextNeeded.py  # Checks if context is required
├── app.py               # Entry point for the API
├── Cache                # Stores cached results
├── data                 # Contains transaction datasets
├── INFO                 # Processed financial documents and reports
├── LanggraphApp.py      # LangChain-based application
├── output_chunks        # Chunked transaction data for processing
├── pathwayF             # Pathway AI integration
├── staticVisualizationAgent.py # Generates static plots
├── README.md            # Project documentation
├── requirements.txt     # Dependencies list
```

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-repo/financeTrackerFrosthack2k25.git
   cd financeTrackerFrosthack2k25
   ```

2. **Create a virtual environment** (Optional but recommended)
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 🏃 Running the Application

1. **Start the API**
   ```bash
   uvicorn app:app --reload
   ```
   This will start the FastAPI server on `http://127.0.0.1:8000`.

2. **Run the AI Agents**
   ```bash
   python agent_fetchai.py
   ```

3. **Using the RAG-based Query System**
   ```bash
   python aazold/rag-app/app.py
   ```

## 📊 Features

- Extracts transactions from PDFs
- Uses Retrieval-Augmented Generation (RAG) for intelligent query responses
- Visualizes financial trends with static plots
- Supports LangChain and Pathway AI for advanced document processing

## 🛠️ Configuration
- Place financial documents in `INFO/data/`
- Update `credentials.json` for authentication (if required)

## 📞 Support
For issues or questions, feel free to open an issue or contact the project maintainers.

Happy coding! 🚀


- https://fetch.ai/docs/examples/rag/langchain-rag --> FetchAi with Langchain
- https://pathway.com/blog/langchain-integration --> pathway with langchain 
- https://github.com/pathwaycom/llm-app/blob/main/cookbooks/self-rag-agents/pathway_langgraph_agentic_rag.ipynb --> pathway adaptic rag with langgraph 
- https://python.langchain.com/docs/integrations/vectorstores/pathway/ --> pathway as vector store in langchain 
- https://github.com/pathwaycom/llm-app/tree/main/examples/pipelines/unstructured_to_sql_on_the_fly --> pathway unstructured to structure query sql 
- https://github.com/Stormbreakerr20/Pathway_InterIIT_13.0/tree/master/code/Rag_application --> pathway INTERIIT

- https://drive.google.com/drive/folders/14cPcPF19g3LPGojMTRhoNCFTAx8sTV0a --> google drive link 
