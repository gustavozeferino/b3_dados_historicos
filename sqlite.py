import sqlite3

# Conexão com o banco de dados (será criado se não existir)
conexao = sqlite3.connect("cotacoes_historicas.db")
cursor = conexao.cursor()

# Criando a tabela
cursor.execute("""
CREATE TABLE IF NOT EXISTS cotacoes_historicas (
    TIPREG TEXT,
    DTPREG DATE,
    CODBDI TEXT,
    CODNEG TEXT,
    TPMERC TEXT,
    NOMRES TEXT,
    ESPECI TEXT,
    PRAZOT TEXT,
    MODREF TEXT,
    PREABE REAL,
    PREMAX REAL,
    PREMIN REAL,
    PREMED REAL,
    PREULT REAL,
    PREOFC REAL,
    PREOFV REAL,
    TOTNEG INTEGER,
    QUATOT INTEGER,
    VOLTOT REAL,
    PREEXE REAL,
    INDOPC TEXT,
    DATVEN DATE,
    FATCOT TEXT,
    PTOEXE TEXT,
    CODISI TEXT,
    DISMES TEXT
)
""")
print("Tabela criada com sucesso!")

# Salvar alterações e fechar a conexão
conexao.commit()
conexao.close()

import sqlite3
import csv

def importar_csv_para_sqlite(caminho_arquivo_csv, nome_banco, nome_tabela):
    """
    Importa dados de um arquivo CSV para uma tabela SQLite.

    :param caminho_arquivo_csv: Caminho do arquivo CSV
    :param nome_banco: Nome do banco SQLite
    :param nome_tabela: Nome da tabela onde os dados serão inseridos
    """
    try:
        # Conectar ao banco de dados SQLite
        conexao = sqlite3.connect(nome_banco)
        cursor = conexao.cursor()
        
        # Garantir que a tabela existe (ajustar estrutura conforme necessário)
        cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {nome_tabela} (
            TIPREG TEXT,
            DTPREG DATE,
            CODBDI TEXT,
            CODNEG TEXT,
            TPMERC TEXT,
            NOMRES TEXT,
            ESPECI TEXT,
            PRAZOT TEXT,
            MODREF TEXT,
            PREABE REAL,
            PREMAX REAL,
            PREMIN REAL,
            PREMED REAL,
            PREULT REAL,
            PREOFC REAL,
            PREOFV REAL,
            TOTNEG INTEGER,
            QUATOT INTEGER,
            VOLTOT REAL,
            PREEXE REAL,
            INDOPC TEXT,
            DATVEN DATE,
            FATCOT TEXT,
            PTOEXE TEXT,
            CODISI TEXT,
            DISMES TEXT
        );
        """)
        print(f"Tabela '{nome_tabela}' criada ou já existente.")
        
        # Abrir o arquivo CSV
        with open(caminho_arquivo_csv, mode='r', encoding='utf-8') as arquivo:
            leitor_csv = csv.reader(arquivo)
            # Pular o cabeçalho do CSV
            # next(leitor_csv)
            
            # Inserir os dados na tabela
            cursor.executemany(f"""
            INSERT INTO {nome_tabela} (
                TIPREG, DTPREG, CODBDI, CODNEG, TPMERC, NOMRES, ESPECI, PRAZOT, MODREF, PREABE,
                PREMAX, PREMIN, PREMED, PREULT, PREOFC, PREOFV, TOTNEG, QUATOT, VOLTOT, PREEXE,
                INDOPC, DATVEN, FATCOT, PTOEXE, CODISI, DISMES
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, leitor_csv)
        
        # Confirmar a operação
        conexao.commit()
        print(f"Dados do arquivo '{caminho_arquivo_csv}' importados com sucesso para a tabela '{nome_tabela}'.")
    
    except sqlite3.Error as e:
        print(f"Erro ao trabalhar com o banco de dados: {e}")
    
    except Exception as e:
        print(f"Erro inesperado: {e}")
    
    finally:
        # Fechar a conexão com o banco
        if conexao:
            conexao.close()
            print("Conexão com o banco de dados encerrada.")

# Exemplo de uso da função
importar_csv_para_sqlite("dados.csv", "banco_dados.db", "cotacoes_historicas")
