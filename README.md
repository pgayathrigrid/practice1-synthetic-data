# 🚀 Synthetic Data Generator using Gemini + Streamlit

## 📌 Overview
This project is a **Streamlit-based web application** that generates synthetic data from a given SQL schema using **Google Gemini (LLM)**.

Users can upload a `.sql` file containing table definitions, and the application automatically generates realistic sample data in structured format.

---

## 🎯 Features
- 📂 Upload SQL schema files (`.sql`, `.txt`)
- 🤖 Generate synthetic data using Gemini API
- 📊 Display generated data in table format
- ⚡ Simple and interactive UI with Streamlit
- 🌐 Deployed as a public web app

---

## 🛠️ Tech Stack
- Python  
- Streamlit  
- Google Gemini API (google-genai)  
- Pandas  

---

## 🖥️ Live Demo
https://practice1-synthetic-data.streamlit.app/ 

---

## 📂 Project Structure

practice1-synthetic-data/
│
├── app.py
├── requirements.txt
├── README.md


---

## ⚙️ How it Works
1. Upload a SQL schema file  
2. The app reads table structure (columns, types)  
3. A prompt is sent to Gemini LLM  
4. LLM generates synthetic data in JSON format  
5. Data is converted into a table and displayed  

---

## 🔐 Environment Variables
To run this project locally, set your API key:

```bash
export GEMINI_API_KEY="your_api_key_here"
