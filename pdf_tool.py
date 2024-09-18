import tkinter as tk
from tkinter import filedialog, StringVar, OptionMenu, messagebox
import pymupdf
import os
import glob
import re

def browse_source_file():
    global source_data_file
    source_data_file = filedialog.askopenfilename(filetypes=[("Fichiers PDF", "*.pdf")])
    source_file_entry.delete(0, tk.END)
    source_file_entry.insert(0, source_data_file)

def browse_search_path():
    global search_path
    search_path = filedialog.askdirectory()
    search_path_entry.delete(0, tk.END)
    search_path_entry.insert(0, search_path)

def browse_merged_pdf_directory():
    global merged_pdf_directory
    merged_pdf_directory = filedialog.askdirectory()
    merged_pdf_directory_entry.delete(0, tk.END)
    merged_pdf_directory_entry.insert(0, merged_pdf_directory)

def get_data(page_num):
    doc = pymupdf.open(source_data_file)
    page = doc.load_page(page_num)
    text = page.get_text("text")
    lines = text.splitlines()

    if len(lines) < 3:
        return None

    line1 = lines[0]
    line2 = lines[1]
    match1 = re.search(r'\d+', line1)
    match2 = re.search(r'\d+', line2)

    if match1 and match2:
        intmed = match1.group()
        police = match2.group()
        return {"intmed": intmed, "police": police}

    return None

def search_pdfs(page_num):
    data_pdf = get_data(page_num)
    if not data_pdf:
        return None

    intmed = data_pdf.get("intmed")
    police = data_pdf.get("police")

    selected_type = type_options[the_type.get()]

    if selected_type == "C":
        pattern = f"C_{intmed}_{police}_*.pdf"
    elif selected_type == "V":
        pattern = f"V_{intmed}_{police}_*.pdf"
    else:
        return "type invalid"

    exact_file = os.path.join(search_path, pattern)
    matching_files = glob.glob(exact_file)
    
    if matching_files:
        file_names = []
        for file in matching_files:
            file_name = os.path.basename(file)
            file_names.append(file_name)
        return file_names
    else:
        return None

def merge_page_with_pdfs(page_num):
    data_pdf = get_data(page_num)
    if not data_pdf:
        return f"page {page_num + 1} sautée, aucune donnée valide."

    intmed = data_pdf.get("intmed")
    police = data_pdf.get("police")
    matching_files = search_pdfs(page_num)

    if not (isinstance(matching_files, list) and matching_files):
        if the_type.get() == "Chèque":
            return f"aucun fichier trouvé pour ce pattern C_{intmed}_{police}_*.pdf"
            #messagebox.showinfo(f"aucun fichier trouvé pour ce pattern C_{intmed}_{police}_*.pdf")
        if the_type.get() == "Virement":
            return f"aucun fichier trouvé pour ce pattern V_{intmed}_{police}_*.pdf"
            #messagebox.showinfo(f"aucun fichier trouvé pour ce pattern V_{intmed}_{police}_*.pdf")

    merged_pdf = pymupdf.open()
    source_pdf = pymupdf.open(source_data_file)
    merged_pdf.insert_pdf(source_pdf, from_page=page_num, to_page=page_num)

    for pdf_file in matching_files:
        pdf_path = os.path.join(search_path, pdf_file)
        external_pdf = pymupdf.open(pdf_path)
        merged_pdf.insert_pdf(external_pdf)
        external_pdf.close()

    #output_pdf = os.path.join(merged_pdf_directory, f"{the_type.get()}_{intmed}_{police}.pdf")
    #naming pdf
    if the_type.get() == "Chèque":
        output_pdf = os.path.join(merged_pdf_directory, f"C_{intmed}_{police}.pdf")
    if the_type.get() == "Virement":
        output_pdf = os.path.join(merged_pdf_directory, f"V_{intmed}_{police}.pdf")
    merged_pdf.save(output_pdf)
    merged_pdf.close()

def start_merging():
    global source_data_file, search_path, merged_pdf_directory, the_type

    source_data_file = source_file_entry.get()
    search_path = search_path_entry.get()
    merged_pdf_directory = merged_pdf_directory_entry.get()
    
    if not all([source_data_file, search_path, merged_pdf_directory, the_type.get()]):
        messagebox.showerror("Error", "vous devez remplir tous les champs")
        return

    merger_dyn()

def merger_dyn():
    doc = pymupdf.open(source_data_file)
    page_count = doc.page_count
    for page_num in range(page_count):
        res = merge_page_with_pdfs(page_num)
        if res:
            print(res)

#init App + cfg
root = tk.Tk()
root.geometry("820x235")
root.resizable(False, False)
root.iconbitmap(r'.\assets\pdf.ico')
root.title("Gestionnaire De Bordereaux PDF")

#Iinit global vars
source_data_file = ""
search_path = ""
merged_pdf_directory = ""
type_options = {"Chèque": "C", "Virement": "V"}
the_type = StringVar()

#widgets wl arnabat o dakchi
#-------source_data_file----------#
tk.Label(root, text="Fichier des données source").grid(row=0, column=0, padx=5, sticky="w")
source_file_entry = tk.Entry(root, width=50)
source_file_entry.grid(row=0, column=1, padx=5, sticky="w")
tk.Button(root, text="Parcourir", command=browse_source_file, bg="#E2DAD6").grid(row=0, column=2, padx=5, sticky="w")
#-------search_path----------#
tk.Label(root, text="chemin des fichier de recherche").grid(row=1, column=0, padx=5, sticky="w", pady=10)
search_path_entry = tk.Entry(root, width=50)
search_path_entry.grid(row=1, column=1, padx=5, sticky="w", pady=10)
tk.Button(root, text="Parcourir", command=browse_search_path, bg="#E2DAD6").grid(row=1, column=2, padx=5, sticky="w", pady=10)
#-------merged_pdf_directory----------#
tk.Label(root, text="chemin de sauvegarde des fichiers pdf").grid(row=2, column=0, padx=5, sticky="w")
merged_pdf_directory_entry = tk.Entry(root, width=50)
merged_pdf_directory_entry.grid(row=2, column=1, padx=5, sticky="w")
tk.Button(root, text="Parcourir", command=browse_merged_pdf_directory, bg="#E2DAD6").grid(row=2, column=2, padx=5, sticky="w")
#________type_options__________#
tk.Label(root, text="Type de transaction:").grid(row=3, column=0, padx=5, sticky="w")
type_menu = OptionMenu(root, the_type, *type_options.keys()).grid(row=3, column=0, padx=150, sticky="w", pady=10) # wrri l keys dyal dict li drti lfo9 (Chèque, Virement)
#---exec code button---------#
mrg = tk.PhotoImage(file=r".\assets\merge.png")
rsz = mrg.subsample(7, 7)
tk.Button(root, image=rsz, compound="left", text="Fusionner pdf", command=start_merging, bg="#7FA1C3", width=100).grid(row=4, column=1, padx=0, sticky="w", pady=30)
#---logo---------#
image = tk.PhotoImage(file=r".\assets\logo.png")
resized_image = image.subsample(12, 12)
label = tk.Label(root, image=resized_image).grid(row=4, column=2, padx=0, sticky="w")

root.mainloop()
