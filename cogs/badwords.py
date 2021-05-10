# EXTERNAL CLASS 2
# handles logging of message statistics

import csv
import random
import discord
import utilmodule
from discord.ext import commands

class Badwords(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def mystats(self, ctx):

        # formatting user ID
        tag = f"{ctx.author.name}#{ctx.author.discriminator}"

        reader = list(csv.reader(open('badword_stats.csv'), delimiter = ','))

        message_ct = None
        badword_ct = None
        message_w_badword_pct = None

        for row in reader:
            # prevent empty list error
            if len(row) == 0:
                continue
            if tag == row[0]:
                message_ct = row[1]
                badword_ct = row[2]
                message_w_badword_pct = round(int(row[3])/int(row[1]) * 100, 2)
                badword_hundred = round(int(row[2])/int(row[4]) * 100)
        
        # pretty message
        embed = discord.Embed(
            title = 'Swear-word Summary',
            description = '"Keep it up, son!"',
            color = 0xF4E337
        )

        # formatting stats
        embed.add_field(name = 'Total Message #', value = f"{message_ct}", inline = False)
        embed.add_field(name = 'Total Bad Word #', value = f"{badword_ct}", inline = False)
        embed.add_field(name = 'Messages w/ Bad Words', value = f"{message_w_badword_pct}%", inline = False)
        embed.add_field(name = 'Avg # Bad Words per 100 Messages', value = f"{badword_hundred}", inline = False)
        embed.set_footer(icon_url = ctx.author.avatar_url, text = tag)

        await ctx.send(embed = embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        # log messages on a come-and-go basis

        # prevent bot from triggering itself
        if message.author == self.client.user:
            return
            
        # discord tag of sender of message
        tag = f"{message.author.name}#{message.author.discriminator}"

        reader = list(csv.reader(open('badword_stats.csv'), delimiter = ','))

        # bible verses about profanity
        dad_responses = [
            "**Colossians 3:8** - *'But now you must put them all away: anger, wrath, malice, slander, and obscene talk from your mouth.'*",
            "**Ephesians 4:29** - *'Let no corrupting talk come out of your mouths, but only such as is good for building up, as fits the occasion, that it may give grace to those who hear.'*",
            "**Matthew 12:36-37** - *'I tell you, on the day of judgment people will give account for every careless word they speak, for by your words you will be justified, and by your words you will be condemned.'*",
            "**James 3:6-8** - *'And the tongue is a fire, a world of unrighteousness.'*",
            "**Proverbs 21:23** - *'Whoso keepeth his mouth and his tongue keepeth his soul from troubles.'*"
        ]

        # reprimands upon hearing bad words
        num_bad_words = self.detector(message.content)
        if num_bad_words > 0:
            await message.channel.send(f"Hey now {message.author.name}, let's keep it Christian!")
            await message.channel.send(random.choice(dad_responses))

        num_words = len(message.content.split())

        # user already recorded?
        existing = False
        
        # recurring author
        for row in reader:
            # prevent empty list error
            if len(row) == 0:
                continue
            if tag == row[0]:
                existing = True
                # incrementing total messages
                row[1] = str(int(row[1]) + 1)

                # incrementing total number of bad words
                row[2] = str(int(row[2]) + num_bad_words)

                # incrementing total number of messages containing bad words
                row[3] = str(int(row[3]) + utilmodule.flatten(num_bad_words))

                # incrementing total number of words
                row[4] = str(int(row[4]) + num_words)
                        
                # writing in the incremented contents of the reader
                writer = csv.writer(open('badword_stats.csv', 'w', newline = ""), delimiter = ',')
                writer.writerows(reader)

        # new message authors
        if not existing:

            # append new row for new author
            appender = open('badword_stats.csv', 'a')
            appender.write(f"{tag}, 1, {num_bad_words}, {utilmodule.flatten(num_bad_words)}, {num_words}")

    def detector(self, message):

        # sums up bad words
        bad_word_count = 0

        bad_words = ["fuck", "shit", "ass", "damn", "bitch", "bastard", "dick", "hell"]
        for word in bad_words:
            bad_word_count += message.lower().count(word)

        return bad_word_count

def setup(client):
    client.add_cog(Badwords(client))
