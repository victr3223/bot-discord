import discord
from discord.ext import commands
from discord import app_commands
import os

from config import TOKEN

intents = discord.Intents.default()
intents.guilds = True
intents.members = True  # necessário se quiser acessar membros/guildas
intents.message_content = False  # True se quiser ler o conteúdo das mensagens (requer ativar no portal do bot)

bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

@bot.event
async def on_ready():
    print(f"🤖 Bot conectado como {bot.user}!")
    
    # Carrega os comandos dos cogs
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            try:
                await bot.load_extension(f"cogs.{filename[:-3]}")
                print(f"✅ Cog carregado: cogs.{filename[:-3]}")
            except Exception as e:
                print(f"❌ Erro ao carregar cogs.{filename[:-3]}: {e}")
    
    # Sincroniza os comandos com o Discord
    await tree.sync()
    print("🌐 Comandos sincronizados.")

bot.run(TOKEN)
