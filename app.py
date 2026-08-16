from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/health")
def health():
    return {"status": "ok", "project": "Student Issue Intelligence & Resolution System"}

if __name__ == "__main__":
    app.run(debug=True)
