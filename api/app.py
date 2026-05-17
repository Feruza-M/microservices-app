import os
from contextlib import contextmanager
from flask import Flask, jsonify, request
import psycopg2
from psycopg2.extras import RealDictCursor

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://appuser:apppass@localhost:5432/appdb")
app = Flask(__name__)

@contextmanager
def get_conn():
    conn = psycopg2.connect(DATABASE_URL)
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()

@app.get('/health')
def health():
    return {'status': 'ok'}

@app.get('/api/tasks')
def list_tasks():
    with get_conn() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute('SELECT id, title, status, created_at, processed_at FROM tasks ORDER BY id DESC')
            rows = cur.fetchall()
            return jsonify(rows)

@app.post('/api/tasks')
def create_task():
    data = request.get_json(force=True, silent=True) or {}
    title = (data.get('title') or '').strip()
    if not title:
        return jsonify({'error': 'title is required'}), 400
    with get_conn() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                'INSERT INTO tasks (title, status) VALUES (%s, %s) RETURNING id, title, status, created_at, processed_at',
                (title, 'new')
            )
            row = cur.fetchone()
            return jsonify(row), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
