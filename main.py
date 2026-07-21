import os
import discord
import requests

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Bot is online 24/7 as {client.user}!")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if client.user.mentioned_in(message):
        prompt = message.content.replace(f'<@{client.user.id}>', '').strip()
        async with message.channel.typing():
            try:
                response = requests.post(
                    "https://groq.com",
                    headers={"Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}"},
                    json={
                        "model": "llama3-8b-8192",
                        "messages": [{"role": "user", "content": prompt}]
                    }
                )
                await message.reply(response.json()['choices']['message']['content'])
            except:
                await message.reply("Error connecting to AI.")

client.run(os.getenv('DISCORD_TOKEN'))
