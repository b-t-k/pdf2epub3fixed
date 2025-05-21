'''
Functions
'''

import os, pathlib
import tkinter as tk
from tkinter import filedialog
import json
import base64

### Contents
# get_input_file
# get_file_by_type
# extract_pdf_to_json
# write_toc_ncx

def get_input_file(type="epub",testFile=None): 
    """
    A function to display a message to open a file which returns a string (osx).

    Checks for a file name already and allows for e.g. "folder name" to be submitted
    """

    if testFile is None:
    
        inputFile = get_file_by_type(type)
        
        if inputFile is None:  # Check if no file was selected
            return None

    else:
        inputFile = testFile
 
    # Use pathlib to handle paths consistently
    path = pathlib.Path(inputFile)
    print("Input file path: ",path)

    if not path.exists():
        print(f"\n\n***NO FILE***\n Did you remember to change the file path?\n")
        inputFile = None  # Set back to None then exit
        return None

    return(inputFile)


def get_file_by_type(file_type,exportFolderPath=None,  initial_dir=None):
    """Open a file dialog to select an EPUB or Excel file based on input type."""
    
    # Create a dictionary to map file type to file dialog filter
    file_types = {
        "epub": [("EPUB files", "*.epub")],
        "pdf": [("pdf files", "*.pdf")],
        "jpeg": [("jpg files", "*.jpeg")],
        "excel": [("Excel files", "*.xlsx")],
        "folder":[]
    }

    # Validate the input file type
    if file_type not in file_types:
        print(f"Invalid file type: {file_type}. Supported types are 'epub', 'excel' 'pdf', 'jpeg' or a folder.")
        return None

    # Open the file dialog with the correct filter based on file type
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # check to see if a folderpath was specified so tkinter will use it as a default for looking for the folder
    if exportFolderPath:
        initial_dir = os.path.expanduser("../"+exportFolderPath)
        print("INITIAL ",initial_dir)
   
    if file_type!="folder":
        path = filedialog.askopenfilename(title=f"Select a {file_type.capitalize()} file", filetypes=file_types[file_type])

    else:
        path = filedialog.askdirectory(title="Select a folder!", initialdir=initial_dir)

    if not path:
        print(f"No {file_type} file selected.")
        return None  # Return None if no file was selected
    
    return path

def extract_pdf_to_json(doc, output_json_path):
    """Extracts all pages of a PDF as JSON and writes to a file for checking purposes"""
    pages_data = []
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        page_dict = page.get_text("dict")  # Extract page data in dict format        
        # Process blocks to handle binary data
        for block in page_dict.get("blocks", []):
            if "image" in block and isinstance(block["image"], bytes):
                # Convert image bytes to base64 string
                block["image"] = base64.b64encode(block["image"]).decode("utf-8")
        page_data = {
            "page_num": page_num + 1,  # Human-readable page number
            "content": page_dict,
        }
        pages_data.append(page_data)
    with open(output_json_path, "w", encoding="utf-8") as json_file:
        json.dump(pages_data, json_file, indent=4, ensure_ascii=False)
    print(f"PDF content extracted and saved to {output_json_path}")

# Create NCX (Deprecated)
def write_toc_ncx(oebps_folder, doc):
    """This generates an EPUB 2 type navigation. Deprecated."""
    toc_ncx_path = os.path.join(oebps_folder, "toc.ncx")
    # # toc = doc.get_toc() # [[1, 'Préface', 7], [1, 'Les deux mélodies fondamentales', 17], ...]
    toc_ncx_points = []
    # for chapnum, t in enumerate(toc) :
    #     toc_ncx_points.append(f"""
    #     <navPoint id="chapter-{chapnum + 1}" playOrder="{chapnum + 1}">
    #         <navLabel>
    #             <text>{t[1]}</text>
    #         </navLabel>
    #         <content src="page_{t[2]}.xhtml"/>
    #     </navPoint>
    #     """)

    toc_ncx_points.append("""
    <navPoint id="navPoint1">
        <navLabel>
            <text>Cover</text>
        </navLabel>
        <content src="cover.xhtml" />
    </navPoint>""")

    toc_ncx_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
    <head>
        <meta name="dtb:uid" content="urn:isbn:{isbn}"/>
        <meta name="dtb:depth" content="1"/>
        <meta name="dtb:totalPageCount" content="{doc.page_count}"/>
        <meta name="dtb:maxPageNumber" content="{doc.page_count}"/>
    </head>
    <docTitle>
        <text>{title}</text>
    </docTitle>
    <navMap>
        {"".join(toc_ncx_points)}
    </navMap>
</ncx>
"""
    with open(toc_ncx_path, "w", encoding="utf-8") as f:
        f.write(toc_ncx_content)
