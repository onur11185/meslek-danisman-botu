import discord
from careers import *
from discord.ui import View, Button, Select

user_data = {}

def calculate_career_scores(user):
    results = []

    for career_name, data in careers.items():
        score = 0

        
        for ilgi in user.get("ilgi", []):
            if ilgi in data.get("ilgi", []):
                score += 2


        if user.get("yas") in data.get("yas", []):
            score += 2


        if user.get("guc") in data.get("guc", []):
            score += 2


        if user.get("hedef") in data.get("hedef", []):
            score += 2


        if user.get("internet") in data.get("internet", []):
            score += 2


        if user.get("preference") in data.get("preference", []):
            score += 2


        if user.get("risk") in data.get("risk", []):
            score += 2


        if user.get("zaman") in data.get("zaman", []):
            score += 2


        percentage = min(100, int((score / 16) * 100))

        results.append({
            "career": career_name,
            "score": score,
            "percent": percentage
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:3]



class StartView(View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="Başla", style=discord.ButtonStyle.success)
    async def start_button(self, interaction: discord.Interaction, button: Button):
        user_id = interaction.user.id

        user_data[user_id] = {
            "yas": None,
            "hedef": None,  
            "ilgi": [],
            "guc": None,
            "internet": None,
            "preference": None,
            "risk": None,
            "zaman": None
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
            "Şimdi ilgilerini seç:",
            view=InterestView(),
            ephemeral=True
        )



class InterestView(View):
    def __init__(self):
        super().__init__()
        self.add_item(InterestSelect())



class InterestSelect(Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="💻 Teknoloji", value="teknoloji"),
            discord.SelectOption(label="🎨 Sanat / Müzik", value="yaratici"),
            discord.SelectOption(label="💼 İş / Girişim", value="girisim"),
            discord.SelectOption(label="🤝 İnsanlara yardım", value="yardim"),
            discord.SelectOption(label="🔬 Bilim", value="bilim"),
        ]

        super().__init__(
            placeholder="Şimdi aşağıdakilerden 2 tane ",
            min_values=1,
            max_values=2,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        user_data[interaction.user.id]["ilgi"] = self.values
        await interaction.response.send_message(
            "Şimdi ise güçlü olduğun alanları seç",
            view=StrengthView(),
            ephemeral=True
        )


class StrengthView(View):
    def __init__(self):
        super().__init__()
        self.add_item(StrengthButton("🧠 Problem çözme", "problem"))
        self.add_item(StrengthButton("🎨 Yaratıcılık", "yaratici"))
        self.add_item(StrengthButton("🗣 İletişim", "iletisim"))
        self.add_item(StrengthButton("📋 Düzen / planlama", "duzen"))



class StrengthButton(Button):
    def __init__(self, label, value):
        super().__init__(label=label, style=discord.ButtonStyle.primary)
        self.value = value

    async def callback(self, interaction: discord.Interaction):
        user_data[interaction.user.id]["guc"] = self.value

        await interaction.response.send_message(
            "Şimdi ise, internet erişiminin ne kadar olduğunu seç   ",
            view=InternetView(),
            ephemeral=True
        )



class InternetView(View):
    def __init__(self):
        super().__init__()
        self.add_item(InternetButton("❌ Kısıtlı", "low"))
        self.add_item(InternetButton("⚠️ Orta", "medium"))
        self.add_item(InternetButton("✅ İyi", "high"))



class InternetButton(Button):
    def __init__(self, label, value):
        super().__init__(label=label, style=discord.ButtonStyle.primary)
        self.value = value

    async def callback(self, interaction: discord.Interaction):
        user_data[interaction.user.id]["internet"] = self.value

        await interaction.response.send_message(
            "Şimdi ise, tercih ettiğiniz çalışma ortamını seçin;",
            view=preferenceView(),
            ephemeral=True
        )



class preferenceView(View):
    def __init__(self):
        super().__init__()
        self.add_item(preferenceButton("🏢 Ofis", "ofis"))
        self.add_item(preferenceButton("💻 Uzaktan", "uzak"))
        self.add_item(preferenceButton("🌳 Saha", "saha"))
        self.add_item(preferenceButton("🔬 Laboratuvar", "lab"))



class preferenceButton(Button):
    def __init__(self, label, value):
        super().__init__(label=label, style=discord.ButtonStyle.primary)
        self.value = value

    async def callback(self, interaction: discord.Interaction):
        user_data[interaction.user.id]["preference"] = self.value

        await interaction.response.send_message(
            "Şimdi ise, risk toleransınızı seçin",
            view=riskView(),
            ephemeral=True
        )


class riskView(View):
    def __init__(self):
        super().__init__()
        self.add_item(riskButton("🟢 Düşük", "low"))
        self.add_item(riskButton("🟡 Orta", "med"))
        self.add_item(riskButton("🔴 Yüksek", "high"))


class riskButton(Button):
    def __init__(self, label, value):
        super().__init__(label=label, style=discord.ButtonStyle.primary)
        self.value = value

    async def callback(self, interaction: discord.Interaction):
        user_data[interaction.user.id]["risk"] = self.value

        await interaction.response.send_message(
            "Şimdi ise, haftada ne kadar boş zamanızın olduğunu seçin;",
            view=TimeView(),
            ephemeral=True
        )



class TimeView(View):
    def __init__(self):
        super().__init__()
        self.add_item(TimeButton("⏱ 2–5 saat", "2_5"))
        self.add_item(TimeButton("⏰ 5–10 saat", "5_10"))
        self.add_item(TimeButton("🔥 10+ saat", "10_plus"))



class TimeButton(Button):
    def __init__(self, label, value):
        super().__init__(label=label, style=discord.ButtonStyle.primary)
        self.value = value

    async def callback(self, interaction: discord.Interaction):
        user_data[interaction.user.id]["zaman"] = self.value

        user = user_data[interaction.user.id]
        top_careers = calculate_career_scores(user)

        text = "🎯 **Sana en uygun kariyerler:**\n\n"
        for i, c in enumerate(top_careers, start=1):
            text += f"**{i}. {c['career']}** — %{c['percent']}\n"
            desc = careers.get(c['career'], {}).get("description", "")
            if desc:
                text += f"{desc}\n"

            how_steps = careers.get(c['career'], {}).get("how", [])
            if how_steps:
                text += "     Nasıl başlarsın?\n"
                for step in how_steps:
                    text += f"      • {step}\n"
                text += "\n"
            else:
                text += "\n" 

        await interaction.response.send_message(text, ephemeral=True)
