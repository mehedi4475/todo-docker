import os
import socket
import psycopg2
from flask import Flask, request, jsonify, Response

app = Flask(__name__)

def get_db():
    return psycopg2.connect(
        host=os.environ["DB_HOST"],
        dbname=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
    )

def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            id SERIAL PRIMARY KEY,
            task TEXT NOT NULL,
            completed BOOLEAN DEFAULT FALSE
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

# --- API endpoints ---

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

# এই Pod ও Node-এর তথ্য জানায় (footer-এ দেখানোর জন্য)
@app.route("/whoami")
def whoami():
    return jsonify({
        "pod": socket.gethostname(),
        "node": os.environ.get("NODE_NAME", "unknown")
    })

@app.route("/todos", methods=["GET"])
def list_todos():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, task, completed FROM todos ORDER BY id")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([
        {"id": r[0], "task": r[1], "completed": r[2]} for r in rows
    ])

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
    return jsonify({"id": new_id, "task": task, "completed": False}), 201

# সম্পন্ন/অসম্পন্ন টগল করে (PUT)
@app.route("/todos/<int:todo_id>", methods=["PUT"])
def toggle_todo(todo_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "UPDATE todos SET completed = NOT completed WHERE id = %s RETURNING completed",
        (todo_id,)
    )
    result = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if result is None:
        return jsonify({"error": "not found"}), 404
    return jsonify({"id": todo_id, "completed": result[0]})

# todo মুছে ফেলে (DELETE)
@app.route("/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM todos WHERE id = %s", (todo_id,))
    deleted = cur.rowcount
    conn.commit()
    cur.close()
    conn.close()
    if deleted == 0:
        return jsonify({"error": "not found"}), 404
    return jsonify({"deleted": todo_id})

# --- HTML পেজ ---

@app.route("/")
def home():
    return Response(HTML_PAGE, mimetype="text/html")


HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Todo App</title>
  <style>
    body { font-family: system-ui, sans-serif; max-width: 600px; margin: 40px auto; padding: 0 16px; background: #f5f5f5; }
    h1 { color: #333; }
    .add-box { display: flex; gap: 8px; margin-bottom: 20px; }
    input[type=text] { flex: 1; padding: 10px; border: 1px solid #ccc; border-radius: 6px; font-size: 15px; }
    button { padding: 10px 16px; border: none; border-radius: 6px; background: #2563eb; color: white; cursor: pointer; font-size: 15px; }
    button:hover { background: #1d4ed8; }
    ul { list-style: none; padding: 0; }
    li { background: white; padding: 12px 14px; margin-bottom: 8px; border-radius: 6px; display: flex; align-items: center; justify-content: space-between; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
    li.done span.task { text-decoration: line-through; color: #999; }
    .actions button { padding: 6px 10px; font-size: 13px; margin-left: 6px; }
    .toggle { background: #16a34a; }
    .toggle:hover { background: #15803d; }
    .delete { background: #dc2626; }
    .delete:hover { background: #b91c1c; }
    footer { margin-top: 30px; padding: 12px; background: #1f2937; color: #d1d5db; border-radius: 6px; font-size: 13px; text-align: center; font-family: monospace; }
    footer .label { color: #9ca3af; }
    footer .val { color: #34d399; font-weight: bold; }
  </style>
</head>
<body>
  <h1>📝 Todo App</h1>
  <div class="add-box">
    <input type="text" id="taskInput" placeholder="Add a new task..." onkeydown="if(event.key==='Enter')addTodo()">
    <button onclick="addTodo()">Add</button>
  </div>
  <ul id="todoList"></ul>

  <footer>
    <div><span class="label">Served by Pod:</span> <span class="val" id="pod">...</span></div>
    <div><span class="label">Node:</span> <span class="val" id="node">...</span></div>
  </footer>

  <script>
    async function loadTodos() {
      const res = await fetch('/todos');
      const todos = await res.json();
      const list = document.getElementById('todoList');
      list.innerHTML = '';
      todos.forEach(t => {
        const li = document.createElement('li');
        if (t.completed) li.className = 'done';
        li.innerHTML = `
          <span class="task">${t.task}</span>
          <span class="actions">
            <button class="toggle" onclick="toggleTodo(${t.id})">${t.completed ? 'Undo' : 'Done'}</button>
            <button class="delete" onclick="deleteTodo(${t.id})">Delete</button>
          </span>`;
        list.appendChild(li);
      });
    }
    async function addTodo() {
      const input = document.getElementById('taskInput');
      if (!input.value.trim()) return;
      await fetch('/todos', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({task: input.value})
      });
      input.value = '';
      loadTodos();
    }
    async function toggleTodo(id) {
      await fetch('/todos/' + id, {method: 'PUT'});
      loadTodos();
    }
    async function deleteTodo(id) {
      await fetch('/todos/' + id, {method: 'DELETE'});
      loadTodos();
    }
    async function loadWhoami() {
      const res = await fetch('/whoami');
      const data = await res.json();
      document.getElementById('pod').textContent = data.pod;
      document.getElementById('node').textContent = data.node;
    }
    loadTodos();
    loadWhoami();
  </script>
</body>
</html>
"""


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)