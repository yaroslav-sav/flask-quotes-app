from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

quotes = [
    {
        "id": 1,
        "quote": "А всё-таки она вертится!",
        "author": "Галилео Галилей",
        "year": 1633,
    },
    {
        "id": 2,
        "quote": "Бог не играет в кости со Вселенной",
        "author" : "Альберт Эйнштейн",
        "year": 1926,
    }
]

@app.route("/")
def index():
    quotes_sort = sorted(quotes, key=lambda x: int(x["year"]))[::-1]
    return render_template("index.html", quotes=quotes_sort)

@app.route("/quotes/<int:quote_id>")
def detail(quote_id):
    quote = None

    for item in quotes:
        if item["id"] == quote_id:
            quote = item
            break

    if quote is None:
        return "quote not found", 404

    return render_template("detail.html", quote=quote)

@app.route("/quotes/add", methods=["GET", "POST"])
def add_quote():
    if request.method == "POST":
        quote = request.form.get("quote", "").strip()
        author = request.form.get("author", "").strip()
        year = request.form.get("year", "").strip()

        errors = []

        if not quote:
            errors.append("Quote is required")

        if not author:
            errors.append("Author is required")

        if not year:
            errors.append("Year is required")
        else:
            try:
                year = int(year)
            except ValueError:
                errors.append("Year must be a number")

        if errors:
            return render_template("add.html", errors=errors, quote=quote, author=author, year=year)

        new_quote = {
            "id": max((x["id"] for x in quotes), default=0) + 1,
            "quote": quote,
            "author": author,
            "year": year,
        }

        quotes.append(new_quote)
        return redirect(url_for("index"))

    return render_template("add.html")

@app.route("/edit/<int:quote_id>", methods=["GET", "POST"])
def edit(quote_id):

    found_id = [x for x in quotes if x["id"] == quote_id]

    if not found_id:
        return "Quote not found", 404

    if request.method == "GET":
        quote = None
        author = None
        year = None

        for item in quotes:
            if item["id"] == quote_id:
                quote = item["quote"]
                author = item["author"]
                year = item["year"]
                break

        if quote is None:
            return "quote not found", 404

        return render_template("edit.html", quote=quote, author=author, year=year)

    if request.method == "POST":
        quote = request.form.get("quote", "").strip()
        author = request.form.get("author", "").strip()
        year = request.form.get("year", "").strip()

        errors = []

        if not quote:
            errors.append("Quote is required")

        if not author:
            errors.append("Author is required")

        if not year:
            errors.append("Year is required")
        else:
            try:
                year = int(year)
            except ValueError:
                errors.append("Year must be a number")

        if errors:
            return render_template("edit.html", errors=errors, quote=quote, author=author, year=year)

        for item in quotes:
            if item["id"] == quote_id:
                item["quote"] = quote
                item["author"] = author
                item["year"] = year
                return redirect(url_for('detail', quote_id=quote_id))

    return "ID does not exist", 404

@app.route("/statistics")
def statistics():
    length = len(quotes)
    return render_template("statistics.html", length=length)

@app.route("/delete/<int:quote_id>", methods=["POST"])
def delete(quote_id):
    global quotes
    quotes = [q for q in quotes if q["id"] != quote_id]
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)