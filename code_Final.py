# LangChain + SQL + LLM setup
from langchain_community.utilities import SQLDatabase
from langchain_core.prompts import PromptTemplate
# from langchain_experimental.sql.base import create_sql_query_chain
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# LLM options
# from langchain.llms import OpenAI
from langchain_ollama import OllamaLLM
# from langchain_google_genai import ChatGoogleGenerativeAI


# *Connect to MYSQL* 
host = "localhost"
port = 3306
username = "root"
database_schema = "text_to_sql"

#since our password contain special character
from urllib.parse import quote_plus
password = quote_plus("Shreyash@6105")

mysql_uri = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database_schema}"

db = SQLDatabase.from_uri(mysql_uri, sample_rows_in_table_info=2)

#to check if our db is imported or not
# db = SQLDatabase.from_uri(mysql_uri, sample_rows_in_table_info=2)
# db.get_table_info()


#prompting llm first time
prompt = PromptTemplate.from_template("""
You are a MySQL expert.

Generate a syntactically correct MySQL SQL query for the given question.

CRITICAL RULES (MUST FOLLOW):
- Use ONLY table and column names EXACTLY as they appear in the schema
- Column names may contain SPACES — preserve them exactly
- ALWAYS wrap column names containing spaces in BACKTICKS (`column name`)
- Do NOT convert names to snake_case
- Generate READ-ONLY queries (SELECT only)
- Do NOT hallucinate tables or columns
- Do NOT add explanations or formatting
- Return ONLY the SQL query

Schema:
{schema}

Question:
{question}

SQL Query:
""")

#for schema
def get_schema(db):
    schema = db.get_table_info()
    return schema


llm = OllamaLLM(
    model="llama3",
    temperature=0
)


sql_chain = (
    RunnablePassthrough.assign(
        schema=lambda _: db.get_table_info()
    )
    | prompt
    | llm
    | StrOutputParser()
)


#trying with a test response
# response = sql_chain.invoke({"question":"What is the total 'Line Total' for Geiss Company"})
# print(response)
# db.run(response)


#writing prompt for llm second time to get our required format result
answer_prompt = PromptTemplate.from_template("""
You are a data assistant.

Given:
- The user's question
- The SQL query result

Generate a clear, concise, and professional natural language answer.

Rules:
- Use the wording of the question
- Clearly mention the value from the result
- Do NOT mention SQL or databases
- Keep the answer short and factual

Question:
{question}

SQL Result:
{result}

Final Answer:
""")


answer_chain = (
    answer_prompt
    | llm
    | StrOutputParser()
)


def ask_question(question: str):
    # Generate SQL
    sql_query = sql_chain.invoke({"question": question})

    # Execute SQL
    db_result = db.run(sql_query)

    # Extract value safely
    value = db_result[0][0] if db_result and db_result[0] else None

    # Generate final answer
    final_answer = answer_chain.invoke({
        "question": question,
        "result": value
    })

    return {
        "sql_query": sql_query,
        "raw_result": value,
        "final_answer": final_answer
    }


while True:
    user_question = input("\nAsk a question (or type 'exit'): ")

    if user_question.lower() == "exit":
        break

    response = ask_question(user_question)

    print("\n--- SQL QUERY ---")
    print(response["sql_query"])

    print("\n--- RESULT ---")
    print(response["raw_result"])

    print("\n--- FINAL ANSWER ---")
    print(response["final_answer"])
