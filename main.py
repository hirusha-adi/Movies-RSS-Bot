import os
import asyncio
import platform
import discord
from discord.ext import commands
import feedparser
from keep_alive import keep_alive
from datetime import datetime

WAIT_SECONDS = 600  # 10 minutes

MBOT_PREFIX = os.environ['MBOT_PREFIX']
TOKEN = os.environ['TOKEN']
FEED_URL = os.environ['FEED_URL']
SECRET_MOVIE_CHANNEL = int(os.environ['SECRET_MOVIE_CHANNEL'])
SECRET_MOVIE_LOG_CHANNEL = int(os.environ['SECRET_MOVIE_LOG_CHANNEL'])
SECRET_OWNER = int(os.environ['SECRET_OWNER'])

client = commands.Bot(command_prefix=MBOT_PREFIX)


@client.event
async def on_ready():
    print(f"Python Version: {platform.python_version()}")
    print(f"Discord.py API Version: {discord.__version__}")
    print(f"Logged in as {client.user.name} | {client.user.id}")
    print(f"Bot is ready to be used!")

    music_channel = client.get_channel(SECRET_MOVIE_CHANNEL)
    music_log_channel = client.get_channel(SECRET_MOVIE_LOG_CHANNEL)

    await music_log_channel.send(f""" **+ BOT ONLINE!** - {datetime.now()} - Bot Prefix: `{MBOT_PREFIX}` - Request Send Time: *{WAIT_SECONDS}* Seconds """)

    while True:
        try:
            blog_feed = feedparser.parse(FEED_URL)

            TITLE = blog_feed.entries[0].title
            try:
                with open("old.txt", "r", encoding="utf-8") as old_file:
                    OLD_TITLE = old_file.read()
            except:
                OLD_TITLE = "NO FILE FOUND"

            if TITLE == OLD_TITLE:
                await music_log_channel.send(f"""**- Info:** RSS Feed not updated yet.""")

            else:
                with open("old.txt", "w", encoding="utf-8") as new_file:
                    new_file.write(TITLE)

                LINK = blog_feed.entries[0].link
                PUB_DATE = blog_feed.entries[0].published
                SUMMARY = blog_feed.entries[0].summary

                print(TITLE)
                print(LINK)
                print(PUB_DATE)
                print(SUMMARY)

                embed = discord.Embed(
                    title=f"""{TITLE}""", color=0x00ff00)
                embed.set_author(name=f"{client.user.name}",
                                 icon_url=f"{client.user.avatar_url}")
                embed.add_field(
                    name="Title", value=f"""{TITLE}""", inline=False)
                embed.add_field(
                    name="Link", value=f"""{LINK}""", inline=False)
                embed.add_field(name="Published on",
                                value=f"""{PUB_DATE}""", inline=False)
                embed.add_field(name="Decription",
                                value=f"""{SUMMARY}""", inline=False)
                await music_channel.send(embed=embed)
                await music_log_channel.send(f"""**+ Success:** Sent *{TITLE}*""")

        except Exception as e:
            await music_log_channel.send(f"""**- Error:** {e}""")

        await asyncio.sleep(WAIT_SECONDS)


@client.command()
async def testshit(ctx):
    blog_feed = feedparser.parse(FEED_URL)
    print(blog_feed.entries)


@client.event
async def on_message(message):
    if client.user == message.author:
        return

    if message.author.id == SECRET_OWNER:
        await client.process_commands(message)

keep_alive()
client.run(TOKEN)
