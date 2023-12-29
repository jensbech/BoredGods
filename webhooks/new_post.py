from flask import Flask, request
import json

app = Flask(__name__)


@app.route('/webhooks/new_post', methods=['POST'])
def webhook():
    data = request.json
    print(json(data, indent=4))

    if data['event'] == 'page_create':
        handle_page_create(data)
    else:
        print(f"Received unhandled event type: {data['event']}")

    return 'Webhook received', 200


def handle_page_create(data):
    page_info = data.get('related_item', {})
    page_name = page_info.get('name')
    page_url = data.get('url')
    triggered_by = data['triggered_by']['name']

    print(f"New page created: {page_name}, by {triggered_by}, URL: {page_url}")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
