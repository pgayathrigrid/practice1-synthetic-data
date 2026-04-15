# 🚀 Synthetic Data Generator + Talk to Your Data using Gemini, Streamlit and Langfuse

## 📌 Overview

This project is a Streamlit-based web application that uses Google Gemini to:

- Generate synthetic data from a SQL schema
- Modify generated datasets using natural language
- Query datasets in plain English
- Convert natural language questions into SQL
- Execute SQL on the generated data
- Visualize query results with charts
- Track observability using Langfuse

Users can upload a `.sql` or `.txt` schema file, generate realistic synthetic data, and then interact with that data through a chatbot-like interface.

---

## 🎯 Features

### Data Generation

- 📂 Upload SQL schema files (`.sql`, `.txt`)
- 🤖 Generate synthetic data using Google Gemini
- 🔢 Choose number of rows to generate
- 📊 Display generated data in a table
- ⬇️ Download generated data as CSV

### Data Modification

- ✏️ Modify generated data using natural language instructions
- 🔄 Update and regenerate the dataset dynamically

### Talk to Your Data

- 💬 Ask questions about the dataset in plain English
- 🔁 Convert natural language questions into SQL automatically
- 🧠 Execute SQL using `pandasql`
- 📋 Display SQL query and query result

### Visualization

- 📈 Generate charts automatically for graph-related questions
- 📊 Supports bar charts for departments, salaries, counts, etc.

### Guardrails

- 🚫 Blocks unsafe queries such as API key, password, hack attempts
- ⚠️ Restricts off-topic questions unrelated to the uploaded dataset

### Observability

- 🔍 Integrated with Langfuse for observability
- 📝 Tracks:
  - User questions
  - Generated SQL queries
  - SQL execution results
  - Errors and blocked queries

---

## 🛠️ Tech Stack

- Python
- Streamlit
- Google Gemini API (`google-genai`)
- Pandas
- PandasQL
- Matplotlib
- Seaborn
- Langfuse

---

## 📂 Project Structure

```text
practice1-synthetic-data/
│
├── app.py
├── sample.sql
├── requirements.txt
├── README.md
├── .gitignore
```

---

## ⚙️ How It Works

1. Upload a SQL schema file
2. The app reads the table structure
3. Google Gemini generates realistic synthetic data
4. The data is displayed and stored in session state
5. Users can modify the data using natural language
6. Users can ask questions about the data
7. Gemini converts the question into SQL
8. The SQL is executed using `pandasql`
9. Results are displayed in table and chart form
10. Langfuse records traces for observability

---

## 💡 Example SQL Schema

```sql
CREATE TABLE employees (
    employee_id INT,
    first_name TEXT,
    last_name TEXT,
    age INT,
    gender TEXT,
    department TEXT,
    designation TEXT,
    salary INT,
    city TEXT,
    state TEXT,
    joining_date DATE,
    experience_years INT,
    email TEXT,
    phone_number TEXT,
    performance_rating FLOAT
);
```

---

## 💬 Example Questions

- Show all employees in the Sales department
- What is the average salary by department?
- Show the highest paid employee
- Plot salary by department
- Show employees with more than 5 years of experience
- Count employees in each city

---

## 🔐 Environment Variables

Create and configure the following environment variables before running locally:

```bash
export GEMINI_API_KEY="your_gemini_api_key"

export LANGFUSE_PUBLIC_KEY="your_langfuse_public_key"
export LANGFUSE_SECRET_KEY="your_langfuse_secret_key"
export LANGFUSE_BASE_URL="https://cloud.langfuse.com"
```

---

## ▶️ Run Locally

```bash
git clone https://github.com/pgayathrigrid/practice1-synthetic-data.git
cd practice1-synthetic-data

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt

streamlit run app.py
```

---

## 🖥️ Live Demo

[Open the Live App](https://practice1-synthetic-data.streamlit.app/)

---

## 🚀 Future Improvements

- Support line, pie, and scatter charts
- Export query results as CSV
- Support multiple tables and joins
- Add chat history persistence
- Improve SQL generation accuracy
- Add deployment monitoring dashboard
