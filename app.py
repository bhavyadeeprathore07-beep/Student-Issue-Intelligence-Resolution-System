from flask import Flask, render_template
import mysql.connector

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


if __name__ == "__main__":
    app.run(debug=True)