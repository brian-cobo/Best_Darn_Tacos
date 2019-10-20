from flask import Flask, render_template, request, jsonify, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/parse_data", methods=["GET", "POST"])
def parse_data():
    if request.method == "POST":
        data = request.json

        budget = data['budget']
        zipCode = data['zipCode']

        print(budget, zipCode)
        return jsonify(data)
    else:
        return render_template('index.html')

if __name__== '__main__':
    app.run


if __name__ == '__main__':
    app.run(debug=True)

