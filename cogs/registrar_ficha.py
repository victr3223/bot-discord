import discord
from discord.ext import commands
from discord import app_commands
import json
import os

FICHAS_PATH = "dados/fichas.json"

class RegistrarFicha(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="registrar_ficha", description="Registra o canal atual como ficha do seu usuário.")
    async def registrar_ficha(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        channel_id = interaction.channel.id

        if not os.path.exists(FICHAS_PATH):
            with open(FICHAS_PATH, "w") as f:
                json.dump({}, f)

        with open(FICHAS_PATH, "r") as f:
            fichas = json.load(f)

        if user_id in fichas:
            await interaction.response.send_message("❌ Você já registrou sua ficha. Use /apagar_ficha para remover o registro anterior.", ephemeral=True)
            return

        fichas[user_id] = channel_id

        with open(FICHAS_PATH, "w") as f:
            json.dump(fichas, f, indent=4)

        await interaction.response.send_message(f"✅ Ficha registrada no nome do {interaction.user.mention}!", ephemeral=False)

    @app_commands.command(name="apagar_ficha", description="Apaga o registro da sua ficha.")
    async def apagar_ficha(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)

        if not os.path.exists(FICHAS_PATH):
            await interaction.response.send_message("❌ Nenhuma ficha registrada ainda.", ephemeral=True)
            return

        with open(FICHAS_PATH, "r") as f:
            fichas = json.load(f)

        if user_id not in fichas:
            await interaction.response.send_message("❌ Você não possui uma ficha registrada.", ephemeral=True)
            return

        del fichas[user_id]

        with open(FICHAS_PATH, "w") as f:
            json.dump(fichas, f, indent=4)

        await interaction.response.send_message("✅ Sua ficha foi apagada com sucesso.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(RegistrarFicha(bot))
# Código atualizado do comando registrar_ficha.py