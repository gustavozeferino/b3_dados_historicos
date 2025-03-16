from datetime import datetime
import tkinter as tk
from tkinter import filedialog
import csv

class InvalidFormatException(Exception):
    """Primeira linha do arquivo está fora do padrão da B3."""
    pass

def select_file():
    """Open a dialog to select an input text file."""
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    input_file = filedialog.askopenfilename(
        title="Selecione o arquivos de dados fornecido pela B3",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    return input_file

def save_file():
    """Open a dialog to specify the save location for a new file."""
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    save_path = filedialog.asksaveasfilename(
        title="Onde você deseja salvar o arquivo CSV?",
        defaultextension=".csv",
        filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
    )
    return save_path

def convert_to_csv(input_file, output_file):
    """Convert the input text file to a CSV file."""

# Abrir o arquivo de entrada (para leitura) e o arquivo de saída (para escrita)
    try:
        with open(input_file, mode="r", encoding="utf-8") as input_data, \
            open(output_file, mode="w", newline="", encoding="utf-8") as output_data:
            
            reader = csv.reader(input_data)  # Criar leitor do CSV
            writer = csv.writer(output_data)  # Criar escritor do CSV

            fisrt_line = next(reader, None)
            if not check_file_header(fisrt_line):
                raise InvalidFormatException

            # Ler e processar cada linha
            for line in reader:
                if line[0:2] == '00':
                    csv_line = processed_data(line)
                    # Escrever a linha imediatamente no arquivo de saída
                    writer.writerow(csv_line)

    except InvalidFormatException as e:
        print(e)
    except FileNotFoundError:
        print("Arquivo de entrada não encontrado.")
    except Exception as e:
        print(f"Erro inesperado: {e}")
    

def check_file_header(data):
    """Check if the first line of the data is a header."""
    TIPO_DE_REGISTRO = data[0:2]
    NOME_DO_ARQUIVO = data[2:15]
    CODIGO_DA_ORIGEM = data[15:23]
    DATA_DA_GERAÇAO_DO_ARQUIVO = data[23:31]
    RESERVA = data[31:245]

    if TIPO_DE_REGISTRO == '00' and CODIGO_DA_ORIGEM == 'BOVESPA ':
        return True
    else:
        return False

def processed_data(data):
    """Processamento dos dados de negociação."""
    TIPREG=data[0:2]                                         # Tipo de registro
    DTPREG=datetime.strptime(data[2:10], "%Y%m%d").date()    # Data do pregão
    CODBDI=data[10:12]                                       # Código BDI  
    CODNEG=(data[12:24]).strip()                             # Código de negociação do papel
    TPMERC=data[24:27]                                       # Tipo de mercado
    NOMRES=(data[27:39]).strip()                             # Nome resumido da empresa emissora do papel
    ESPECI=(data[39:49]).strip()                             # Especificação do papel
    PRAZOT=(data[49:52]).strip()                             # Prazo em dias do mercado a termo
    MODREF=(data[52:56]).strip()                             # Moeda de referência
    PREABE=float(data[56:69])/100                            # Preço de abertura
    PREMAX=float(data[69:82])/100                            # Preço máximo
    PREMIN=float(data[82:95])/100                            # Preço mínimo
    PREMED=float(data[95:108])/100                           # Preço médio
    PREULT=float(data[108:121])/100                          # Preço do último negócio
    PREOFC=float(data[121:134])/100                          # Preço da melhor oferta de compra
    PREOFV=float(data[134:147])/100                          # Preço da melhor oferta de venda
    TOTNEG=int(data[147:152])                                # Número de negócios efetuados
    QUATOT=int(data[152:170])                                # Quantidade total de títulos negociados
    VOLTOT=float(data[170:188])                              # Volume total de títulos negociados
    PREEXE=float(data[188:201])/100                          # Preço de exercício para opções
    INDOPC=data[201:202]                                     # Indicador de correção de preços
    DATVEN=datetime.strptime(data[202:210], '%Y%m%d').date() # Data do vencimento para opções
    FATCOT=data[210:217]                                     # Fator de cotação do papel
    PTOEXE=data[217:230]                                     # Preço de exercício para opções refer
    CODISI=data[230:242]                                     # Código do papel no sistema ISIN ou código interno do papel
    DISMES=data[242:245]                                     # Número de distribuição do papel
    
    processed_data = [TIPREG, DTPREG, CODBDI, CODNEG, TPMERC, NOMRES, ESPECI, PRAZOT, MODREF, PREABE, PREMAX, PREMIN, PREMED, PREULT, PREOFC, PREOFV, TOTNEG, QUATOT, VOLTOT, PREEXE, INDOPC, DATVEN, FATCOT, PTOEXE, CODISI, DISMES]
    return processed_data




if __name__ == "__main__":
    # Step 1: Select the input file
    input_file = select_file()
    if input_file:
        print(f"Arquivo de dados selecionado: {input_file}")
    else:
        print("Nenhum arquivo de dados selecionado.\nFim do programa.")
        exit()

    # Step 2: Specify the output file location
    output_file = save_file()
    if output_file:
        print(f"Arquivo CSV será salvo em: {output_file}")
    else:
        print("Arquivo CSV final não especificado.\nFim do programa.")
        exit()


