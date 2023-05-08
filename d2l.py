import discord
from discord.ext import commands
from dotenv import load_dotenv
from lotify.client import Client
from bot import bot

import os
import json

load_dotenv()

# Discord Bot
discord_bot_id = int(os.environ['DISCORD_BOT_ID'])
discord_bot_token = os.environ['DISCORD_BOT_TOKEN']
ignore_discord_uid = os.environ.get('IGNORE_DISCORD_UID', None) # (Optional) Ignore specific discord user

# Discord channel to line
message_channel_id = os.environ.get('MESSAGE_CHANNEL_ID', None) # (Optional) To monitor a specific channel can be set optional
lotify_token = os.environ['LOTIFY_TOKEN']

lotify = Client()

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}({bot.user.id})")

@bot.command()
async def ping(ctx):
    await ctx.send(f'{round(bot.latency*1000)}(ms)')
    
@bot.command()
async def clean(ctx,num:int):
    if ctx.message.author.id==378069026552676355:
        await ctx.channel.purge(limit=num+1)
    else:
        await ctx.send('只有Rita可以執行這指令')       

# Check if message channel is set 
set_message_channel = message_channel_id is not None        

@bot.listen()
async def on_message(message):

    if message.webhook_id == discord_bot_id: return # Ignore the bot's own messages

    if ignore_discord_uid is not None:
        ignore_discord_uid_list = ignore_discord_uid.split(':')     
        if str(message.webhook_id) in ignore_discord_uid_list: return # Ignore specific user messages

    if set_message_channel is False:
        lotify_message = message.author.display_name + "\n"
        lotify_message += message.content
        lotify.send_message(
            access_token=lotify_token,
            message=lotify_message
        )
    else:
        count = len(message_channel_id_list)
        for i in range(0,count):
            if message.channel.id == int(message_channel_id_list[i]):
                lotify_message = message.author.display_name + "\n"
                lotify_message += message.content
                lotify.send_message(
                    access_token=lotify_token_list[i],
                    message=lotify_message
                )

if __name__ == "__main__":
    if set_message_channel is False:
        print("Channel is not specified, all channel messages will be forwarded to Line")
        print("Only send public channels, to make private channels also forward, please confirm the private channel message seen by the bot")
        lotify_token_list = lotify_token.split(':')
        if(len(lotify_token_list)!=1):
            print("Do not set up multiple LOTIFY_TOKEN")
        else:
            bot.run(discord_bot_token)
    else :
        # Check if the number of elements of lotify_token is the same as the number of elements of message_channel_id
        message_channel_id_list = message_channel_id.split(':')
        lotify_token_list = lotify_token.split(':')
        if len(message_channel_id_list) != len(lotify_token_list):
            print("Please make sure the number of MESSAGE_CHANNEL_ID and LOTIFY_TOKEN are the same")
        else:
            bot.run(discord_bot_token)