from flask import Flask, render_template
import random
import pip._vendor.requests as requests

app = Flask(__name__)

# @app.route("/")
# def index():
#     return render_template("index.html", name = "World")

# @app.route("/index.html/<name>")
# def index_custom_greeting():
#     return render_template("index.html", name)

@app.route("/get-quote")
def get_quote():
    new_quote = get_random_quote()
    return {"quote": new_quote}


def get_random_quote():
    response = requests.get("https://api.forismatic.com/api/1.0/?method=getQuote&lang=en&format=json")
    if response.status_code == 200:
        quote_data = response.json()
        return f"{quote_data['quoteText']} - {quote_data['quoteAuthor']}"
    return "Unable to fetch a quote at the moment."

# Home Route
@app.route("/")
def home(): # triggered when accesing /, on localhost port 5000 (127.0.0.1:5000/)
    # return "Hello, World!"
    return render_template("original_index.html", name = "World")

# Greeting Route
@app.route("/greet/<name>") # /greet is the function greet(), and /<name> is mentioning that everything that's written in /greet/ is the value of a variable called 'name'
# greet() is triggered by accessing /greet, and it needs to get an argument - it gets it from accessing /greet/whatever_name
# if you try to access only "/greet" or "/greet/", the page will show it's not found (404), so @app.route() defines the only route to trigger greet()
def greet(name): # greet() gets it's name arg by trying to access it in the url of the localhost (127.0.0.1:5000/greet/<name>), <name> is where arg name gets its value
    # return f"Hello, {name}!"
    return render_template("original_index.html", name = name, quote = get_random_quote())

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)