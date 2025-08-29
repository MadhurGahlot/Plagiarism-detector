from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Hello World - Plagiarism Detector is Running! <br> It is Created BY Madhur Gahlot "


if __name__ == "__main__":
    app.run(debug=True)
