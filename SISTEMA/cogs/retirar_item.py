import discord
from discord.ext import commands
from discord import app_commands
import json
import os
from utils.caminhos import INVENTARIOS_PATH
from utils.permissoes import is_mestre

class RetirarItem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def carregar_inventarios(self):
        if not os.path.exists(INVENTARIOS_PATH):
            return {}
        with open(INVENTARIOS_PATH, "r") as f:
            return json.load(f)

    def salvar_inventarios(self, inventarios):
        with open(INVENTARIOS_PATH, "w") as f:
            json.dump(inventarios, f, indent=4)

    @app_commands.command(name="retirar_item", description="Remove um item do seu inventário ou do inventário de outro jogador (mestre).")
    @app_commands.describe(item="Número ou nome do item", usuario="Jogador alvo (apenas mestre)")
    async def retirar_item(self, interaction: discord.Interaction, item: str, usuario: discord.User = None):
        inventarios = self.carregar_inventarios()

        autor = interaction.user
        alvo = usuario if usuario and is_mestre(autor) else autor
        id_alvo = str(alvo.id)

        if id_alvo not in inventarios or not inventarios[id_alvo]:
            await interaction.response.send_message("❌ Este usuário não possui inventário.", ephemeral=True)
            return

        inventario = inventarios[id_alvo]

        # Tenta converter item para número
        try:
            index = int(item) - 1
            if index < 0 or index >= len(inventario):
                raise IndexError
            item_removido = inventario.pop(index)
        except ValueError:
            # Se não for número, tenta remover pelo nome
            if item in inventario:
                inventario.remove(item)
                item_removido = item
            else:
                await interaction.response.send_message("❌ Item não encontrado no inventário.", ephemeral=True)
                return
        except IndexError:
            await interaction.response.send_message("❌ Número inválido.", ephemeral=True)
            return

        inventarios[id_alvo] = inventario
        self.salvar_inventarios(inventarios)

        await interaction.response.send_message(f"🗑️ Item removido: `{item_removido}` de {alvo.display_name}.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(RetirarItem(bot))
