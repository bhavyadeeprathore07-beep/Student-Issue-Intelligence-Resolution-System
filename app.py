from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

from config import Config


app = Flask(__name__)
app.config.from_object(Config)


def get_db_connection():
    connection = mysql.connector.connect(
        host=app.config["DB_HOST"],
        port=app.config["DB_PORT"],
        user=app.config["DB_USER"],
        password=app.config["DB_PASSWORD"],
        database=app.config["DB_NAME"]
    )

    return connection


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/health")
def health():
    try:
        connection = get_db_connection()

        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()

        cursor.close()
        connection.close()

        if result and result[0] == 1:
            return {
                "status": "ok",
                "database": "connected",
                "project": "Student Issue Intelligence & Resolution System"
            }

        return {
            "status": "error",
            "database": "query failed"
        }, 500

    except mysql.connector.Error as error:
        return {
            "status": "error",
            "database": "connection failed",
            "message": str(error)
        }, 500


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not name or not email or not password:
            flash("All fields are required.", "danger")
            return redirect(url_for("register"))

        if len(password) < 6:
            flash("Password must contain at least 6 characters.", "danger")
            return redirect(url_for("register"))

        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute(
            "SELECT id FROM users WHERE email = %s",
            (email,)
        )

        existing_user = cursor.fetchone()

        if existing_user:
            cursor.close()
            connection.close()

            flash("An account with this email already exists.", "warning")
            return redirect(url_for("register"))

        password_hash = generate_password_hash(password)

        cursor.execute(
            """
            INSERT INTO users (name, email, password_hash, role)
            VALUES (%s, %s, %s, %s)
            """,
            (name, email, password_hash, "student")
        )

        connection.commit()

        cursor.close()
        connection.close()

        flash("Registration successful. Please login.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT id, name, email, password_hash, role
            FROM users
            WHERE email = %s
            """,
            (email,)
        )

        user = cursor.fetchone()

        cursor.close()
        connection.close()

        if user and check_password_hash(
            user["password_hash"],
            password
        ):

            session["user_id"] = user["id"]
            session["user_name"] = user["name"]
            session["user_role"] = user["role"]

            return redirect(url_for("dashboard"))

        flash("Invalid email or password.", "danger")

    return render_template("login.html")

@app.route("/submit-complaint", methods=["GET", "POST"])
def submit_complaint():

    if "user_id" not in session:
        return redirect(url_for("login"))

    connection = get_db_connection()

    if request.method == "POST":

        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        location = request.form.get("location", "").strip()
        category_id = request.form.get("category_id")

        if not title or not description or not category_id:
            flash("Please fill all required fields.", "danger")
            connection.close()
            return redirect(url_for("submit_complaint"))

        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO complaints
            (user_id, title, description, location, category_id)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                session["user_id"],
                title,
                description,
                location,
                category_id
            )
        )

        connection.commit()

        cursor.close()
        connection.close()

        flash("Your issue has been submitted successfully.", "success")

        return redirect(url_for("my_complaints"))

    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        "SELECT id, name FROM categories ORDER BY name"
    )

    categories = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "submit_complaint.html",
        categories=categories
    )


@app.route("/my-complaints")
def my_complaints():

    if "user_id" not in session:
        return redirect(url_for("login"))

    connection = get_db_connection()

    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT
            c.id,
            c.title,
            c.description,
            c.location,
            c.priority,
            c.status,
            c.created_at,
            cat.name AS category
        FROM complaints c
        LEFT JOIN categories cat
            ON c.category_id = cat.id
        WHERE c.user_id = %s
        ORDER BY c.created_at DESC
        """,
        (session["user_id"],)
    )

    complaints = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "my_complaints.html",
        complaints=complaints
    )

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("login"))

    return render_template(
        "dashboard.html",
        name=session["user_name"],
        role=session["user_role"]
    )


@app.route("/logout")
def logout():

    session.clear()

    flash("You have been logged out.", "success")

    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)