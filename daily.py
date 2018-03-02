import discord
from discord.ext import commands
from datetime import datetime, timedelta
import random
import os

class daily:
	"""Get a nice reward for daily activity."""

	def __init__(self, bot):
		self.bot = bot

	@commands.command(pass_context=True)
	async def daily(self, ctx):
		"""Receive a cool virtual prize, once a day!"""

		targetID = ctx.message.author.id
		targetFolder = "data/daily/"

		prizes = [line.rstrip('\n') for line in open(targetFolder + "prizes.txt")]

		if os.path.isfile(targetFolder + targetID + ".txt"):
			with open(targetFolder + targetID + ".txt", "r") as file:
				lastDaily = datetime.strptime(file.readline()[:-2], "%Y-%m-%d %H:%M:%S.%f")

			if ((datetime.utcnow() - lastDaily) > timedelta(1)):
				with open(targetFolder + targetID + ".txt", w) as file:
					lines = file.readlines()
					lines[0] = str(datetime.utcnow()) + "\n"
					file.writelines(lines)
			else:
				await self.bot.say(ctx.message.author.mention + ", you have already received a daily prize in the last 24 hours!")
				return None
		else:
			with open(targetFolder + targetID + ".txt", "a+") as file:
				file.write(str(datetime.utcnow()) + "\n")

		with open(targetFolder + targetID + ".txt", "a") as file:
			prize = random.choice(prizes)
			file.write(str(prize) + "\n")

		await self.bot.say(":atm:  |  "+ ctx.message.author.mention + ", you received your daily  :yen:  " + prize + ".")

	@commands.command(pass_context=True)
	async def collection(self, ctx):
		"""See the prizes you've collected so far."""

		targetFolder = "data/daily/"
		targetID = ctx.message.author.id

		if os.path.isfile(targetFolder + targetID + ".txt"):
			with open(targetFolder + targetID + ".txt", "r") as file:
				await self.bot.say(":shopping_bags:  |  Here's what you've collected so far, " + ctx.message.author.mention + ":\n • " + " • ".join(file.readlines()[1:]))
		else:
			await self.bot.say(":x:  |  You haven't collected anything! Use the `!daily` command to get an awesome rare prize every day.")

def setup(bot):
	bot.add_cog(daily(bot))
