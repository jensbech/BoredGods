from flask import Flask, request
import json
import asyncio
import os


def create_app(discord_client):
    app = Flask(__name__)
    global client
    client = discord_client

    @app.route('/webhooks/new_post', methods=['POST'])
    def webhook():
        data = request.json
        print(data)
        print(json.dumps(data, indent=4))

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

        discord_message = f"A new Wiki page **{page_name}** was just created by {triggered_by}\n{page_url}"

        # Assuming you have the channel ID as an environment variable
        channel_id = int(os.getenv("DISCORD_CHANNEL_ID"))

        # Get the Discord channel object
        channel = client.get_channel(channel_id)

        # If the channel was found, send the message
        if channel:
            asyncio.run_coroutine_threadsafe(
                channel.send(discord_message),
                client.loop
            )
        else:
            print(f"Could not find the Discord channel with ID: {channel_id}")

    return app
