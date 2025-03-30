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
                "lucro": None }
            
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

# Exemplo de uso da classe
portfolio = Portfolio()

# Adicionando posições
portfolio.add_position("2025-03-28", "AAPL", 10, 150.00)
portfolio.add_position("2025-03-28", "MSFT", 5, 300.00)
portfolio.add_position("2025-03-29", "GOOG", 8, 2800.00)

# Removendo uma posição
portfolio.remove_position("2025-03-28", "AAPL")

# Recuperando informações
print(portfolio.get_positions("2025-03-28"))
print("Total Value:", portfolio.get_total_value("2025-03-28"))

# Exibindo todo o histórico da simulação
portfolio.display_simulation()