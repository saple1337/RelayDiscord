import discord
import json
import aiohttp
import logging
import asyncio
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)

with open('relay_config.json') as config_file:
    config = json.load(config_file)
with open('relay_whitelist.json') as whitelist_file:
    whitelist = json.load(whitelist_file)

intents = discord.Intents.default()
intents.messages = True
client = discord.Client(intents=intents)

user_conversations = {}
user_cooldowns = {}

@client.event
async def on_ready():
    logging.info(f'Logged in as {client.user}')
    await client.change_presence(activity=discord.Game(name=config["activity"]))

@client.event
async def on_message(message):
    if not isinstance(message.channel, discord.DMChannel) or message.author.bot:
        return

    user_id = str(message.author.id)

    if user_id in user_cooldowns and datetime.now() < user_cooldowns[user_id]:
        remaining_time = user_cooldowns[user_id] - datetime.now()
        await send_embed(f"You're on cooldown! Please wait {str(remaining_time).split('.')[0]} before using this bot again.")
        return

    if user_id not in user_conversations:
        user_conversations[user_id] = {"step": 1}

    conversation = user_conversations[user_id]
    step = conversation["step"]

    async def send_embed(content):
        embed = discord.Embed(description=content, color=discord.Color.blue())
        await message.channel.send(embed=embed)

    if step == 1:
        await send_embed("What game are you hosting?")
        conversation["step"] = 2
    elif step == 2:
        conversation["game_name"] = message.content
        await send_embed("What time is this game being hosted? (Please provide a Discord timestamp)")
        conversation["step"] = 3
    elif step == 3:
        conversation["timestamp"] = message.content
        await send_embed("Hey, what would your message like to be?")
        conversation["step"] = 4
    elif step == 4:
        conversation["user_message"] = message.content

        authorized, user_server_name, user_server_image, user_server_link = False, None, None, None
        for server in whitelist["servers"]:
            if user_id in server["authorized_users"]:
                authorized = True
                user_server_name = server["server_name"]
                user_server_image = server["server_image"]
                user_server_link = server["server_link"]
                break

        if authorized:
            logging.info(f"User {message.author} is authorized, preparing to relay message.")
            async with aiohttp.ClientSession() as session:
                for server in whitelist["servers"]:
                    if server["server_name"] != user_server_name:
                        webhook_data = {
                            "username": user_server_name,
                            "avatar_url": user_server_image,
                            "content": "@everyone",  
                            "embeds": [{
                                "title": f"🎮 {conversation['game_name']} Game 🎮",
                                "description": f"\nTime: {conversation['timestamp']}\n\nInformation: {conversation['user_message']}\n\n[Join us here]({user_server_link})",
                                "color": 16711680,
                                "footer": {"text": "If you want this extension added to your server, please add saple"}
                            }]
                        }

                        logging.info(f"Sending webhook with username: {user_server_name} and avatar_url: {user_server_image}")
                        try:
                            async with session.post(server["webhook_link"], json=webhook_data) as response:
                                if response.status == 204:
                                    logging.info(f"Message successfully relayed to {server['server_name']}.")
                                else:
                                    logging.error(f"Failed to relay message to {server['server_name']}. Status: {response.status}")
                        except Exception as e:
                            logging.error(f"Exception occurred while sending message to {server['server_name']}: {str(e)}")

            user_cooldowns[user_id] = datetime.now() + timedelta(hours=3)
            await send_embed(config["dm_response"])
        else:
            await send_embed("You are not authorized to use this bot.")
            logging.warning(f"Unauthorized access attempt by {message.author}.")

        user_conversations.pop(user_id, None)

client.run(config["token"])
