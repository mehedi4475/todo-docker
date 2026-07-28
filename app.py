import os
import psycopg2
from flask import Flask, request, jsonify

app = Flask(__name__)

def get_db():
    return psycopg2.connect(
        host=os.environ["DB_HOST"],
        dbname=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
    )

# অ্যাপ চালু হলে টেবিল বানিয়ে নেয়
def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            id SERIAL PRIMARY KEY,
            task TEXT NOT NULL
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

@app.route("/")
def home():
    return jsonify({"message": "Hello from auto-deploy! Version 4"})

@app.route("/health")
def health():
    return jsonify({"status": "ok"})
    
@app.route("/todos", methods=["GET"])
def list_todos():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, task FROM todos ORDER BY id")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([{"id": r[0], "task": r[1]} for r in rows])

@app.route("/todos", methods=["POST"])
def add_todo():
    task = request.json["task"]
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO todos (task) VALUES (%s) RETURNING id", (task,))
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"id": new_id, "task": task}), 201

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)