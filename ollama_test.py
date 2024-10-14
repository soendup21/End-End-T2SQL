import mysql.connector
import requests

# Database connection setup
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="SONYpassword",
    database="SonyDatabaseTest"
)

ollama_url = "http://localhost:11434/api/generate"

def get_ollama_response(question, admin_prompt):
    try:
        prompt = admin_prompt[0] + "\n" + question
        data = {
            "model": "tinyllama",
            "prompt": prompt, 
            "stream": False
        }
        headers = {
            "Content-Type": "application/json"
        }

        response = requests.post(ollama_url, json=data, headers=headers)

        if response.status_code == 200:
            return response.json()["response"]
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        print(f"Error: {e}")
        return "Error: Unable to generate response."

def read_sql_query(query, db):
    cursor = db.cursor()
    cursor.execute(query)
    results = []
    for x in cursor:
        results.append(x)
    return results

admin_prompt = [
    """
    You are a SQL expert, specializing in assisting users with generating SQL commands based on their questions. The SQL database consists of three tables with the following case-sensitive columns:

    business: Business_id | Business_name
    countrecords: count_id (Tray Number) | Lot_id (Tray ID) | Direction (In/Out) | Timestamp | Machine_ID | Substrate | TTL | badmark (Bad Marks) | ASSY_input (Initial Chip Count) | NG (Not Good Chips) | Good (Good Chips)
    station: Machine_ID | Machine_name | Business_id

    Objective:

    Our primary objective is to count the number of microchips on a tray. The count_id represents the tray number, and Lot_id is the specific ID of the tray. The Direction column indicates whether the tray is being put into the machine ("in") or taken out ("out"). The Machine_ID in countrecords links to the corresponding Machine_name in the station table. The Timestamp column records the date and time when the tray with a specific Lot_id is recorded. The badmark column counts the number of bad marks on the microchips, Assy_input represents the number of chips on the tray before it is put into the machine, NG lists the chips that are not good, and Good lists the chips that are good.

    Examples:

    Question: "How many entries of records are present in countrecords?"
    SQL Command: SELECT COUNT(*) FROM countrecords;

    Question: "What's the machine name with ID 5?"
    SQL Command: SELECT Machine_name FROM station WHERE Machine_ID = 5;

    Question: when was maximum bad marks counted?
    SQL Command: SELECT Timestamp, badmark 
    FROM countrecords 
    ORDER BY badmark DESC 
    LIMIT 1;

    Question: how many lots did I count yesterday?   
    SQL Command: SELECT COUNT(DISTINCT Lot_id) 
    FROM countrecords 
    WHERE DATE(Timestamp) = CURDATE() - INTERVAL 1 DAY;

    Instructions:

    Relevant Questions: If the user’s question directly relates to the database, respond with the appropriate SQL command prefixed by ####.
    Irrelevant Questions: If the user’s question is not related to the database, Introduce yourself as AI to chat with database created by KMUTNB. Use the same language style as the user's query.
    Case Sensitivity: Remember that table and column names are strictly case-sensitive. Ensure accuracy when creating the SQL query. make sure when you create query, it is executable in SQL.
    Special Handling: If the user asks about "good," use the Good column in countrecords. If they ask about "not good," use the NG column in countrecords.
    """
]

while True:
    question = input("Ask me anything: ")
    if question.lower() == "exit":
        break

    ollama_response = get_ollama_response(question, admin_prompt)

    if ollama_response.startswith("####"):
        query = ollama_response[4:].strip()
        print("Sending query: " + query)
        query_response = read_sql_query(query, mydb)
        for row in query_response:
            print(row)
    else:
        print(ollama_response)
