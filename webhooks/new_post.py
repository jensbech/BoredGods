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
        page_url = data.get('url')
        triggered_by = data['triggered_by']['name']

        discord_message = f"{triggered_by} publiserte akkurat en ny side i Wikien!\n{page_url}"

        channel_id = int(os.getenv("DISCORD_CHANNEL_ID"))

        channel = client.get_channel(channel_id)

        if channel:
            asyncio.run_coroutine_threadsafe(
                channel.send(discord_message),
                client.loop
            )
        else:
            print(f"Could not find the Discord channel with ID: {channel_id}")

    return app
