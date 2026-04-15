import streamlit as st
import pandas as pd
from google.genai import Client
import json
from pandasql import sqldf
import matplotlib.pyplot as plt
import seaborn as sns
from langfuse import Langfuse

# -------------------- LANGFUSE -------------------- #
langfuse = Langfuse(
    public_key=st.secrets["LANGFUSE_PUBLIC_KEY"],
    secret_key=st.secrets["LANGFUSE_SECRET_KEY"],
    host=st.secrets["LANGFUSE_BASE_URL"]
)

# ✅ SAFE LOG FUNCTION (FIXED)
def log_to_langfuse(name, input_data, output_data):
    try:
        langfuse.log(
            name=name,
            input=input_data,
            output=output_data
        )
    except:
        pass


# ---------------- API KEY ---------------- #
api_key = st.secrets["GEMINI_API_KEY"]

if not api_key:
    st.error("🚨 GEMINI_API_KEY not set")
    st.stop()

client = Client(api_key=api_key)

st.set_page_config(page_title="Synthetic Data Generator", layout="wide")

# ---------------- SIDEBAR ---------------- #
menu = st.sidebar.selectbox("Navigation", ["Data Generation", "Talk to your data"])


# ================= DATA GENERATION ================= #

if menu == "Data Generation":

    st.title("Synthetic Data Generator 🚀")

    uploaded_file = st.file_uploader("Upload SQL file", type=["sql", "txt"])
    user_prompt = st.text_area("Additional Instructions (optional)")
    num_rows = st.slider("Number of rows", 1, 100, 5)

    if uploaded_file:
        content = uploaded_file.read().decode()

        st.subheader("Uploaded Schema:")
        st.code(content)

        if st.button("Generate Data"):

            prompt = f"""
            Generate synthetic data for this SQL schema:

            {content}

            Instructions:
            {user_prompt}

            Rules:
            - Generate {num_rows} rows
            - Respect column data types
            - Return ONLY valid JSON (no markdown)
            """

            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=prompt
            )

            try:
                clean_text = response.text.strip()

                if clean_text.startswith("```"):
                    clean_text = clean_text.replace("```json", "").replace("```", "").strip()

                data = json.loads(clean_text)
                df = pd.DataFrame(data)

                st.success("✅ Data generated successfully!")
                st.dataframe(df)

                st.session_state["data"] = df

                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button("Download CSV", csv, "synthetic_data.csv", "text/csv")

            except:
                st.error("⚠️ Failed to parse AI response")
                st.write(response.text)

    # -------- MODIFY DATA -------- #
    if "data" in st.session_state:

        st.subheader("Modify Generated Data")

        modify_prompt = st.text_input("Enter modification instruction")

        if st.button("Apply Changes"):

            df = st.session_state["data"]

            prompt = f"""
            Modify dataset:

            Data:
            {df.to_json(orient='records')}

            Instruction:
            {modify_prompt}

            Return ONLY valid JSON.
            """

            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=prompt
            )

            try:
                clean_text = response.text.strip()

                if clean_text.startswith("```"):
                    clean_text = clean_text.replace("```json", "").replace("```", "").strip()

                new_data = json.loads(clean_text)
                new_df = pd.DataFrame(new_data)

                st.success("✅ Data updated!")
                st.dataframe(new_df)

                st.session_state["data"] = new_df

            except:
                st.error("Modification failed")
                st.write(response.text)


# ================= TALK TO YOUR DATA ================= #

elif menu == "Talk to your data":

    st.title("💬 Chat with Your Data")

    if "data" not in st.session_state:
        st.warning("⚠️ Please generate data first")
    else:
        df = st.session_state["data"]

        st.subheader("Your Data:")
        st.dataframe(df)

        if "messages" not in st.session_state:
            st.session_state.messages = []

        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])

        user_input = st.chat_input("Ask something about your data...")

        if user_input:

            # -------- GUARDRAILS -------- #
            blocked_keywords = ["ignore", "bypass", "hack", "api key", "password"]
            off_topic_keywords = ["movie", "song", "weather", "cricket", "politics"]

            if any(word in user_input.lower() for word in blocked_keywords):
                log_to_langfuse("blocked_query", user_input, "Blocked unsafe query")
                st.error("🚫 Unsafe query detected!")
                st.stop()

            if any(word in user_input.lower() for word in off_topic_keywords):
                log_to_langfuse("off_topic_query", user_input, "Blocked off-topic query")
                st.warning("⚠️ Ask questions related to your dataset only.")
                st.stop()

            # -------- SAVE USER MESSAGE -------- #
            st.session_state.messages.append({"role": "user", "content": user_input})
            st.chat_message("user").write(user_input)

            # -------- NL → SQL -------- #
            schema = ", ".join(df.columns)

            prompt = f"""
            You are a SQL assistant.

            Table name: data_table
            Columns: {schema}

            Convert question into SQL.

            Rules:
            - Return ONLY SQL
            - No explanation

            Question: {user_input}
            """

            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=prompt
            )

            sql_query = response.text.strip()

            if sql_query.startswith("```"):
                sql_query = sql_query.replace("```sql", "").replace("```", "").strip()

            log_to_langfuse("sql_generation", user_input, sql_query)

            try:
                result = sqldf(sql_query, {"data_table": df})

                log_to_langfuse("sql_execution", sql_query, result.to_string())

                assistant_msg = st.chat_message("assistant")

                assistant_msg.code(sql_query, language="sql")

                if result.empty:
                    assistant_msg.warning("⚠️ No results found")
                else:
                    assistant_msg.dataframe(result)

                # -------- VISUALIZATION -------- #
                if any(word in user_input.lower() for word in ["plot", "chart", "graph", "bar"]):

                    if result.shape[1] >= 2:
                        x_col = result.columns[0]
                        y_col = result.columns[1]

                        if pd.api.types.is_numeric_dtype(result[y_col]):
                            fig, ax = plt.subplots()
                            sns.barplot(x=result[x_col], y=result[y_col], ax=ax)
                            plt.xticks(rotation=45)
                            assistant_msg.pyplot(fig)
                        else:
                            assistant_msg.warning("Y-axis must be numeric")
                    else:
                        assistant_msg.warning("Not enough data")

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"{sql_query}\n\nResult:\n{result.to_string(index=False)}"
                })

            except Exception as e:
                log_to_langfuse("error", user_input, str(e))
                st.error("⚠️ SQL execution failed")
                st.write(str(e))