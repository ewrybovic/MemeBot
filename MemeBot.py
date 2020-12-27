import os
import csv
import random
import time
from dotenv import load_dotenv

# Reddit python wrapper
import praw

# Discord API
from discord.ext import commands, tasks

# read the .env file and assign to variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
CHANNEL = os.getenv("DISCORD_CHANNEL_ID")
R_ID= os.getenv('REDDIT_ID')
R_SECRET = os.getenv('REDDIT_SECRET')
R_USER = os.getenv('REDDIT_USER')

# Load the MemeWorthy Subreddits from CSV
subreddits = []
with open('MemeReddits.csv', newline='') as csv_file:
    reader = csv.reader(csv_file)
    for row in reader:
        for subreddit in row:
            subreddits.append(subreddit)

# Set the prefix for a bot command
bot = commands.Bot(command_prefix='!')

# Create the reddit API connection
reddit = praw.Reddit(client_id = R_ID, client_secret=R_SECRET, user_agent=R_USER)

def get_meme():
    # Get subreddit name from list
    subreddit = subreddits[random.randint(0,len(subreddits) - 1)]

    postNum = random.randint(0,9)
    currentNum = 0
    submissions = []

    # Bot can get from either top(1) or hot(0)
    if random.randint(0,1) ==0:
        submissions = reddit.subreddit(subreddit).hot(limit=10)
    else:
        submissions = reddit.subreddit(subreddit).top('day', limit=10)

    # Cant index the submissions since it is a generator so loop through it until we hit the post number
    for submission in submissions:
        if postNum == currentNum:

            # Check if the post has selftext, if so it is not a pic/vid post
            if not submission.selftext and "v.redd.it" not in submission.url and "youtube.com" in not submission.url:
                return submission
            # Get a new meme by recursion
            else:
                return get_meme()

        currentNum += 1

# Function that executes with the !meme
@bot.command(name="meme", help="Gets a meme from a random subreddit")
async def meme_command(ctx):
    submission = get_meme()
    await ctx.send(f'{submission.title} [{submission.subreddit}]\n{submission.url}')

# Error handling for the get_meme funciton
@meme_command.error
async def get_meme_error(ctx, error):
    await ctx.send(f"Error finding meme: {error}")

@tasks.loop(hours=6)
async def loop():
    await bot.wait_until_ready()
    channel = bot.get_channel(int(CHANNEL))

    try:
        # Get the channel that we are gonna send the meme to
        submission = get_meme()
        await channel.send(f"{submission.title}\n{submission.url}")
    except:
        await channel.send(f"Error getting meme in task")


@bot.event
async def on_ready():
    loop.start()

bot.run(TOKEN)

