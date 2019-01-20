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

@app.route("/poll")
def poll():
    print(attendanceApp.personScanned)
    personScannedData = '{ "ID" : "1111111"}'
    return personScannedData
    # return attendanceApp.personScanned
