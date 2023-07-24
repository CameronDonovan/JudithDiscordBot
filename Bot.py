from nextcord.ext import commands
import nextcord

import requests
import dotenv
import json
import os

dotenv.load_dotenv()

prefix = os.getenv("BOT_PREFIX")
token = os.getenv("DISCORD_TOKEN")
CarterAPI = os.getenv("CARTER_TOKEN")

UIName = "Judith"  # You can change this to anything you want

intents = nextcord.Intents.all()
# Change this to anything you want to display on your bots Activity
activity = nextcord.Activity(type=nextcord.ActivityType.watching, name="Horse Dressage Videos")
client = commands.Bot(command_prefix=prefix, intents=intents, activity=activity)

client.remove_command("help")

# On startup
@client.event
async def on_ready():
    print(f"{UIName} | Operational")


@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    await ctx.send(f'`cogs.{extension}` was loaded.')

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    await ctx.send(f'`cogs.{extension}` was unloaded. You can no longer use it until it is reloaded.')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

def SendMessage(message, CarterAPI):
    response = requests.post(
                    "https://api.carterlabs.ai/api/chat",
                    headers={
                        "Content-Type": "application/json"
                    },
                    data=json.dumps({
                        "text": message.content,
                        "key": CarterAPI,
                        "user_id": message.author.id
                    })
                )
    
    RawResponse = response.json()
    Response = RawResponse["output"]
    FullResponse = Response["text"]
    ResponseOutput = FullResponse

    return ResponseOutput


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    channel = message.channel
    if message.author != client.user and not message.content.lower().startswith(prefix) and "judith" in message.content.lower():
        try:
            async with channel.typing():
                ResponseOutput = SendMessage(message, CarterAPI)
                await message.reply(ResponseOutput)

        except Exception as err:
            await channel.send(f"There was an Error: {err}")
    
    elif message.reference:
        replied_to = await message.channel.fetch_message(message.reference.message_id)
        if replied_to.author == client.user:
            async with channel.typing():
                ResponseOutput = SendMessage(message, CarterAPI)
                await message.reply(ResponseOutput)

    # Only temporary!
    if isinstance(channel, nextcord.DMChannel) and message.author != client.user and not message.content.startswith(prefix):
        try:
            async with channel.typing():
                ResponseOutput = SendMessage(message, CarterAPI)
                await message.reply(ResponseOutput)

        except Exception as err:
            await channel.send(f"There was an Error: {err}")

    await client.process_commands(message)




client.run(token)