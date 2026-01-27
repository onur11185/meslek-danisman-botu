import discord
from discord.ui import View, Button

user_data = {}

class StartView(View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="Başla", style=discord.ButtonStyle.success)
    async def start_button(self, interaction: discord.Interaction, button: Button):
        user_id = interaction.user.id

        user_data[user_id] = {
            "yas": None,
            "hedef": None
        }

        await interaction.response.send_message(
            "Yaş aralığın?:",
            view=AgeView(),
            ephemeral=True
        )

class AgeView(View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="18 yaş altı", style=discord.ButtonStyle.primary)
    async def under_18(self, interaction: discord.Interaction, button: Button):
        await self.go_next(interaction, "under_18")

    @discord.ui.button(label="18–25", style=discord.ButtonStyle.primary)
    async def age_18_25(self, interaction: discord.Interaction, button: Button):
        await self.go_next(interaction, "18_25")

    @discord.ui.button(label="25+", style=discord.ButtonStyle.primary)
    async def age_25_plus(self, interaction: discord.Interaction, button: Button):
        await self.go_next(interaction, "25_plus")

    async def go_next(self, interaction, age_key):
        user_data[interaction.user.id]["yas"] = age_key

        await interaction.response.send_message(
            "Tamam, şimdi hedefini seç:",
            view=GoalView(age_key),
            ephemeral=True
        )

class GoalView(View):
    def __init__(self, age_key):
        super().__init__()

        if age_key == "under_18":
            self.add_item(GoalButton("📚 İlgi alanlarını keşfet", "kesfet"))
            self.add_item(GoalButton("🧠 Beceri öğrenmek", "beceri"))
            self.add_item(GoalButton("🚀 Kariyere hazırlanmak", "kariyer"))

        elif age_key == "18_25":
            self.add_item(GoalButton("🎓 Alan / bölüm seçmek", "alan"))
            self.add_item(GoalButton("💼 İş bulmak", "is"))
            self.add_item(GoalButton("🚀 Kariyer kurmak", "kariyer"))

        elif age_key == "25_plus":
            self.add_item(GoalButton("🔁 Kariyer değiştirmek", "degisim"))
            self.add_item(GoalButton("💰 Daha iyi gelir", "gelir"))
            self.add_item(GoalButton("🧘 Daha dengeli iş", "denge"))

class GoalButton(Button):
    def __init__(self, label, value):
        super().__init__(label=label, style=discord.ButtonStyle.secondary)
        self.value = value

    async def callback(self, interaction: discord.Interaction):
        user_data[interaction.user.id]["hedef"] = self.value

        await interaction.response.send_message(
            "Hedefin kaydedildi",
            ephemeral=True
        )


