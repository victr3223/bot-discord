import os

# Caminho para a pasta de dados
PASTA_DADOS = "dados"

# Garante que a pasta existe
os.makedirs(PASTA_DADOS, exist_ok=True)

# Caminhos dos arquivos JSON
FICHAS_PATH = os.path.join(PASTA_DADOS, "fichas.json")
INVENTARIOS_PATH = os.path.join(PASTA_DADOS, "inventarios.json")
ENCICLOPEDIAS_PATH = os.path.join(PASTA_DADOS, "enciclopedia.json")
CAMINHO_ENCICLOPEDIA = "dados/enciclopedia.json"
CAMINHO_MONSTROS = "dados/monstros.json"