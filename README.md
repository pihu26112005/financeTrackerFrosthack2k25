# Finance Tracker - AI-powered Financial Analysis

## Overview
This project is an AI-powered financial analysis system that processes and analyzes transaction data to provide insights and answer user queries. It integrates LangChain, Fetch.ai, and Pathway for efficient data processing and retrieval.

## Features
- Parses and extracts financial transactions from documents.
- Stores structured financial data for quick retrieval.
- Provides financial insights based on user queries.
- Implements advanced retrieval-augmented generation (RAG) techniques.
- Uses Fetch.ai and Pathway for efficient data processing.
- Supports visualization of financial data trends.

## Project Structure
```
├── aazold
│   ├── adaptive_rag.py
│   ├── app.yaml
│   ├── data
│   │   ├── x.txt
│   │   ├── y.txt
│   │   └── z.txt
│   └── rag-app
│       └── app.py
├── agent_fetchai.py
├── agents
│   ├── DocToGDrive.py
│   ├── DocumentParsingAgent2.py
│   ├── DocumentParsingAgent.py
│   ├── GetReleventTransactionByDate.py
│   ├── GetReleventTransaction.py
│   ├── GetUserQueryOutput.py
│   ├── IsContextNeeded.py
│   └── __pycache__
├── app.py
├── Cache
│   ├── 1-0-0
│   └── 1-0-1
├── credentials.json
├── data
│   └── finance_docs_extracted.csv
├── INFO
│   ├── data
│   ├── filtered_transactions.json
│   ├── output.json
│   ├── processed_output.json
│   ├── staticPlots
├── LanggraphApp.py
├── output_chunks
├── pathwayF
│   ├── baseModel.py
│   ├── langchainPathwayClient.py
│   ├── pathwayServer.py
│   ├── pdfToCSVByLLM.py
│   └── __pycache__
├── README.md
├── requirements.txt
└── staticVisualizationAgent.py
```

## Installation
1. Clone the repository:
   ```sh
   git clone <repository-url>
   cd financeTrackerFrosthack2k25
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Set up credentials (e.g., Fetch.ai API keys, database configurations) in `credentials.json`.

## Running the Application
### Step 1: Start the Backend
```sh
python app.py
```
### Step 2: Run Supporting Agents
Run the required agents in separate terminals:
```sh
python agents/GetUserQueryOutput.py
python agents/GetReleventTransaction.py
```
### Step 3: Query the System
Use the API to fetch transaction insights:
```sh
curl -X POST "http://localhost:8000/query" -H "Content-Type: application/json" -d '{"query": "What was my highest deposit in January 2025?"}'
```

## Relevant Resources
- [FetchAi with LangChain](https://fetch.ai/docs/examples/rag/langchain-rag)
- [Pathway with LangChain](https://pathway.com/blog/langchain-integration)
- [Pathway Adaptive RAG with LangGraph](https://github.com/pathwaycom/llm-app/blob/main/cookbooks/self-rag-agents/pathway_langgraph_agentic_rag.ipynb)
- [Pathway as a Vector Store in LangChain](https://python.langchain.com/docs/integrations/vectorstores/pathway/)
- [Pathway Unstructured to Structured SQL Queries](https://github.com/pathwaycom/llm-app/tree/main/examples/pipelines/unstructured_to_sql_on_the_fly)
- [Pathway INTERIIT Project](https://github.com/Stormbreakerr20/Pathway_InterIIT_13.0/tree/master/code/Rag_application)
- [Google Drive with Additional Files](https://drive.google.com/drive/folders/14cPcPF19g3LPGojMTRhoNCFTAx8sTV0a)

## Contributing
Feel free to open issues and submit pull requests for improvements.
