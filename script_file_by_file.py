import tkinter as tk
from tkinter import filedialog
from b3_to_csv import converter_b3_para_csv

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

if __name__ == "__main__":

    try:
        input_file = select_file()
        if input_file:
            print(f"Arquivo de dados selecionado: {input_file}")
        else:
            print("Nenhum arquivo de dados selecionado.\nFim do programa.")
            exit()

        output_file = save_file()
        if output_file:
            print(f"Arquivo CSV será salvo em: {output_file}")
        else:
            print("Arquivo CSV final não especificado.\nFim do programa.")
            exit()

        converter_b3_para_csv(input_file, output_file)

    except Exception as e:
        print(f"Erro durante a conversão: {e}")
        
    finally:    
        print("Conversão concluída com sucesso.")