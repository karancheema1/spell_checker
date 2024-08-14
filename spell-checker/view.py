from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/')
def home():
    return "Welcome to the Spell Checker API"


@app.route('/check', methods=['POST'])
def check_spelling():
    data = request.json
    text = data.get('text', '')
    # TODO: Implement spell checking logic
    return jsonify({"original": text, "corrected": text})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
