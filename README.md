# 🚀 AI-Powered Text-to-SQL API

This project converts natural language queries into SQL using LLMs and executes them on a database.

## 🔥 Features
- Natural language → SQL conversion
- FastAPI backend
- SQL Server integration
- Real-time query execution
- Safe query handling

## 🏗️ Architecture
User → FastAPI → LLM → SQL Server → Results

## 🛠️ Tech Stack
- Python
- FastAPI
- OpenAI / LLM
- SQL Server

## ▶️ How to Run

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
