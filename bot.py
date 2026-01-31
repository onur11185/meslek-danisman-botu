from config import *
from logic import *
from careers import *
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
        "Kariyer Yardım Botu\n"
        "!start: kariyerini bulmak için sorulacak soruları başlatır;\n"
        "Bot, yaşını, mesleğini vs. sorar;\n"
        "Sonra da sana uygun bir meslek veya kariyer yolu bulur.\n"
    )


@bot.command()
async def start(ctx: commands.Context):
    await ctx.send("Başlamak için tıkla", view=StartView())

@bot.command()
async def data(ctx):
    user_id = ctx.author.id

    if user_id not in user_data:
        await ctx.send("Henüz veri yok")
        return

    data = user_data[user_id]

    mesaj = (
        f"📊 *Bilgilerin*\n\n"
        f"🧒 Yaş: `{data['yas']}`\n"
        f"🎯 Hedef: `{data['hedef']}`\n"
        f"💡 İlgi Alanları: `{', '.join(data['ilgi']) if data['ilgi'] else 'Yok'}`\n"
        f"💪 Güçlü Yön: `{data['guc']}`\n"
        f"⚠️ İnternet Erişimin: `{data['internet']}`\n"
        f"⚠️ İş Yeri Tercihin: `{data['preference']}`\n"
        f"💪 Risk Toleransınız: `{data['risk']}`\n"
        f"⏰ Zaman: `{data['zaman']}`"
    )

    await ctx.send(mesaj)

if __name__ == "__main__":
    bot.run(TOKEN)
