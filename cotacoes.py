import db
import pandas as pd



def grade_opcoes(data_pregao, data_vencimento):
    """
    Função para criar uma grade de opções com base na data de pregão e data de vencimento.

    :param data_pregao: Data de pregão no formato 'YYYY-MM-DD'.
    :param data_vencimento: Data de vencimento no formato 'YYYY-MM-DD'.
    :return: DataFrame com as opções disponíveis. Se não houver opções disponíveis, retorna None.
    """

    consulta_sql = f"""SELECT * from pregao_opcoes_bova11 WHERE DTPREG = ? AND DATVEN = ?"""
    resultado_consulta = db.consultar_banco(database_path, consulta_sql, [data_pregao, data_vencimento])
    if resultado_consulta:
        df = pd.DataFrame(resultado_consulta, columns=["DTPREG", "ATIVO", "CODISI", "DATVEN", "PREEXE", "TIPO", "CODNEG", "PREULT"])
        # Criando o DataFrame para TIPO == 'CALL'
        df_call = df[df['TIPO'] == 'CALL'][['PREEXE', 'CODNEG', 'PREULT']].copy()
        df_call = df_call.rename(columns={'CODNEG': 'CALL', 'PREULT': 'PRECO_CALL'})
        df_call.set_index('PREEXE', inplace=True)

        # Criando o DataFrame para TIPO == 'PUT'
        df_put = df[df['TIPO'] == 'PUT'][['PREEXE', 'CODNEG', 'PREULT']].copy()
        df_put = df_put.rename(columns={'CODNEG': 'PUT', 'PREULT': 'PRECO_PUT'})
        df_put.set_index('PREEXE', inplace=True)

        # Combinando os dois DataFrames usando PREEXE como índice
        df_combined = pd.merge(df_call, df_put, on='PREEXE', how='outer')

        return df_combined
    else:
        print(f"Nenhuma opção encontrada para a data de pregão {data_pregao} e data de vencimento {data_vencimento}.")
        return None
