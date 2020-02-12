from flask import Flask, render_template, request, send_from_directory
from models import MobileNet
import os
from math import floor

app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = "uploads"
app.config["STATIC_IMG_FOLDER"] = "static/img"

model = MobileNet()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


# Custom static data
@app.route("/uploads/<path:filename>", methods=["GET"])
def img_render(filename):
    return send_from_directory(
        app.config["UPLOAD_FOLDER"], filename=filename, as_attachment=True
    )


@app.route("/infer", methods=["POST"])
def success():
    if request.method == "POST":
        f = request.files["file"]
        saveLocation = app.config["UPLOAD_FOLDER"] + "/" + f.filename
        f.save(saveLocation)
        inference, confidence = model.infer(saveLocation)
        # make a percentage with 2 decimal points
        confidence = floor(confidence * 10000) / 100
        # delete file after making an inference  - let them be
        # os.remove(saveLocation)
        # # respond with the inference
        return render_template("inference.html", name=inference, confidence=confidence)
        return render_template(
            "inference.html",
            name="test",
            confidence="test confidence",
            image=f.filename,
        )
