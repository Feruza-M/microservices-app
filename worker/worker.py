import os
import time
import psycopg2

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://appuser:apppass@localhost:5432/appdb")
POLL_INTERVAL = int(os.getenv("POLL_INTERVAL", "5"))

def process_once():
    conn = psycopg2.connect(DATABASE_URL)
    try:
        conn.autocommit = False
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id FROM tasks
                WHERE status = 'new'
                ORDER BY id ASC
                LIMIT 1
                FOR UPDATE SKIP LOCKED
            """)
            row = cur.fetchone()
            if not row:
                conn.commit()
                return False
            task_id = row[0]
            cur.execute(
                "UPDATE tasks SET status = 'done', processed_at = NOW() WHERE id = %s",
                (task_id,)
            )
        conn.commit()
        return True
    finally:
        conn.close()

if __name__ == '__main__':
    while True:
        try:
            found = process_once()
            if not found:
                time.sleep(POLL_INTERVAL)
        except Exception:
            time.sleep(POLL_INTERVAL)
