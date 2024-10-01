from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_mysqldb import MySQL
import spacy

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  # Replace with your MySQL username
app.config['MYSQL_PASSWORD'] = ''  # Replace with your MySQL password
app.config['MYSQL_DB'] = 'taskmanager'

mysql = MySQL(app)

#Adding a task 
@app.route("/add_task", methods=["POST"])
def add_task():
    data = request.get_json()
    task = data.get("task", "")
    priority = data.get("priority", "Medium")
    due_date = data.get("dueDate", None)
    importance = data.get("importance", 3)
    completed = False

    cur = mysql.connection.cursor()
    query = "INSERT INTO tasks (task, priority, due_date, importance, completed) VALUES (%s, %s, %s, %s, %s)"
    cur.execute(query, (task, priority, due_date, importance, completed))
    mysql.connection.commit()
    cur.close()

    return jsonify({"message": "Task added successfully"})

#Fetching tasks 
@app.route("/get_tasks", methods=["GET"])
def get_tasks():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tasks")
    tasks = cur.fetchall()
    cur.close()

    task_list = []
    for task in tasks:
        task_list.append({
            "id": task[0],
            "task": task[1],
            "priority": task[2],
            "dueDate": str(task[3]),
            "importance": task[4],
            "completed": task[5]
        })

    return jsonify(task_list)

#Updating Task Completion
@app.route("/update_task/<int:id>", methods=["PUT"])
def update_task(id):
    data = request.get_json()
    completed = data.get("completed", False)

    cur = mysql.connection.cursor()
    query = "UPDATE tasks SET completed = %s WHERE id = %s"
    cur.execute(query, (completed, id))
    mysql.connection.commit()
    cur.close()

    return jsonify({"message": "Task updated successfully"})



@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    text = data.get("task", "")
    doc = nlp(text)

    # Extract named entities, parts of speech, and other useful info
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    tokens = [(token.text, token.pos_) for token in doc]

    return jsonify({
        "entities": entities,
        "tokens": tokens
    })

if __name__ == "__main__":
    app.run(debug=True)
