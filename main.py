from simplegmail import Gmail
from simplegmail.query import construct_query
from bs4 import BeautifulSoup

def extract_url_from_html(html_body):
    """Extracts the URL from HTML body."""
    try:
        soup = BeautifulSoup(html_body, 'html.parser')
        link_tag = soup.find('a', href=lambda value: value and value.startswith('https://view.connect.etoro.com/'))
        return link_tag.get('href') if link_tag else None
    except Exception as e:
        print(f"Error extracting URL: {e}")
        return None

def main():
    try:
        gmail = Gmail()

        query_params_1 = {
            "sender": "wguevarab02@gmail.com",
            "newer_than": (1, "day"),
            "unread": True,
        }

        messages = gmail.get_messages(query=construct_query(query_params_1))

        for message in messages:
            html_body = message.html
            url = extract_url_from_html(html_body)

            if url:
                print(url)
            else:
                print('No matching <a> tag found with the specified URL.')

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

