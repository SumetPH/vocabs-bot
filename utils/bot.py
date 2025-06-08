import discord
from discord.ext import commands
from utils.llm import conversation_sample, translate_word, generate_sentence
from utils.word import remember_word, random_word

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")

@bot.command()
async def rw(ctx: commands.Context):
    rw = await random_word()
    await ctx.send(rw['word'], view=RandomWordView(word=rw['word']))

@bot.command()
async def cs(ctx: commands.Context):
    rw = await random_word()
    cs = await conversation_sample(word=rw['word'])
    await ctx.send(f"```{cs}```")

class HintButton(discord.ui.Button):
    def __init__(self, word):
        super().__init__(label='Hint', style=discord.ButtonStyle.secondary)
        self.word = word

    async def callback(self, interaction: discord.Interaction):
        sentence = await generate_sentence(self.word)
        await interaction.response.send_message(sentence.sentence, view=RandomWordView(word=self.word, show_hint=False))    

class TranslateButton(discord.ui.Button):
    def __init__(self, word):
        super().__init__(label='Translate', style=discord.ButtonStyle.primary)
        self.word = word
    
    async def callback(self, interaction: discord.Interaction):
        translate = await translate_word(self.word)
        msg = f"Translate : {translate.translate_th}\nParts of Speech : {translate.parts}"
        await interaction.response.send_message(msg, view=RandomWordView(word=self.word, show_translate=False))

class RememberButton(discord.ui.Button):
    def __init__(self, word):
        super().__init__(label='Remember', style=discord.ButtonStyle.success)
        self.word = word

    async def callback(self, interaction: discord.Interaction):
        result = await remember_word(self.word)
        if(result == True):
            await interaction.response.send_message("Remembered")
        else:
            await interaction.response.send_message("Error something went wrong")

class RandomWordView(discord.ui.View):
    def __init__(self, word, show_translate=True, show_hint=True, show_remember=True):
        super().__init__()
        self.word = word

        if(show_remember):
            self.add_item(RememberButton(word=word))

        if(show_translate):
            self.add_item(TranslateButton(word=word))
        
        if(show_hint):
            self.add_item(HintButton(word=word))
        




