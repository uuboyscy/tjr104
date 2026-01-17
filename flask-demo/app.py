from flask import Flask, request

from utils.model import get_rec_result

app = Flask(__name__)

@app.route("/")
def hello_flask():
    return "Hello Flask!"

# /greet/<user_name>
@app.route("/greet/<user_name>")
def greet(user_name):
    return f"<h1>Hello {user_name}</h1>"

# /api/recommendation/<user_id>
@app.route("/api/recommendation/<user_id>")
def recommendation(user_id):
    result = get_rec_result(user_id)
    return result

# /two_sum/<x>/<y>
@app.route("/two_sum/<int:x>/<int:y>")
def two_sum(x: int, y: int):
    return str(x + y)

# /hello_get?user_name=Allen&age=22
@app.route("/hello_get")
def hello_get():
    user_name = request.args.get("user_name")
    age = request.args.get("age")
    if not user_name:
        return "What is your name?"
    if not age:
        return f"Hello {user_name}"
    return f"Hello {user_name}, you are {age} years old."

# /hello_post
@app.route("/hello_post", methods=["GET", "POST"])
def hello_post():
    html = """
    <form method="post">
      <label for="name">Name</label>
      <input id="name" name="name" type="text" />
      <button type="submit">Submit</button>
    </form>
    """
    request_method = request.method
    name = request.form.get("name")

    if request_method == "POST":
        html += f"""<h3>Hello {name} !</h3>"""

    return html

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
