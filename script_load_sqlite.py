import yaml
from db import importar_csv_para_sqlite

if __name__ == "__main__":
    # Carregar configurações do arquivo YAML
    with open("config.yml", "r") as config_file:
        config = yaml.safe_load(config_file)

    # Obter configurações do SQLite
    db_config = config["sqlite"]
    database_path = db_config["database_path"]
    timeout = db_config.get("timeout", 5)  # Valor padrão de 5 segundos

    # Obter configurações do arquivo CSV
    csv_files = config["csv_files"]
    for csv_file in csv_files:
        csv_path = csv_file["path"]
        print(f"Processando: {csv_path}")
        importar_csv_para_sqlite(csv_path, database_path, "cotacoes_historicas")