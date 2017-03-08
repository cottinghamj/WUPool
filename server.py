from flask import Flask, jsonify, render_template, request, session, redirect, url_for, make_response

app = Flask(__name__)
app.debug = True

@app.route("/")
def hello():
    render_template('index.html')


if __name__ == "__main__":
    app.run()