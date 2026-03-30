from flask import Flask, render_template, request, jsonify
import os
import pg8000.native
from urllib.parse import urlparse
import ssl

app = Flask(__name__, template_folder="../templates")

def get_conn():
    url = os.environ.get("DATABASE_URL")
    p = urlparse(url)
    ctx = ssl.create_default_context()

    return pg8000.native.Connection(
        user=p.username,
        password=p.password,
        host=p.hostname,
        port=p.port or 5432,
        database=p.path.lstrip("/"),
        ssl_context=ctx,
    )

def init_db():
    conn = get_conn()
    conn.run("""
        CREATE TABLE IF NOT EXISTS calc_logs (
            id SERIAL PRIMARY KEY,
            num1 FLOAT,
            num2 FLOAT,
            result FLOAT,
            created_at TIMESTAMPTZ DEFAULT NOW()
        )
    """)
    conn.close()

def insert_log(a, b, result):
    conn = get_conn()
    conn.run(
        "INSERT INTO calc_logs (num1, num2, result) VALUES (:a, :b, :r)",
        a=a, b=b, r=result
    )
    conn.close()

def get_logs():
    conn = get_conn()
    rows = conn.run("""
        SELECT id, created_at, num1, num2, result
        FROM calc_logs
        ORDER BY id DESC
        LIMIT 10
    """)
    conn.close()
    return rows

@app.route("/api/calculator", methods=["GET", "POST"])
def home():
    result = None
    error = None

    init_db()

    if request.method == "POST":
        num1 = request.form.get("num1")
        num2 = request.form.get("num2")

        try:
            result = int(num1) + int(num2)

            insert_log(int(num1), int(num2), result)

        except:
            error = "숫자를 올바르게 입력해주세요."

    return render_template("calculator.html", result=result, error=error)

@app.route("/api/logs")
def logs_api():
    rows = get_logs()

    return jsonify([
        {
            "id": r[0],
            "ts": r[1].isoformat(),
            "a": r[2],
            "b": r[3],
            "result": r[4]
        }
        for r in rows
    ])


app = app
