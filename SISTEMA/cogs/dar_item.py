import discord
from discord.ext import commands
from discord import app_commands
import json
import os
from config import ID_MESTRE

INVENTARIOS_PATH = "dados/inventarios.json"

class DarItem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="dar_item", description="Mestre dá um item a um jogador.")
    @app_commands.describe(item="Nome do item", usuario="Usuário que receberá o item")
    async def dar_item(self, interaction: discord.Interaction, item: str, usuario: discord.Member):
        if interaction.user.id != ID_MESTRE:
            await interaction.response.send_message("❌ Apenas o mestre pode conceder itens.", ephemeral=True)
            return

        user_id = str(usuario.id)

        if not os.path.exists(INVENTARIOS_PATH):
            with open(INVENTARIOS_PATH, "w") as f:
                json.dump({}, f)

        with open(INVENTARIOS_PATH, "r") as f:
            inventarios = json.load(f)

        inventarios.setdefault(user_id, []).append(item)

        with open(INVENTARIOS_PATH, "w") as f:
            json.dump(inventarios, f, indent=4)

        await interaction.response.send_message(f"✅ {item} foi adicionado ao inventário de {usuario.mention}.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(DarItem(bot))
    # Código atualizado do comando dar_item.py