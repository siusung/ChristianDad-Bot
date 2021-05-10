# EXTERNAL CLASS 1
# handles webscraping jokes and joking with users' messages

import praw
import random
import discord
import utilmodule
from discord.ext import commands

class Jokes(commands.Cog):
    # intializing credentials of the reddit app from praw file
    reddit = utilmodule.praw_object()
    
    def __init__(self, client):
        self.client = client

    def hi_im_dad(self, message):

        # split into woruds
        message = message.split()

        for word in message:
            # single word cases
            if word in ["im", "Im", "i'm", "I'm"]:

                # isolates the part of the string after the keyword
                segment = " ".join(message[message.index(word) + 1: len(message)])
                
                return "Hi " + segment + ", I'm Dad!"

            # multiple word cases
            if word in ["i", "I"]:

                # detects for completed phrase
                if message[message.index(word) + 1] == "am":

                    # isolates the part of the string after the keyword
                    segment = " ".join(message[message.index(word) + 2: len(message)])

                return "Hi " + segment + ", I'm Dad!"

    @commands.command()
    async def plsjoke(self, ctx):
        # choosing to scrape from certain subreddit
        subreddit = self.reddit.subreddit("dadjokes")
        submissions = []

        # compiling a list of the top # jokes
        hot = subreddit.hot(limit = 50)

        for joke in hot:
            submissions.append(joke)

        rand_hot = random.choice(submissions)

        # creating an embed object for prettier messages
        joke_embed = discord.Embed(
            title = rand_hot.title, 
            description = rand_hot.selftext,
            color = 0xF4E337)

        joke_embed.set_footer(text = f"Posted by u/{rand_hot.author.name}")

        await ctx.send(embed = joke_embed)

    @commands.Cog.listener()
    async def on_message(self, message):

        # prevent bot from triggering itself
        if message.author == self.client.user:
            return

        # detects dad joke keywords
        im_keys = ["i am", "I am", "im", "Im", "i'm", "I'm"]
        for key in im_keys:
            if key in message.content:
                # reply in the same channel the message was sent in
                await message.channel.send(self.hi_im_dad(message.content))

def setup(client):
    client.add_cog(Jokes(client))

            

        

