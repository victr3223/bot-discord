import discord
from discord.ext import commands
from discord import app_commands
import json
import os
from utils.caminhos import FICHAS_PATH, INVENTARIOS_PATH
from utils.permissoes import is_mestre

class Inventario(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def carregar_fichas(self):
        if not os.path.exists(FICHAS_PATH):
            return {}
        with open(FICHAS_PATH, "r") as f:
            return json.load(f)

    def carregar_inventarios(self):
        if not os.path.exists(INVENTARIOS_PATH):
            return {}
        with open(INVENTARIOS_PATH, "r") as f:
            return json.load(f)

    def salvar_inventarios(self, inventarios):
        with open(INVENTARIOS_PATH, "w") as f:
            json.dump(inventarios, f, indent=4)

    @app_commands.command(name="inventario", description="Exibe seu inventário ou o de outro jogador (apenas para o Mestre).")
    @app_commands.describe(usuario="(Opcional) Jogador cujo inventário será exibido")
    async def inventario(self, interaction: discord.Interaction, usuario: discord.User = None):
        fichas = self.carregar_fichas()
        inventarios = self.carregar_inventarios()

        solicitante = interaction.user
        is_mestre_user = is_mestre(solicitante)

        # Determinar de quem é o inventário
        if usuario and is_mestre_user:
            alvo = usuario
        elif usuario and not is_mestre_user:
            await interaction.response.send_message("❌ Apenas o Mestre pode ver o inventário de outro jogador.", ephemeral=True)
            return
        else:
            alvo = solicitante

        id_alvo = str(alvo.id)
        inventario_usuario = inventarios.get(id_alvo, [])
        canal_id = fichas.get(id_alvo)

        if canal_id is None:
            await interaction.response.send_message("❌ Este usuário ainda não tem uma ficha registrada.", ephemeral=True)
            return

        canal = self.bot.get_channel(int(canal_id))
        if canal is None:
            await interaction.response.send_message("❌ Canal da ficha não encontrado.", ephemeral=True)
            return

        if not inventario_usuario:
            conteudo = "*Este inventário está vazio.*"
        else:
            conteudo = "\n".join(f"{i+1}. {item}" for i, item in enumerate(inventario_usuario))

        embed = discord.Embed(
            title=f"🎒 Inventário de {alvo.display_name}",
            description=conteudo,
            color=discord.Color.blue()
        )

        await interaction.response.send_message("✅ Inventário enviado para o canal da ficha.", ephemeral=True)
        msg = await canal.send(embed=embed)
        await msg.delete(delay=60)

async def setup(bot):
    await bot.add_cog(Inventario(bot))
