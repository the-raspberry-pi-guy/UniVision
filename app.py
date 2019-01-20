from flask import Flask, render_template, request
import main as UV
import json

app = Flask(__name__)
attendanceApp = UV.FaceID()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/courses", methods=["GET", "POST"])
def courses():
    if request.method == "GET":
        return render_template("courses.html")

    # POST request
    else:
        attendanceApp.main()

@app.route("/list")
def list():
    return render_template("list.html")

@app.route("/poll")
def poll():
    lastPersonScannedId = attendanceApp.getLastPersonScanned()
    # personScannedData = '{"ID" : "' + lastPersonScannedId + '"}'
    personScannedData = attendanceApp.getStudentJson(lastPersonScannedId)
    return personScannedData
