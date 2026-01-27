from config import *
from logic import *
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print("Bot başlatıldı!")

@bot.command()
async def help_me(ctx):
    await ctx.send(
        "Kariyer Yardım Botu\n\n"
        "!start → kariyerini bulmak için sorulacak soruları başlatır\n"
        "Bot, yaşını, mesleğini vs. sorar\n"
        "Sonra da sana uygun bir meslek veya kariyer yolu bulur\n"
    )


@bot.command()
async def start(ctx: commands.Context):
    await ctx.send("Başlamak için tıkla", view=StartView())



if __name__ == "__main__":
    bot.run(TOKEN)