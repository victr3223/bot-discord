import os

# Tenta pegar o token do ambiente (Railway ou outros)
TOKEN = os.getenv("DISCORD_TOKEN")

# Se não encontrar no ambiente, tenta carregar de um arquivo local (apenas no desenvolvimento)
if not TOKEN:
    try:
        from secrets import LOCAL_TOKEN
        TOKEN = LOCAL_TOKEN
    except ImportError:
        raise RuntimeError("❌ Token do Discord não encontrado! Configure DISCORD_TOKEN ou secrets.py")

ID_MESTRE = 1195510333419290665
