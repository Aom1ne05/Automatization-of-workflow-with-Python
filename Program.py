import tkinter as tk
from tkinter import simpledialog, ttk
from tkinter.font import Font
import json
import os

# Paths for the data files
DOCUMENTS_FILE = "documents.json"
DIRECTORIES_FILE = "directories.json"

# Load data from JSON files
def load_data():
    if os.path.exists(DOCUMENTS_FILE) and os.path.exists(DIRECTORIES_FILE):
        with open(DOCUMENTS_FILE, "r") as doc_file:
            documents = json.load(doc_file)
        with open(DIRECTORIES_FILE, "r") as dir_file:
            directories = json.load(dir_file)
    else:
        documents = [
            {'type': 'passport', 'number': '2207 876234', 'name': 'John Ray'},
            {'type': 'invoice', 'number': '11-2', 'name': 'Olivia Cust'},
            {'type': 'insurance', 'number': '10006', 'name': 'Stan Smith'}
        ]
        directories = {
            '1': ['2207 876234', '11-2'],
            '2': ['10006'],
            '3': []
        }
    return documents, directories

# Save data to JSON files
def save_data(documents, directories):
    with open(DOCUMENTS_FILE, "w") as doc_file:
        json.dump(documents, doc_file, indent=4)
    with open(DIRECTORIES_FILE, "w") as dir_file:
        json.dump(directories, dir_file, indent=4)

def display_info(info):
    # Create a top-level window (dialog) that is always on top
    top = tk.Toplevel(root)
    top.title("Information")
    top.geometry("800x500")
    top.attributes('-topmost', True)
    top.configure(bg='lightblue')

    # Set font
    font = Font(family="Montserrat", size=12)

    tk.Label(top, text="Information", padx=20, pady=10, font=font, bg='lightblue').pack()

    # Create a Treeview widget
    columns = ("Number", "Type", "Owner", "Shelf")
    tree = ttk.Treeview(top, columns=columns, show='headings')
    tree.heading("Number", text="Document Number")
    tree.heading("Type", text="Type")
    tree.heading("Owner", text="Owner")
    tree.heading("Shelf", text="Shelf")

    for line in info:
        tree.insert("", tk.END, values=line)

    tree.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

    tk.Button(top, text="OK", command=top.destroy, font=font, bg='lightgreen', relief=tk.RAISED).pack(pady=10)

def owner_of_doc():
    number_of_document = simpledialog.askstring("Input", "Enter document number:", parent=root)
    for element in documents:
        if number_of_document == element['number']:
            shelf = get_shelf_of_document(element['number'])
            display_info([(element['number'], element['type'], element['name'], shelf)])
            return
    display_info([('Document not found in the database', '', '', '')])

def shelf_of_dir():
    number_of_document = simpledialog.askstring("Input", "Enter document number:", parent=root)
    for key, values in directories.items():
        if number_of_document in values:
            display_info([(number_of_document, "N/A", "N/A", key)])
            return
    display_info([('Document not found in the database', '', '', '')])

def all_info():
    info = []
    for element in documents:
        shelf = get_shelf_of_document(element['number'])
        info.append((element['number'], element['type'], element['name'], shelf))
    
    # Add entries for empty shelves
    all_shelves = set(directories.keys())
    shelves_with_docs = {get_shelf_of_document(doc['number']) for doc in documents}
    empty_shelves = all_shelves - shelves_with_docs

    for shelf in empty_shelves:
        info.append(('N/A', 'N/A', 'N/A', shelf))

    display_info(info)

def get_shelf_of_document(doc_number):
    for key, values in directories.items():
        if doc_number in values:
            return key
    return "N/A"

def add_shelf():
    shelf_number = simpledialog.askstring("Input", "Enter shelf number:", parent=root)
    if shelf_number not in directories:
        directories[shelf_number] = []
        save_data(documents, directories)
        display_info([('Shelf added', '', '', f'Current shelves: {", ".join(list(directories.keys()))}')])
    else:
        display_info([('This shelf already exists', '', '', f'Current shelves: {", ".join(list(directories.keys()))}')])

