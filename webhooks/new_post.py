import aiohttp
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

    async def handle_page_create(data):
        page_url = data.get('url')
        author = data['triggered_by']['name']
        page_id = data['id']

        new_page_published_message = f"{author} publiserte akkurat en ny side i Wikien!\n{page_url}"

        full_page = await get_page_content(page_id)

        channel_id = int(os.getenv("DISCORD_CHANNEL_ID"))

        channel = client.get_channel(channel_id)

        if channel:
            asyncio.run_coroutine_threadsafe(
                channel.send(new_page_published_message + "\n" + full_page),
                client.loop
            )
        else:
            print(f"Could not find the Discord channel with ID: {channel_id}")

    return app


async def get_page_content(page_id):
    base_url = os.getenv("BASE_URL")
    token = os.getenv("BOOKSTACK_API_ID")
    api_id = os.getenv("BOOKSTACK_API_ID")

    search_url = base_url + f"/pages/{page_id}"
    auth_header = {
        'Authorization': f'Token { api_id }:{ token }'}
    async with aiohttp.ClientSession() as session:
        async with session.get(search_url, headers=auth_header) as response:
            if response.status == 200:
                data = await response.json()
                return data['markdown']
            else:
                return "Could not fetch page content."
