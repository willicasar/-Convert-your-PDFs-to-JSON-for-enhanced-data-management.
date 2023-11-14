import os
import tkinter as tk
from tkinter import filedialog
import json
import pdfplumber
import PyPDF2
import webbrowser

def convert_to_json():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path.endswith('.pdf'):
        try:
            with pdfplumber.open(file_path) as pdf:
                pdf_data = []
                for page_num, page in enumerate(pdf.pages, start=1):
                    page_text = page.extract_text()
                    pdf_data.append({'page': page_num, 'text': page_text})

                file_name = os.path.splitext(os.path.basename(file_path))[0]
                directory = os.path.dirname(file_path)
                json_file_path = os.path.join(directory, f"{file_name}.json")

        except Exception as e:
            print(f"Error with pdfplumber: {e}. Trying with PyPDF2...")
            try:
                pdf_file = open(file_path, 'rb')
                pdf_reader = PyPDF2.PdfReader(pdf_file)

                pdf_data = []
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    page_text = page.extract_text()
                    pdf_data.append({'page': page_num + 1, 'text': page_text})

                pdf_file.close()
                file_name = os.path.splitext(os.path.basename(file_path))[0]
                directory = os.path.dirname(file_path)
                json_file_path = os.path.join(directory, f"{file_name}.json")

            except Exception as e:
                print(f"Error with PyPDF2: {e}. Cannot extract text from PDF.")
                result_label.config(text="¡Error! No se puede extraer texto del PDF.")
                return

        json_data = json.dumps(pdf_data, indent=2)

        with open(json_file_path, 'w') as json_file:
            json_file.write(json_data)
        result_label.config(text=f"¡Conversión completada! Archivo '{file_name}.json' generado.", fg="black")
        convert_button.pack_forget()  # Oculta el botón "Convertir a JSON"
        view_json_button.pack()  # Muestra el botón "Ver JSON"

    else:
        result_label.config(text="¡Error! Selecciona un archivo PDF.", fg="black")

def view_json():
    json_file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if json_file_path.endswith('.json'):
        json_directory = os.path.dirname(json_file_path)
        result_label.config(text=f"El archivo JSON está en: {json_directory}", fg="black")
        webbrowser.open(json_file_path)  # Abre el archivo JSON en el navegador

root = tk.Tk()
root.title("PDF to JSON Converter")
root.geometry("300x200")
root.configure(bg="#F9DCC5")

instructions = tk.Label(root, text="Por favor, selecciona un archivo PDF:", fg="black", bg="#F9DCC5")
instructions.pack()

convert_button = tk.Button(root, text="Convertir a JSON", command=convert_to_json, bg="#FC9C4F")
convert_button.pack()

result_label = tk.Label(root, text="", fg="black", bg="#F9DCC5")
result_label.pack()

view_json_button = tk.Button(root, text="Ver JSON", command=view_json, bg="#FC9C4F")  # Mostrará el botón "Ver JSON" después de la conversión
view_json_button.pack()
view_json_button.pack_forget()  # Se oculta inicialmente

root.mainloop()