def del_shelf():
    shelf_number = simpledialog.askstring("Input", "Enter shelf number:", parent=root)
    if shelf_number in directories and len(directories[shelf_number]) == 0:
        del directories[shelf_number]
        save_data(documents, directories)
        display_info([('Shelf deleted', '', '', f'Current shelves: {", ".join(list(directories.keys()))}')])
    elif shelf_number in directories and len(directories[shelf_number]) != 0:
        display_info([('The shelf contains documents, remove them before deleting the shelf', '', '', f'Current shelves: {", ".join(list(directories.keys()))}')])
    else:
        display_info([('This shelf does not exist', '', '', f'Current shelves: {", ".join(list(directories.keys()))}')])

def add_doc():
    number_of_document = simpledialog.askstring("Input", "Enter document number:", parent=root)
    type_of_document = simpledialog.askstring("Input", "Enter document type:", parent=root)
    name_of_user = simpledialog.askstring("Input", "Enter document owner:", parent=root).title()
    shelf_number = simpledialog.askstring("Input", "Enter storage shelf:", parent=root)
    if shelf_number in directories:
        directories[shelf_number].append(number_of_document)
        documents.append({'type': type_of_document, 'number': number_of_document, 'name': name_of_user})
        save_data(documents, directories)
        all_info()  # Display updated information
    else:
        display_info([('This shelf does not exist', '', '', f'Add shelf with command Add Shelf\nCurrent list of documents:\n' + "\n".join([f"№: {d['number']}, Type: {d['type']}, Owner: {d['name']}" for d in documents]))])

def del_doc():
    number_of_document = simpledialog.askstring("Input", "Enter document number:", parent=root)
    found = False
    for x in range(len(documents)):
        if number_of_document == documents[x]['number']:
            found = True
            del documents[x]
            for values in directories.values():
                if number_of_document in values:
                    values.remove(number_of_document)
            save_data(documents, directories)
            break
    if found:
        all_info()  # Display updated information
    else:
        display_info([('Document not found in the database', '', '', f'Current list of documents:\n' + "\n".join([f"№: {d['number']}, Type: {d['type']}, Owner: {d['name']}" for d in documents]))])

def move_doc():
    number_of_document = simpledialog.askstring("Input", "Enter document number:", parent=root)
    shelf_number = simpledialog.askstring("Input", "Enter shelf number:", parent=root)
    found_doc = False
    if shelf_number in directories:
        for values in directories.values():
            if number_of_document in values:
                values.remove(number_of_document)
                directories[shelf_number].append(number_of_document)
                found_doc = True
                break
        if found_doc:
            save_data(documents, directories)
            all_info()  # Display updated information
        else:
            display_info([('Document not found in the database', '', '', f'Current list of documents:\n' + "\n".join([f"№: {d['number']}, Type: {d['type']}, Owner: {d['name']}" for d in documents]))])
    else:
        display_info([('This shelf does not exist', '', '', f'Current shelves: {", ".join(list(directories.keys()))}')])

def quit_program():
    save_data(documents, directories)
    root.destroy()

# Create the main window
root = tk.Tk()
root.title("Document Management System")
root.geometry("400x500")
root.configure(bg='lightblue')

# Load Montserrat font
font_path = "Montserrat-Regular.ttf"  # Replace with the path to your Montserrat font file
root.option_add('*Font', 'Montserrat 12')
root.tk.call("font", "create", "Montserrat", "-family", "Montserrat", "-size", 12)

# Define rounded button style
def rounded_button(text, command, color='lightgreen'):
    btn = tk.Button(root, text=text, command=command, bg=color, font=("Montserrat", 12), relief=tk.FLAT, width=20)
    btn.pack(pady=5, padx=10)
    btn.bind("<Enter>", lambda e: btn.config(bg='lightcoral'))
    btn.bind("<Leave>", lambda e: btn.config(bg=color))
    return btn

# Load existing data
documents, directories = load_data()

# Add buttons for different commands
rounded_button("Find Document Owner", owner_of_doc)
rounded_button("Find Document Shelf", shelf_of_dir)
rounded_button("Show All Info", all_info)
rounded_button("Add Shelf", add_shelf)
rounded_button("Delete Shelf", del_shelf)
rounded_button("Add Document", add_doc)
rounded_button("Delete Document", del_doc)
rounded_button("Move Document", move_doc)
rounded_button("Quit", quit_program, color='lightcoral')

# Run the application
root.mainloop()
