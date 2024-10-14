import pandas as pd
import google.generativeai as genai

# Configure Google Generative AI with API Key
GOOGLE_API_KEY="AIzaSyBePwurGkm7AINWqWK-MkZrnwT31QFLNtc"
genai.configure(api_key=GOOGLE_API_KEY)

# Load the CSV file into a pandas DataFrame
df = pd.read_csv(r'F:\Project\End-End T2SQL\CountRecords.csv')

admin_prompt = [
"""
You are an expert in using Python and pandas for querying data from a CSV file.
The CSV file contains data with the following columns:

CountRecords: Count ID | LOT ID | In/Out | Timestamp | Machine ID | CDB | BMS | Maker | Badmarks total | Good chips

Objective:
Our primary objective is to count the number of microchips on a tray. The Count ID represents the tray number, and LOT ID is the specific ID of the tray. The In/Out column indicates whether the tray is being put into the machine ("in") or taken out ("out"). The Machine ID links to the corresponding Machine. The Timestamp column records the date and time when the tray with a specific LOT ID is recorded. The Badmarks total column counts the number of bad marks on the microchips, CDB represents some other data, and Good chips lists the chips that are good.

Examples:
Question: "How many entries of records are present?"
Python Command: result = df.shape[0]

Question: "When was the maximum bad marks counted?"
Python Command: result = df.loc[df['Badmarks total'].idxmax(), ['Timestamp', 'Badmarks total']]

Instructions:
Generate Python code using pandas to retrieve data from the DataFrame. Ensure accuracy when creating the query.
"""
]

# Function to generate response from Google Gemini
def get_gemini_response(question, admin_prompt):
    try:
        model = genai.GenerativeModel('gemini-pro')
        message = admin_prompt[0] + "\n" + question
        response = model.generate_content(message)
        return response.text
    except Exception as e:
        print(f"Error: {e}")
        return "Error: Unable to generate response."

# Function to read and execute the generated pandas code
def read_excel_query(query_code, df):
    try:
        # Execute the dynamically generated query code (Python)
        exec(query_code)
        return locals().get("result", "No result found")  # Get the 'result' variable from the executed code
    except Exception as e:
        return f"Error executing query: {e}"

# Main loop to ask questions and get responses
while True:
    question = input("Ask me anything: ")
    if question == "exit":
        break
    
    # Get response from LLM (should generate pandas code now)
    gemini_response = get_gemini_response(question, admin_prompt)
    
    if gemini_response.startswith("result ="):  # Assume result assignment for a valid query
        query_code = gemini_response.strip()
        print("Executing code:\n", query_code)
        query_response = read_excel_query(query_code, df)
        print(query_response)
    else:
        print(gemini_response)
