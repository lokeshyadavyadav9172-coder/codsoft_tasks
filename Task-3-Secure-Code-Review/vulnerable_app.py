from flask import Flask, request
import sqlite3
import subprocess
import os

app = Flask(__name__)

# Vulnerability 1: Hardcoded secret
SECRET_KEY = "super-secret-demo-key-123"

# Vulnerability 2: Hardcoded database credentials
DB_USER = "admin"
DB_PASSWORD = "admin123"


def get_db():
    return sqlite3.connect("users.db")


@app.route("/")
def home():
    return """
    <h1>Demo User Portal</h1>
    <p>Security Code Review Application</p>
    <a href="/login">Login</a>
    """


# Vulnerability 3: SQL Injection
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        connection = get_db()
        cursor = connection.cursor()

        query = (
            "SELECT * FROM users "
            "WHERE username = '" + username +
            "' AND password = '" + password + "'"
        )

        cursor.execute(query)

        user = cursor.fetchone()

        connection.close()

        if user:
            return "Login successful!"

        return "Invalid username or password."

    return """
    <h2>Login</h2>

    <form method="POST">

        <input name="username"
               placeholder="Username">

        <br><br>

        <input name="password"
               type="password"
               placeholder="Password">

        <br><br>

        <button type="submit">
            Login
        </button>

    </form>
    """


# Vulnerability 4: Command injection
@app.route("/ping")
def ping():

    host = request.args.get("host", "localhost")

    result = subprocess.check_output(
        "ping -n 1 " + host,
        shell=True
    )

    return result.decode(errors="replace")


# Vulnerability 5: Debug mode enabled
@app.route("/debug-info")
def debug_info():

    return {
        "environment": os.environ.get("ENVIRONMENT", "development"),
        "secret_key": SECRET_KEY,
        "database_user": DB_USER
    }


if __name__ == "__main__":

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )