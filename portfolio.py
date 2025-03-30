import pandas as pd


class Portfolio:
    def __init__(self):
        # Inicializa o dicionário para armazenar os dados da simulação
        self.portfolio = {}
        self.historico = {}
    
    def adiciona_posicao(self, data_pregao, opcao, data_vencimento, lote, preco):
        """
        Adiciona ou atualiza uma posição na data especificada.
        """
        if data_pregao not in self.portfolio:
            self.portfolio[data_pregao] = {
                "posicoes": {},
                "valor_total": 0
            }
        
        # Calcula o valor da posição
        valor_posicao = lote * preco
        
        # Adiciona ou atualiza os dados da posição
        chave_posicao = (opcao, data_vencimento)

        self.portfolio[data_pregao]["posicoes"][chave_posicao] = {
            "lote": lote,
            "preco": preco,
            "valor": valor_posicao
        }

        # Adiciona a posição ao histórico
        if chave_posicao not in self.historico:
            self.historico[chave_posicao] = {
                "data_abertura": None,
                "data_fechamento": None,
                "lote": None,
                "preco_compra": None,
                "preco_venda": None,
                "lucro": None,
                "status": "Aberto" }
            
        # Atualiza o histórico
        self.historico[chave_posicao]["data_abertura"] = data_pregao
        self.historico[chave_posicao]["lote"] = lote
        if lote > 0:
            self.historico[chave_posicao]["preco_compra"] = preco
        else:
            self.historico[chave_posicao]["preco_venda"] = preco
        
        # Atualiza o valor total das posições
        self.portfolio[data_pregao]["valor_total"] = sum(
            position["valor"] for position in self.portfolio[data_pregao]["posicoes"].values()
        )
    
    def remove_posicao(self, data_pregao, opcao, data_vencimento, preco):
        """
        Remove uma posição específica na data especificada.
        """
        chave_posicao = (opcao, data_vencimento)

        if data_pregao in self.portfolio and chave_posicao in self.portfolio[data_pregao]["posicoes"]:
            del self.portfolio[data_pregao]["posicoes"][chave_posicao]
            # Atualiza o valor total das posições
            self.portfolio[data_pregao]["total_value"] = sum(
                position["valor"] for position in self.portfolio[data_pregao]["posicoes"].values()
            )

        # Atualiza o historico de operações
        if chave_posicao in self.historico:
            self.historico[chave_posicao]["data_fechamento"] = data_pregao
            if self.historico[chave_posicao]["lote"] > 0:
                self.historico[chave_posicao]["preco_venda"] = preco
            else:
                self.historico[chave_posicao]["preco_compra"] = preco                

            self.historico[chave_posicao]['lucro'] = abs(self.historico[chave_posicao]["lote"]) * (self.historico[chave_posicao]["preco_venda"] - self.historico[chave_posicao]["preco_compra"])         
            self.historico[chave_posicao]['status'] = "Fechado"

    def posicoes(self, data_pregao):
        """
        Retorna todas as posições para uma data específica.
        """
        if data_pregao in self.portfolio:
            return self.portfolio[data_pregao]["posicoes"]
        return None
    
    def valor_total(self, data_pregao):
        """
        Retorna o valor total das posições para uma data específica.
        """
        if data_pregao in self.portfolio:
            return self.portfolio[data_pregao]["valor_total"]
        return 0
    
    def historico_valor(self):
        """
        Exibe todo o histórico da simulação.
        """
        for data_pregao, dados in self.portfolio.items():
            print(f"{data_pregao}: {dados['valor_total']}")

    def posicoes_fechadas(self):
        dados = []
        for chave_posicao, dados_posicao in self.historico.items():
            if dados_posicao["status"] == "Fechado":
                dados.append([chave_posicao, dados_posicao['data_abertura'], dados_posicao['data_fechamento'], dados_posicao['lote'], dados_posicao['preco_compra'], dados_posicao['preco_venda'], dados_posicao['lucro']])

        if dados:
            # Cria um DataFrame a partir dos dados
            df = pd.DataFrame(dados, columns=["Opção", "Data Abertura", "Data Fechamento", "Lote", "Preço Compra", "Preço Venda", "L/P"])
            # Exibe o DataFrame formatado
            print(df.to_string(index=False))
        else:
            print("Nenhuma posição fechada encontrada.")

    def copia_posicoes(self, data_pregao_origem, data_pregao_destino):
        """
        Copia as posições de uma data de origem para uma data de destino.
        """
        if data_pregao_origem in self.portfolio:
            self.portfolio[data_pregao_destino] = self.portfolio[data_pregao_origem].copy()
                