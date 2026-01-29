# Text-to-SQL Assistant Using LLM (LangChain + MySQL)

This project translates **natural language questions into SQL queries** and returns the results as **simple, easy-to-understand English responses**.  
The core objective is to explore how **Large Language Models (LLMs) can work directly with real databases** using LangChain, without building any web-based interface.

---

## Project Overview

This system performs the following steps:

1. Takes a user query written in natural language  
2. Converts it into a **valid MySQL SELECT query**  
3. Executes the query on an actual MySQL database  
4. Transforms the SQL output into a **human-readable response**

---

## Tools and Technologies

- Python  
- LangChain  
- Ollama (LLaMA 3 model)  
- MySQL  

---

## Project Structure

- `code_final.py` – Main application script  
- `README.md` – Project documentation  
- `requirements.txt` – Required dependencies  
- `Data_CSV/` – CSV files used to create database tables  

---

## Setup Requirements

Before running the project, make sure to:

- Create a database using **MySQL Workbench** or any SQL client  
- Create tables using the CSV files available in the `Data_CSV/` folder  
- Update and verify database connection credentials inside the code  

---

## Development Steps

### 1. Database Connection
- Connected Python to a MySQL database using LangChain’s `SQLDatabase`
- Worked with an actual database schema instead of dummy or hardcoded data
- Verified that all tables and columns were correctly detected

---

### 2. SQL Query Generation (LLM – Stage 1)
- Designed prompts to:
  - Enforce correct table and column usage
  - Handle column names that contain spaces
  - Minimize incorrect or hallucinated queries
- Used the LLaMA 3 model via Ollama to generate **read-only SQL queries**

---

### 3. SQL Query Execution
- Executed the generated SQL queries directly on the MySQL database
- Retrieved results safely and in a controlled manner

---

### 4. Natural Language Response Generation (LLM – Stage 2)
- Passed the SQL query results back to the LLM
- Generated concise and user-friendly answers
- Ensured that SQL syntax and internal database details are not exposed in the final response

---

### 5. Interactive Command-Line Interface
- Enables users to ask multiple questions in one session
- Displays:
  - The generated SQL query  
  - Raw database output  
  - Final natural language answer  
- Typing `exit` ends the program

---

## Example Workflow

**User Input:**  
“What is the total sales for Geiss Company?”

**System Output:**
- SQL query is automatically generated  
- Query is executed on the MySQL database  
- Final answer is returned in plain English  

---

## Key Learnings

- Grounding LLM responses using real database schemas
- Prompt engineering for safe and controlled SQL generation
- Chaining multiple LLM calls to improve response accuracy
- Practical use of LangChain for database-driven AI applications

---

## Author

**Pranjal Mahale**
