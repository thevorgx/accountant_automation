import re
import pymupdf
import os
import glob

#chemin du fichier d'où proviennent les données(a changé).
SOURCE_DATA_FILE = r"C:\Users\khali\OneDrive\Desktop\accountant_automation\sour_data_pdfs\bigdata.pdf"
#chemin du dossier où se trouvent les fichiers que je souhaite rechercher(a changé).
PATH_SEARCH = r"C:\Users\khali\OneDrive\Desktop\accountant_automation\pdfs_tofind"
#chemin du dossier dans lequel vous souhaitez enregistrer les fichiers de sortie(a changé).
MERGED_PDF_DIRECTORY = r"C:\Users\khali\OneDrive\Desktop\accountant_automation\saved_pdf"
#type d'operation: peut être "C(chéque)" ou "V(virement)" (regard la fonction "search_pdfs()")(a changé).
TYPE = "C"

doc = pymupdf.open(SOURCE_DATA_FILE)
page_count = doc.page_count



def get_data(page_num):
    """extraire extraire les données "intmed" et "police".
    return rien si y a moin de 3 lignes de text dans la page ou si la les valeurs sont pas trouvé
    return "intmed" et "police" s'ils sont trouvés dans la page en dictionnaire (key = value)
    pour les extraire plus tard en utilisant la méthode get()"""
    page = doc.load_page(page_num)#ouvrire la page voulu.
    text = page.get_text("text")#prendre que le text dans la page.
    lines = text.splitlines()#séparer les lignes(pour les traiter séparement).

    if len(lines) < 3:
        return None

    line1 = lines[0] 
    line2 = lines[1]
    #print(text)
    #print(f" page : {page_num + 1} ---> ligne1: {line1} ligne2: {line2}")
    match1 = re.search(r'\d+', line1)#regex "\d+" prendre la premiére sequence de chiffres dans la ligne.
    match2 = re.search(r'\d+', line2)

    if match1 and match2:#si les deux sequences trouvé: sauvegarde dans deux variables "intmed" et "police".
        intmed = match1.group()#la méthode groupe() sert pour extraire le string du séquence
        police = match2.group()#parce que la méthode search() en haut retourne un objet est pas un string.
        return {"intmed": intmed, "police": police}                                           

    return None

def search_pdfs(page_num, directory=PATH_SEARCH):
    """Rechercher les fichiers pdf correspondant au motif spécifié.
    Retourner None si aucune donnée n'est trouvée.
    Retourner "type invalide" si le type ne correspond pas à "C" ou "V".
    Si une erreur se produit (laisser pour le débogage), retourner le message "type invalid".
    Retourner une liste des noms de fichiers à fusionner."""
    #data voulu du pdf (intmed, police)
    data_pdf = get_data(page_num)
    if not data_pdf:
        return None
    
    intmed = data_pdf.get("intmed")
    police = data_pdf.get("police")
    #vérifier quel Type d'operation pour construire le pattern voulu
    if TYPE == "C":
        pattern = f"C_{intmed}_{police}_*.pdf"
    elif TYPE == "V":
        pattern = f"V_{intmed}_{police}_*.pdf"
    else:
        return "type invalid"

    exact_file = os.path.join(directory, pattern)#combine le chemin du dossier et le pattern pour créer le chemin complet de recherche.
    matching_files = glob.glob(exact_file)#rehcerche les fichiers correspondant au pattern "exact_file" (glob() renvois une list de leurs chemin).
    #print(matching_files)
    file_names = []
    #si il trouve quelque chose, on stock les noms des fichiers dans une liste "file_names"
    #PS: enléve le commentaire sur le print() en bas pour voir.
    if matching_files:
        for file in matching_files:
            file_name = os.path.basename(file)
            file_names.append(file_name)
        #print(f"{file_names}")
        return file_names
    else:
        return None

def merge_page_with_pdfs(page_num):
    """fusionner la page ou on a pris les données (intmed, police)
    avec les fichers correspondant(plus de details en commentaires en bas)"""
    #get data du voulu du pdf (intmed, police)
    data_pdf = get_data(page_num)
    if not data_pdf:
        #print(f"page {page_num + 1} sautée, aucune donnée valide.")
        return f"page {page_num + 1} sautée, aucune donnée valide."
    intmed = data_pdf.get("intmed")
    police = data_pdf.get("police")
    matching_files = search_pdfs(page_num)

    #vérifie si 'matching_files' n'est pas une liste valide et non vide -> regarde la documentation
    #de valeurs retourner de search_pdfs()
    if not (isinstance(matching_files, list) and matching_files):
        #print(f"No files found for pattern {TYPE}_{intmed}_{police}_*.pdf")
        return f"aucun fichier trouvé pour ce pattern {TYPE}_{intmed}_{police}_*.pdf"

    #crée un nouveau pdf et mettre la bonne page du fichier data
    merged_pdf = pymupdf.open()
    merged_pdf.insert_pdf(doc, from_page=page_num, to_page=page_num)

    #fusionner le nouveau fichier crée avec les autres fichiers correspondant au pattern
    for pdf_file in matching_files:
        pdf_path = os.path.join(PATH_SEARCH, pdf_file)#construire le chemin d'accès au fichier en joignant le dossier "PATH_SEARCH" avec le nom de fichier "pdf_file."
        external_pdf = pymupdf.open(pdf_path)
        merged_pdf.insert_pdf(external_pdf)
        external_pdf.close()

    #sauvegardé le fichier crée avec le nom "{TYPE}_{intmed}_{police}.pdf"
    #exemple: C_9834_334423.pdf
    output_pdf = os.path.join(MERGED_PDF_DIRECTORY, f"{TYPE}_{intmed}_{police}.pdf")
    merged_pdf.save(output_pdf)
    merged_pdf.close()

#exec du programme
if __name__ == "__main__":
    for page_num in range(page_count):
        res = merge_page_with_pdfs(page_num)
        #if res:
            #print(res)
