import streamlit as st
import pandas as pd
from google.genai import Client
import json
import os

# API KEY
client = Client(api_key=os.getenv("GEMINI_API_KEY"))

st.set_page_config(page_title="Synthetic Data Generator", layout="wide")

# Sidebar
menu = st.sidebar.selectbox("Navigation", ["Data Generation", "Talk to your data"])

if menu == "Data Generation":

    st.title("Synthetic Data Generator 🚀")

    uploaded_file = st.file_uploader("Upload SQL file", type=["sql", "txt"])

    # User inputs
    user_prompt = st.text_area("Additional Instructions (optional)")
    num_rows = st.slider("Number of rows", 1, 100, 5)

    if uploaded_file:
        content = uploaded_file.read().decode()

        st.subheader("Uploaded Schema:")
        st.code(content)

        # Generate Data
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
                model="gemini-2.0-flash",
                contents=prompt
            )

            try:
                clean_text = response.text.strip()

                if clean_text.startswith("```"):
                    clean_text = clean_text.replace("```json", "").replace("```", "").strip()

                data = json.loads(clean_text)
                df = pd.DataFrame(data)

                st.success("✅ Data generated successfully!")

                st.subheader("Generated Data:")
                st.dataframe(df)

                # Save in session
                st.session_state["data"] = df

                # Download CSV
                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button("Download CSV", csv, "synthetic_data.csv", "text/csv")

            except Exception as e:
                st.error("⚠️ Failed to parse AI response")
                st.write(response.text)


    if "data" in st.session_state:

        st.subheader("Modify Generated Data")

        modify_prompt = st.text_input("Enter modification instruction")

        if st.button("Apply Changes"):

            df = st.session_state["data"]

            prompt = f"""
            Modify the following dataset based on the instruction:

            Data:
            {df.to_json(orient='records')}

            Instruction:
            {modify_prompt}

            Return ONLY valid JSON.
            """

            response = client.models.generate_content(
                model="gemini-2.0-flash",
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


elif menu == "Talk to your data":

    st.title("Talk to Your Data 💬")

    if "data" not in st.session_state:
        st.warning("⚠️ Please generate data first in Data Generation tab")
    else:
        df = st.session_state["data"]

        st.subheader("Your Data:")
        st.dataframe(df)

        query = st.text_input("Ask something about your data")

        if st.button("Ask"):

            prompt = f"""
            Answer the question based on this dataset:

            Data:
            {df.to_json(orient='records')}

            Question:
            {query}
            """

            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt
            )

            st.subheader("Answer:")
            st.write(response.text)