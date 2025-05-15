import discord
from discord.ext import commands
from discord import app_commands
import json
import os
from utils.permissoes import is_mestre
from utils.caminhos import CAMINHO_ENCICLOPEDIA, CAMINHO_MONSTROS, FICHAS_PATH


def carregar_json(caminho, padrao):
    if not os.path.exists(caminho):
        return padrao
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)


def salvar_json(caminho, dados):
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)


class Enciclopedia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="registrar_enciclopedia", description="Mestre registra um monstro na enciclopédia de um jogador.")
    @app_commands.describe(
        monstro="Nome do monstro",
        descricao="Descrição do monstro",
        usuario="Jogador que vai receber o monstro",
        imagem="Imagem do monstro (anexo)"
    )
    async def registrar_enciclopedia(
        self,
        interaction: discord.Interaction,
        monstro: str,
        descricao: str,
        usuario: discord.Member,
        imagem: discord.Attachment
    ):
        if not is_mestre(interaction.user):
            await interaction.response.send_message("❌ Apenas o Mestre pode usar este comando.", ephemeral=True)
            return

        if not imagem.content_type.startswith("image/"):
            await interaction.response.send_message("❌ O anexo precisa ser uma imagem.", ephemeral=True)
            return

        imagem_url = imagem.url
        user_id = str(usuario.id)

        enciclopedia = carregar_json(CAMINHO_ENCICLOPEDIA, {})
        monstros_info = carregar_json(CAMINHO_MONSTROS, {})

        if user_id not in enciclopedia:
            enciclopedia[user_id] = []

        if monstro not in enciclopedia[user_id]:
            enciclopedia[user_id].append(monstro)
            salvar_json(CAMINHO_ENCICLOPEDIA, enciclopedia)
        else:
            await interaction.response.send_message(f"{usuario.mention} já tem **{monstro}** na enciclopédia.", ephemeral=True)
            return

        monstros_info[monstro] = {
            "descricao": descricao,
            "imagem": imagem_url
        }
        salvar_json(CAMINHO_MONSTROS, monstros_info)

        await interaction.response.send_message(
            f"✅ Monstro **{monstro}** registrado na enciclopédia de {usuario.mention}.",
            ephemeral=True
        )

    @app_commands.command(name="enciclopedia", description="Veja sua enciclopédia de monstros.")
    async def enciclopedia(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        enciclopedia = carregar_json(CAMINHO_ENCICLOPEDIA, {})
        monstros_info = carregar_json(CAMINHO_MONSTROS, {})
        fichas = carregar_json(FICHAS_PATH, {})

        if user_id not in enciclopedia or not enciclopedia[user_id]:
            await interaction.response.send_message("📖 Sua enciclopédia está vazia.", ephemeral=True)
            return

        canal_id = fichas.get(user_id)
        if canal_id is None:
            await interaction.response.send_message("❌ Você não possui uma ficha registrada.", ephemeral=True)
            return

        canal = self.bot.get_channel(canal_id)
        if canal is None:
            await interaction.response.send_message("❌ Canal da ficha não encontrado.", ephemeral=True)
            return

        paginas = []
        for monstro in enciclopedia[user_id]:
            info = monstros_info.get(monstro, {})
            embed = discord.Embed(
                title=f"📖 {monstro}",
                description=info.get("descricao", "Sem descrição."),
                color=discord.Color.green()
            )
            if "imagem" in info:
                embed.set_image(url=info["imagem"])
            paginas.append(embed)

        # Enviar páginas uma por uma com botões (paginação)
        class Paginador(discord.ui.View):
            def __init__(self, embeds):
                super().__init__(timeout=60)
                self.embeds = embeds
                self.index = 0
                self.msg = None

            @discord.ui.button(label="⬅️", style=discord.ButtonStyle.secondary)
            async def anterior(self, interaction_btn: discord.Interaction, _):
                if interaction_btn.user != interaction.user:
                    return
                self.index = (self.index - 1) % len(self.embeds)
                await interaction_btn.response.edit_message(embed=self.embeds[self.index], view=self)

            @discord.ui.button(label="➡️", style=discord.ButtonStyle.secondary)
            async def proximo(self, interaction_btn: discord.Interaction, _):
                if interaction_btn.user != interaction.user:
                    return
                self.index = (self.index + 1) % len(self.embeds)
                await interaction_btn.response.edit_message(embed=self.embeds[self.index], view=self)

        view = Paginador(paginas)
        msg = await canal.send(embed=paginas[0], view=view)
        await interaction.response.send_message("📖 Enciclopédia enviada para seu canal de ficha.", ephemeral=True)

        # Apagar após 1 minuto
        await msg.delete(delay=60)

    @app_commands.command(name="remover_monstro", description="Mestre remove um monstro da enciclopédia de um jogador.")
    @app_commands.describe(
        monstro="Nome do monstro a remover",
        usuario="Jogador que perderá o monstro"
    )
    async def remover_monstro(self, interaction: discord.Interaction, monstro: str, usuario: discord.Member):
        if not is_mestre(interaction.user):
            await interaction.response.send_message("❌ Apenas o Mestre pode usar este comando.", ephemeral=True)
            return

        user_id = str(usuario.id)
        enciclopedia = carregar_json(CAMINHO_ENCICLOPEDIA, {})

        if user_id in enciclopedia and monstro in enciclopedia[user_id]:
            enciclopedia[user_id].remove(monstro)
            salvar_json(CAMINHO_ENCICLOPEDIA, enciclopedia)
            await interaction.response.send_message(f"🗑️ Monstro **{monstro}** removido da enciclopédia de {usuario.mention}.", ephemeral=True)
        else:
            await interaction.response.send_message(f"❌ O monstro **{monstro}** não está na enciclopédia de {usuario.mention}.", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Enciclopedia(bot))
