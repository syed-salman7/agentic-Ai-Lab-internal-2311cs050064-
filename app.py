import os
import re
import streamlit as st
from openai import OpenAI

from database import create_database, get_schema, execute_query


# ---------------------------------------------------------
# CREATE DATABASE
# ---------------------------------------------------------

create_database()


# ---------------------------------------------------------
# OPENAI CLIENT
# ---------------------------------------------------------

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error("OPENAI_API_KEY is not set.")
    st.stop()

client = OpenAI(api_key=api_key)


# ---------------------------------------------------------
# PAGE
# ---------------------------------------------------------

st.title("Text-to-SQL Question Answering System")

st.write(
    "Ask a question about the student database using normal English."
)


# ---------------------------------------------------------
# RETRIEVAL
# ---------------------------------------------------------

def retrieve_schema():

    schema = get_schema()

    return schema


# ---------------------------------------------------------
# SQL GENERATION
# ---------------------------------------------------------

def generate_sql(question, schema):

    prompt = f"""
You are a Text-to-SQL assistant.

Convert the user's natural language question into
a valid SQLite SQL query.

DATABASE SCHEMA:
{schema}

USER QUESTION:
{question}

Rules:
1. Generate only SQL.
2. Do not use Markdown.
3. Use only tables and columns present in the schema.
4. Generate SELECT queries only.
5. Do not INSERT, UPDATE, DELETE, DROP or ALTER.
"""

    response = client.responses.create(
        model="gpt-5-mini",
        input=prompt
    )

    sql = response.output_text.strip()

    # Remove markdown code fences if the model returns them
    sql = re.sub(r"```sql", "", sql, flags=re.IGNORECASE)
    sql = re.sub(r"```", "", sql)

    return sql.strip()


# ---------------------------------------------------------
# SECURITY CHECK
# ---------------------------------------------------------

def validate_sql(sql):

    sql_upper = sql.upper().strip()

    dangerous_commands = [
        "INSERT",
        "UPDATE",
        "DELETE",
        "DROP",
        "ALTER",
        "CREATE",
        "REPLACE",
        "ATTACH",
        "DETACH"
    ]

    if not sql_upper.startswith("SELECT"):
        return False

    for command in dangerous_commands:
        if re.search(r"\b" + command + r"\b", sql_upper):
            return False

    return True


# ---------------------------------------------------------
# USER INPUT
# ---------------------------------------------------------

question = st.text_input(
    "Enter your question:",
    placeholder="Example: Which students scored more than 80?"
)


# ---------------------------------------------------------
# END-TO-END WORKFLOW
# ---------------------------------------------------------

if st.button("Run Query"):

    if not question:
        st.warning("Please enter a question.")
        st.stop()

    # Step 1: Retrieve schema
    schema = retrieve_schema()

    st.subheader("Retrieved Database Schema")

    st.code(schema, language="sql")


    # Step 2: Generate SQL
    with st.spinner("Generating SQL..."):

        sql = generate_sql(question, schema)

    st.subheader("Generated SQL")

    st.code(sql, language="sql")


    # Step 3: Validate SQL
    if not validate_sql(sql):

        st.error("Unsafe SQL query rejected.")

        st.stop()


    # Step 4: Execute SQL
    try:

        columns, rows = execute_query(sql)

        # Step 5: Display result
        st.subheader("Query Result")

        if rows:

            data = [dict(zip(columns, row)) for row in rows]

            st.dataframe(data)

        else:

            st.info("No records found.")

    except Exception as e:

        st.error(f"SQL execution error: {e}")