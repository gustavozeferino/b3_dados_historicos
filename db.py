
import sqlite3
import csv

def consultar_banco(caminho_banco, consulta_sql, parametros=None):
    try:
        # Conectar ao banco de dados SQLite
        conexao = sqlite3.connect(caminho_banco)
        cursor = conexao.cursor()

        # Executar consulta com ou sem parâmetros
        if parametros:
            cursor.execute(consulta_sql, parametros)
        else:
            cursor.execute(consulta_sql)
        
        # Obter os resultados
        resultados = cursor.fetchall()
        return resultados
    
    except sqlite3.Error as e:
        print(f"Erro ao consultar o banco: {e}")
        return None


def importar_csv_para_sqlite(caminho_arquivo_csv, caminho_banco, nome_tabela):
    """
    Importa dados de um arquivo CSV para uma tabela SQLite.

    :param caminho_arquivo_csv: Caminho do arquivo CSV
    :param caminho_banco: caminho do banco SQLite
    :param nome_tabela: Nome da tabela onde os dados serão inseridos
    """
    try:
        # Conectar ao banco de dados SQLite
        conexao = sqlite3.connect(caminho_banco)
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


def criar_datas_vencimento(caminho_banco):
    """
    Cria uma tabela com as datas de vencimento de opções excluindo opções de IBOV e datas inválidas.

    :param caminho_banco: caminho do banco SQLite
    """
    try:
        # Conectar ao banco de dados SQLite
        conexao = sqlite3.connect(caminho_banco)
        cursor = conexao.cursor()
        
        cursor.execute(f""" DROP TABLE IF EXISTS datas_vencimento""")
        cursor.execute(f"""
            CREATE TABLE datas_vencimento AS select distinct DATVEN as DATA
            from cotacoes_historicas
            where strftime('%Y', DATVEN) <> '9999' AND CODNEG NOT LIKE 'IBOV%'
            ORDER BY DATVEN
        """)
        
        # Confirmar a operação
        conexao.commit()
        print(f"Tabela datas_vencimento criada com sucesso.")
    
    except sqlite3.Error as e:
        print(f"Erro ao trabalhar com o banco de dados: {e}")
    
    except Exception as e:
        print(f"Erro inesperado: {e}")
    
    finally:
        # Fechar a conexão com o banco
        if conexao:
            conexao.close()
            print("Conexão com o banco de dados encerrada.")


def criar_datas_pregao(caminho_banco):
    """
    Cria uma tabela com as datas de pregão.

    :param caminho_banco: caminho do banco SQLite
    """
    try:
        # Conectar ao banco de dados SQLite
        conexao = sqlite3.connect(caminho_banco)
        cursor = conexao.cursor()

        cursor.execute(f""" DROP TABLE IF EXISTS datas_pregao""")        
        cursor.execute(f"""
            CREATE TABLE datas_pregao AS select distinct DTPREG as DATA
            from cotacoes_historicas
            ORDER BY DTPREG
        """)
        
        # Confirmar a operação
        conexao.commit()
        print(f"Tabela datas_pregao criada com sucesso.")
    
    except sqlite3.Error as e:
        print(f"Erro ao trabalhar com o banco de dados: {e}")
    
    except Exception as e:
        print(f"Erro inesperado: {e}")
    
    finally:
        # Fechar a conexão com o banco
        if conexao:
            conexao.close()
            print("Conexão com o banco de dados encerrada.")


def criar_tabela_ativos_com_opcoes(caminho_banco, tabela_original="cotacoes_historicas", tabela_destino="ativos_com_opcoes"):
    """
    Cria uma tabela com o CODNEG e ISIN únicos dos ativos que possuem opções negoaciadas

    :param caminho_banco: caminho do banco SQLite
    :param tabela_original: tabela com o historico de cotações
    :param tabela_destino: tabela dos ativos com opções
    """
    try:
        # Conectar ao banco de dados SQLite
        conexao = sqlite3.connect(caminho_banco)
        cursor = conexao.cursor()

        cursor.execute(f""" DROP TABLE IF EXISTS {tabela_destino}""")        

        cursor.execute(f"""
            CREATE TABLE {tabela_destino} AS SELECT DISTINCT CODNEG, CODISI
            FROM {tabela_original}
            WHERE   CODISI IN (SELECT DISTINCT CODISI FROM {tabela_original} WHERE TPMERC IN ('070', '080'))
                    AND TPMERC = '010'
            ORDER BY CODNEG""")
        
        # Confirmar a operação
        conexao.commit()
        print(f"Tabela {tabela_destino} criada com sucesso.")
    
    except sqlite3.Error as e:
        print(f"Erro ao trabalhar com o banco de dados: {e}")
    
    except Exception as e:
        print(f"Erro inesperado: {e}")
    
    finally:
        # Fechar a conexão com o banco
        if conexao:
            conexao.close()
            print("Conexão com o banco de dados encerrada.")


