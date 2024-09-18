import tkinter as tk
from tkinter import filedialog
import source
"""GUI: work in progress..."""

merged_pdf_directory = source.merged_pdf_directory
source_data_file = source.source_data_file
search_path = source.search_path
the_type = source.the_type

def save_directory():
    global merged_pdf_directory
    merged_pdf_directory = filedialog.askdirectory()
    save_entry.delete(0, tk.END)
    save_entry.insert(0, merged_pdf_directory)

def data_file():
    global source_data_file
    source_data_file = filedialog.askopenfilename()
    data_file_entry.delete(0, tk.END)
    data_file_entry.insert(0, source_data_file)

def search_directory():
    global search_path
    search_path = filedialog.askdirectory()
    search_dir_entry.delete(0, tk.END)
    search_dir_entry.insert(0, search_path)

def transaction_type(event):
    global the_type
    selection = listbox.curselection()
    if selection:
        selected = listbox.get(selection[0])
        if selected == "Chèque":
            the_type = "C"
        elif selected == "Virement":
            the_type = "V"
        type_label.config(text=f"Catégorie: {selected}")

def render():
    global save_entry, data_file_entry, search_dir_entry, listbox, type_label
    root = tk.Tk()
    root.configure(bg="white")
    root.title("vorg pdf fusion reactor")

    #1-------save_directory--------#
    save_label = tk.Label(root, text="Chemin de sauvegarde des fichiers pdf:", bg="white")
    save_label.grid(row=0, column=0, padx=5, sticky="w")

    save_entry = tk.Entry(root, width=50)
    save_entry.grid(row=0, column=1, sticky="w")

    parcourir1 = tk.Button(root, text="Parcourir", command=save_directory, bg="#557C56")
    parcourir1.grid(row=0, column=2, padx=5, sticky="w")

    #2-------data_file--------#
    srs_data_label = tk.Label(root, text="chemin d'accès au fichier pdf des données sources:", bg="white")
    srs_data_label.grid(row=1, column=0, padx=5, sticky="w")

    data_file_entry = tk.Entry(root, width=50)
    data_file_entry.grid(row=1, column=1, sticky="w")

    parcourir2 = tk.Button(root, text="Parcourir", command=data_file, bg="#557C56")
    parcourir2.grid(row=1, column=2, padx=5, sticky="w")

    #3-------search_dir--------#
    search_label = tk.Label(root, text="Fichier de recherche:", bg="white")
    search_label.grid(row=2, column=0, padx=5, sticky="w")

    search_dir_entry = tk.Entry(root, width=50)
    search_dir_entry.grid(row=2, column=1, sticky="w")

    parcourir3 = tk.Button(root, text="Parcourir", command=search_directory, bg="#557C56")
    parcourir3.grid(row=2, column=2, padx=5, sticky="w")

    #4-------Transaction_Type--------#
    transaction_label = tk.Label(root, text="Type de transaction:", bg="white")
    transaction_label.grid(row=3, column=0, padx=5, sticky="w")

    listbox = tk.Listbox(root, height=2,)
    listbox.insert(tk.END, "Chèque")
    listbox.insert(tk.END, "Virement")
    listbox.grid(row=4, column=0, padx=5, sticky="w")
    listbox.bind("<<ListboxSelect>>", transaction_type)

    type_label = tk.Label(root, text="", fg="#557C56", font=("bold", 12), bg="white")
    type_label.grid(row=4, column=1, padx=0, sticky="w")


    root.mainloop()
