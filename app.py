from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    error = None

    if request.method == "POST":
        num1 = request.form.get("num1")
        num2 = request.form.get("num2")

        try:
            result = int(num1) + int(num2)
        except:
            error = "숫자를 올바르게 입력해주세요."

    return render_template("calculator.html", result=result, error=error)


if __name__ == "__main__":
    app.run(debug=True)