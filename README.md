# Agentic AI Research Assistant

An AI-powered research assistant built using **Python, FastAPI, LangChain, Groq, and Keenable Search**. It uses an AI agent to search the web, retrieve webpage content, and generate relevant, context-aware responses.

## Features

- **AI Agent:** Uses LangChain's agent framework.
- **Web Search:** Searches the internet using Keenable Search.
- **Web Fetching:** Retrieves webpage content for research.
- **LLM Integration:** Uses Groq-powered language models.
- **FastAPI:** Provides an API interface.
- **Streaming:** Supports incremental response generation.

## Tech Stack

- Python
- FastAPI
- LangChain
- LangServe
- Groq
- Keenable Search & Fetch
- Python-dotenv

## Project Structure

```text
project/
│
├── chatBot.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

## Installation

**1. Clone the repository**

```bash
git clone <your-repository-url>
cd <repository-name>
```

**2. Create a virtual environment**

```bash
python -m venv env
```

**3. Activate the environment (Windows)**

```bash
env\Scripts\activate
```

**4. Install dependencies**

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the project root and add your API credentials:

```env
GROQ_API_KEY=your_groq_api_key
KEENABLE_API_KEY=your_keenable_api_key
```

Use the environment variable names required by your installed Keenable SDK configuration.

## Run the Application

Start the FastAPI server:

```bash
uvicorn chatBot:app --reload
```

Replace `chatBot` with your Python filename if it is different.

## API Endpoints

| Endpoint | Description |
|---|---|
| `/docs` | FastAPI Swagger documentation |
| `/agent/invoke` | Invoke the AI agent |
| `/agent/stream` | Stream agent responses |
| `/agent/playground/` | Interactive LangServe playground |

Base URL:

```text
http://127.0.0.1:8000
```

## Learning Objectives

This project explores Agentic AI, LLM integration, tool calling, web research automation, and building AI-powered applications with FastAPI.

## Author

**Mohammed Aazam Mansuri**
