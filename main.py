from flask import Flask, render_template, request, redirect, url_for, jsonify
from bs4 import BeautifulSoup
from simplegmail import Gmail
from simplegmail.query import construct_query

app = Flask(__name__)


def extract_url_from_html(html_body):
    """Extracts the URL from HTML body."""
    try:
        soup = BeautifulSoup(html_body, "html.parser")
        link_tag = soup.find(
            "a",
            href=lambda value: value
            and value.startswith("https://view.connect.etoro.com/"),
        )
        return link_tag.get("href") if link_tag else None
    except Exception as e:
        print(f"Error extracting URL: {e}")
        return None


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/authenticate", methods=["GET", "POST"])
def authenticate():
    if request.method == "POST":
        # Assuming you have a form field named 'email'
        email_sender = request.form.get("email")
        return redirect(url_for("get_urls", email_sender=email_sender))
    return render_template("authentication.html")


@app.route("/get_urls", methods=["GET"])
def get_urls():
    try:
        email_sender = request.args.get("email_sender")

        # Ensure email_sender is provided
        if not email_sender:
            return redirect(url_for("authenticate"))

        gmail = Gmail()

        query_params_1 = {
            "sender": email_sender,
            "newer_than": (1, "day"),
            "unread": True,
        }

        messages = gmail.get_messages(query=construct_query(query_params_1))

        urls = []
        for message in messages:
            html_body = message.html
            url = extract_url_from_html(html_body)

            if url:
                urls.append(url)
            else:
                print("No matching <a> tag found with the specified URL.")

        return jsonify(urls)

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    app.run(debug=True)
