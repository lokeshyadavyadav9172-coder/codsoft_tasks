from flask import Flask, request
import sqlite3
import os
import re
import socket
from werkzeug.security import check_password_hash

app = Flask(__name__)

# Secure practice: load the application secret from an environment variable.
# A development fallback is provided only so the demo can run locally.
app.config["SECRET_KEY"] = os.environ.get(
    "APP_SECRET_KEY",
    "development-only-secret"
)


def get_db():
    """Create a SQLite database connection."""
    connection = sqlite3.connect("users.db")
    connection.row_factory = sqlite3.Row
    return connection


def validate_username(username):
    """Allow only safe username characters and a reasonable length."""

    if not username:
        return False

    return bool(
        re.fullmatch(
            r"[A-Za-z0-9_.-]{1,50}",
            username
        )
    )


def validate_host(host):
    """Validate a hostname or IP-style value before DNS resolution."""

    if not host:
        return False

    return bool(
        re.fullmatch(
            r"[A-Za-z0-9.-]{1,253}",
            host
        )
    )


@app.route("/")
def home():
    """Display the application home page."""

    return """
    <h1>Secure Demo User Portal</h1>
    <p>Secure Coding Review Application</p>

    <a href="/login">Login</a>
    <br><br>

    <a href="/ping?host=localhost">
        Test Host Resolution
    </a>
    """


@app.route("/login", methods=["GET", "POST"])
def login():
    """Authenticate a user using validated input and password hashing."""

    if request.method == "POST":

        username = request.form.get(
            "username",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        )

        # Secure practice: validate user input.
        if not validate_username(username):
            return "Invalid username format.", 400

        if not password:
            return "Password is required.", 400

        connection = get_db()

        try:
            cursor = connection.cursor()

            # Secure practice:
            # Parameterized SQL prevents SQL injection.
            query = """
                SELECT username, password_hash
                FROM users
                WHERE username = ?
            """

            cursor.execute(
                query,
                (username,)
            )

            user = cursor.fetchone()

        finally:
            connection.close()

        # Secure practice:
        # Compare the supplied password with a stored password hash.
        if user and check_password_hash(
            user["password_hash"],
            password
        ):
            return "Login successful!"

        # Do not reveal whether the username exists.
        return "Invalid username or password.", 401

    return """
    <h2>Secure Login</h2>

    <form method="POST">

        <input
            name="username"
            maxlength="50"
            placeholder="Username"
            required
        >

        <br><br>

        <input
            name="password"
            type="password"
            maxlength="128"
            placeholder="Password"
            required
        >

        <br><br>

        <button type="submit">
            Login
        </button>

    </form>
    """


@app.route("/ping")
def ping():
    """
    Resolve a hostname without executing an operating-system command.

    This avoids shell=True and subprocess execution completely.
    """

    host = request.args.get(
        "host",
        "localhost"
    ).strip()

    # Secure practice:
    # Validate the supplied hostname before processing it.
    if not validate_host(host):
        return "Invalid host.", 400

    try:
        # Secure practice:
        # DNS resolution does not require subprocess or shell execution.
        ip_address = socket.gethostbyname(host)

        return {
            "host": host,
            "resolved_ip": ip_address,
            "status": "Host resolved successfully"
        }

    except socket.gaierror:
        return {
            "host": host,
            "status": "Host could not be resolved"
        }, 404


@app.route("/debug-info")
def debug_info():
    """
    Return non-sensitive application information.

    Secrets, passwords, and credentials are never exposed.
    """

    return {
        "environment": os.environ.get(
            "ENVIRONMENT",
            "production"
        ),
        "security": "Sensitive configuration is not exposed."
    }


if __name__ == "__main__":

    # Secure practice:
    # Debug mode is disabled.
    app.run(
        debug=False,
        host="127.0.0.1",
        port=5000
    )