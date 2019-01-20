from flask import Flask, render_template, request
import main as UV

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/courses", methods=["GET", "POST"])
def courses():
    if request.method == "GET":
        return render_template("courses.html")

    # POST request
    else:
        attendanceApp = UV.FaceID()
        attendanceApp.main()