def criar_tabela_cotacao_bova11(caminho_banco, tabela_original, tabela_final):
    """
    Cria uma tabela com as cotações de BOVA11 apenas.

    :param caminho_banco: caminho do banco SQLite
    """
    try:
        # Conectar ao banco de dados SQLite
        conexao = sqlite3.connect(caminho_banco)
        cursor = conexao.cursor()

        cursor.execute(f""" DROP TABLE IF EXISTS {tabela_final}""")        
        cursor.execute(f"""
            CREATE TABLE {tabela_final} AS SELECT DTPREG, CODNEG, PREABE, PREMIN, PREMAX, PREULT, QUATOT
            FROM {tabela_original}
            WHERE   CODNEG  = 'BOVA11'
                    AND TPMERC = '010'
            """)
        
        # Confirmar a operação
        conexao.commit()
        print(f"Tabela {tabela_final} criada com sucesso.")
    
    except sqlite3.Error as e:
        print(f"Erro ao trabalhar com o banco de dados: {e}")
    
    except Exception as e:
        print(f"Erro inesperado: {e}")
    
    finally:
        # Fechar a conexão com o banco
        if conexao:
            conexao.close()
            print("Conexão com o banco de dados encerrada.")



def criar_tabela_opcoes_ativos(caminho_banco, tabela_cotacoes="cotacoes_historicas", tabela_final="pregao_opcoes", ativo="BOVA11"):  

    """
    Cria uma tabela com as opções de ativos apenas.

    :param caminho_banco: caminho do banco SQLite
    """
    try:
        # Conectar ao banco de dados SQLite
        conexao = sqlite3.connect(caminho_banco)
        cursor = conexao.cursor()


        cursor.execute(f"""
            DROP TABLE IF EXISTS temp_cotacoes_opcoes
        """)        
        
        cursor.execute(f"""
            CREATE TABLE temp_cotacoes_opcoes AS SELECT * 
            FROM {tabela_cotacoes} 
            WHERE   CODISI IN (SELECT CODISI FROM ativos_com_opcoes WHERE CODNEG = '{ativo}')
                    AND TPMERC IN ('070', '080')
        """)        

        cursor.execute(f"""
            DROP TABLE IF EXISTS {tabela_final}
        """)        

        cursor.execute(f"""
            CREATE TABLE {tabela_final} (
                DTPREG TEXT,
                ATIVO TEXT,
                CODISI TEXT,
                DATVEN TEXT,
                PREEXE REAL,
                TIPO TEXT,
                CODNEG TEXT,
                PREULT REAL,
                PRIMARY KEY (DTPREG, ATIVO, DATVEN, PREEXE, CODNEG))
        """)     

        cursor.execute(f"""
            INSERT INTO {tabela_final} (DTPREG, ATIVO, CODISI, DATVEN, PREEXE, TIPO, CODNEG, PREULT)
            SELECT DISTINCT
                cotacoes.DTPREG,
                ativos.CODNEG,
                cotacoes.CODISI,
                cotacoes.DATVEN,
                cotacoes.PREEXE,
                CASE 
                    WHEN cotacoes.TPMERC = '070' THEN 'CALL'
                    WHEN cotacoes.TPMERC = '080' THEN 'PUT'
                END AS TIPO,
                cotacoes.CODNEG,
                cotacoes.PREULT
            FROM temp_cotacoes_opcoes AS cotacoes
            INNER JOIN ativos_com_opcoes AS ativos ON cotacoes.CODISI = ativos.CODISI
        """)             

        cursor.execute(f"""
            DROP TABLE IF EXISTS temp_cotacoes_opcoes
        """)             

        cursor.execute(f"""

        """)             

        # Confirmar a operação
        conexao.commit()
        print(f"Tabela {tabela_final} criada com sucesso.")
    
    except sqlite3.Error as e:
        print(f"Erro ao trabalhar com o banco de dados: {e}")
    
    except Exception as e:
        print(f"Erro inesperado: {e}")
    
    finally:
        # Fechar a conexão com o banco
        if conexao:
            conexao.close()
            print("Conexão com o banco de dados encerrada.")
