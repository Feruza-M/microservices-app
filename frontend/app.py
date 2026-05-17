from flask import Flask, render_template_string

app = Flask(__name__)

HTML = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Tasks App</title>
  <style>
    body { font-family: Arial, sans-serif; max-width: 760px; margin: 40px auto; padding: 0 16px; }
    h1 { margin-bottom: 8px; }
    form { display: flex; gap: 8px; margin: 20px 0; }
    input { flex: 1; padding: 10px; }
    button { padding: 10px 16px; cursor: pointer; }
    li { margin: 10px 0; padding: 12px; border: 1px solid #ddd; border-radius: 8px; list-style: none; }
    .muted { color: #666; }
    .done { color: green; }
    .new { color: #b26b00; }
  </style>
</head>
<body>
  <h1>Tasks App</h1>
  <p class="muted">Frontend -> API -> Postgres, worker processes tasks asynchronously.</p>
  <form id="task-form">
    <input id="title" type="text" placeholder="Enter task title" required>
    <button type="submit">Add</button>
  </form>
  <ul id="tasks"></ul>
  <script>
    async function loadTasks() {
      const res = await fetch('/api/tasks');
      const data = await res.json();
      const list = document.getElementById('tasks');
      list.innerHTML = data.map(t => `
        <li>
          <strong>${t.title}</strong><br>
          <span class="${t.status}">status: ${t.status}</span><br>
          <span class="muted">created: ${t.created_at}</span>
        </li>
      `).join('');
    }

    document.getElementById('task-form').addEventListener('submit', async (e) => {
      e.preventDefault();
      const input = document.getElementById('title');
      const title = input.value.trim();
      if (!title) return;
      await fetch('/api/tasks', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title })
      });
      input.value = '';
      await loadTasks();
    });

    loadTasks();
    setInterval(loadTasks, 3000);
  </script>
</body>
</html>
"""

@app.get('/')
def index():
    return render_template_string(HTML)

@app.get('/health')
def health():
    return {'status': 'ok'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
