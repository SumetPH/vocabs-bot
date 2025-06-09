import discord
from discord.ext import commands
from utils.llm import conversation_sample, translate_vocab, generate_sentence
from utils.vocab import remember_vocab, random_vocab

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"{bot.user} is ready and online!")

@bot.tree.command(name="random-vocab", description="Random vocab")
async def random_vocab_slash(interaction: discord.Interaction):
    rw = await random_vocab()
    await interaction.response.send_message(rw['vocab'], view=RandomVocabView(vocab=rw['vocab']))

@bot.tree.command(name="conversation-sample", description="Conversation sample from random vocab")
async def conversation_sample_slash(interaction: discord.Interaction):
    rw = await random_vocab()
    cs = await conversation_sample(vocab=rw['vocab'])
    await interaction.response.send_message(f"```{cs}```")


class HintButton(discord.ui.Button):
    def __init__(self, vocab):
        super().__init__(label='Hint', style=discord.ButtonStyle.secondary)
        self.vocab = vocab

    async def callback(self, interaction: discord.Interaction):
        sentence = await generate_sentence(self.vocab)
        await interaction.response.send_message(sentence.sentence, view=RandomVocabView(vocab=self.vocab, show_hint=False))    

class TranslateButton(discord.ui.Button):
    def __init__(self, vocab):
        super().__init__(label='Translate', style=discord.ButtonStyle.primary)
        self.vocab =vocab
    
    async def callback(self, interaction: discord.Interaction):
        translate = await translate_vocab(self.vocab)
        await interaction.response.send_message(translate, view=RandomVocabView(vocab=self.vocab, show_translate=False))

class RememberButton(discord.ui.Button):
    def __init__(self, vocab):
        super().__init__(label='Remember', style=discord.ButtonStyle.success)
        self.vocab = vocab

    async def callback(self, interaction: discord.Interaction):
        result = await remember_vocab(self.vocab)
        if(result == True):
            await interaction.response.send_message("Remembered")
        else:
            await interaction.response.send_message("Error something went wrong")

class RandomVocabView(discord.ui.View):
    def __init__(self, vocab, show_translate=True, show_hint=True, show_remember=True):
        super().__init__()
        self.vocab = vocab

        if(show_remember):
            self.add_item(RememberButton(vocab=vocab))

        if(show_translate):
            self.add_item(TranslateButton(vocab=vocab))
        
        if(show_hint):
            self.add_item(HintButton(vocab=vocab))
        




