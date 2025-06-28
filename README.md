# Sales Ai Agent: AI-Powered Sales & Email Automation

## Overview
aiagentSales is an AI-driven platform designed to automate and enhance sales email generation, customer query replies, and database-driven responses for companies. It leverages advanced LLMs (Gemini/OpenAI), Retrieval-Augmented Generation (RAG), and MongoDB to streamline outbound sales, customer support, and information retrieval workflows.

## Features
- **Sales Email Generation:** Three distinct AI sales agents (professional, engaging, concise) generate cold emails. The best email is selected and sent automatically.
- **OPEN AI SDK:** LLM integration with OPENAI SDK.
- **Automated Query Replies:** Uses RAG to answer customer queries by searching a knowledge base.
- **Database Query Handling:** Converts user requests into MongoDB queries, fetches results, and crafts human-readable responses.
- **Agent Handoffs:** Intelligent agent handoff system routes tasks between specialized agents (e.g., sales, query, database) for optimal workflow automation.
- **Guardrails:** Input guardrails for name and spam detection to ensure safe and relevant interactions.
- **Email Delivery:** Integrates with SendGrid for sending emails.

## Project Structure
```
    SalesAgent/
      app.py                # Main application entry point
      requirements.txt      # Python dependencies
      Agents/               # Sales and DB agent tools
      Guardrails/           # Input/spam guardrails
      Model/                # LLM model setup (Gemini)
      RagSearch/            # RAG utilities (ChromaDB)
      Tools/                # Email, MongoDB, and utility functions
```

## Setup Instructions
1. **Clone the repository**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Environment Variables:**
   - Create a `.env` file in `ai/SalesAgent/` with the following keys:
     - `GEMINI_API_KEY` (for Gemini LLM)
     - `OPENAI_API_KEY` (for traces )
     - `SENDGRID_API_KEY` (for email delivery)
   - Ensure MongoDB is running locally at `mongodb://localhost:27017/` and has a database `LPU` with a `courses` collection.
4. **Prepare ChromaDB:**
   - Place your PDF documents in `/docs/` and run `create_chroma_db.py` to build the knowledge base.

## Usage
- **Run the main application:**
  ```bash
  python app.py
  ```
- The system will process either sales or query emails based on the input type.
- Modify `email_generator()` in `app.py` to test different scenarios.

## Key Components
- **Agents:**
  - `agenticTools.py`: Three sales personas as tools.
  - `DBtool.py`: MongoDB query generator and response formatter.
- **Guardrails:**
  - `inputGuardrail.py`: Checks for personal names in messages.
  - `spamGuardrail.py`: Detects spam or irrelevant queries.
- **RAG Search:**
  - `create_chroma_db.py`: Builds ChromaDB from PDFs.
  - `query_chroma_db.py`: Retrieves relevant info for queries.
- **Tools:**
  - `projectFunctions.py`: Email sending and error logging.
  - `MongoData.py`: Executes MongoDB commands.
- **Model:**
  - `geminiModel.py`: Configures Gemini LLM for all agents.

## Notes
- Update sender/recipient emails in `projectFunctions.py` as needed.
- The `.env` and `venv` directories are ignored by git.

