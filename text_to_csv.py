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
            if check_first_line(fisrt_line):
                pass
            else:
                raise InvalidFormatException

            # Ler e processar cada linha
            for line in reader:
                
                print(f"Lendo linha: {line}")  # Exibir a linha (opcional)
                
                csv_line = processed_data(line)
                # Escrever a linha imediatamente no arquivo de saída
                writer.writerow(csv_line)
                print(f"Linha salva: {csv_line}")

    except InvalidFormatException as e:
        print(e)
    except FileNotFoundError:
        print("Arquivo de entrada não encontrado.")
    except Exception as e:
        print(f"Erro inesperado: {e}")
    

def check_first_line(data):
    """Check if the first line of the data is a header."""
    return True

def processed_data(data):
    """Process the input data and return the processed data."""
    # Processar os dados conforme necessário
    processed_data = data
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


