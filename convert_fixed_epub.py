"""
With chunks from André Ourednik pdf2epub3fixed.py Copyright (C) 2024 André Ourednik and Contributors (https://github.com/aourednik/pdf2epub3fixed)

This script is intended to take an InDesign generated pdf and make a functional fixed epub that is as accessible as possible.

It assumes that the images in InDesign have been converted into a single background image.

It also assumes that the first page is the cover.

The first run will generate a list of fonts. Ensure those fonts are in a folder named "fonts" in the same directory as the pdf. Then run it again.
"""

from functions import get_input_file, extract_pdf_to_json
from datetime import datetime
import os
import zipfile
import shutil
import pymupdf #  PDF processing
from PIL import Image # pillow package
import io
from datetime import datetime
from titlecase import titlecase

## Function list
# int_to_hex_color
# convert_allcaps
# generate_font_list
# 
# write_mimetype_file
# write_meta_inf_container_xml
# write_content_opf
# write_toc_xhtml
# write_toc_ncx
# write_css_and_font_files
# 
# create_epub_structure_from_pdf
# generate_html
# process_images
# zip_folder_to_epub


# Get pdf file
pdf_path = get_input_file('pdf')

# Set base path and change directory
current_folder = os.path.dirname(pdf_path)
os.chdir(current_folder)

# Get cover image
cover_image = get_input_file('jpeg')

#set date
current_date = datetime.now().strftime('%Y-%m-%d')

# set metadata defaults
output_folder = "output"
title =  "The_TITLE"
author =  "AUTHOR_FIRST AUTHOR_LAST"
language =  "en-US"
publisher = "PUBLISHER_NAME"
date = current_date
description = "THIS_IS_THE_DESCRIPTION"
rights =  "Copyright © INSERT_YEAR AUTHOR_NAME"
isbn =  "9780000000000"

# set file paths
epub_file_name =  os.path.splitext(pdf_path)[0]
output_folder_html = os.path.join(output_folder,epub_file_name + "_html")
epub_file_path = os.path.join(output_folder,epub_file_name + ".epub")
font_folder = current_folder + "/fonts"
css_folder = "css"

def int_to_hex_color(value):
    return f"#{value:06X}"

def convert_allcaps(text):
    """
    Checks if all alphabetic characters in the given text are uppercase.
    Returns False if there are no alphabetic characters at all.
    """
    has_alpha = False # Flag to check if there's at least one letter
    for char in text:
        if char.isalpha(): # Only consider alphabetic characters
            has_alpha = True
            if not char.isupper():
                return False # Found a lowercase letter, so it's not all caps
    return has_alpha

def generate_font_list(folder_path):
    font_array = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith((".ttf", ".otf")):  # Check if the file is a TrueType or opentype font
            font_name = os.path.splitext(file_name)[0]  # Remove the extension
            font_path = os.path.join(folder_path, file_name)
            font_array.append({
                "font_name": font_name,
                "font_path": font_path
            })
    return font_array

# create base files
def write_mimetype_file(output_folder):
    mimetype_path = os.path.join(output_folder, "mimetype")
    with open(mimetype_path, "w", encoding="utf-8") as f:
        f.write("application/epub+zip")

def write_meta_inf_container_xml(meta_inf_folder):
    """Write the META-INF/container.xml file"""
    container_path = os.path.join(meta_inf_folder, "container.xml")
    container_content = """<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
    <rootfiles>
        <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
    </rootfiles>
</container>
"""
    with open(container_path, "w", encoding="utf-8") as f:
        f.write(container_content)

def write_content_opf(oebps_folder,content_opf_items,xhtml_files,page):
    page_width = int(page.rect.width)
    page_height = int(page.rect.height)
    """Write OEBPS/content.opf"""
    content_opf_path = os.path.join(oebps_folder, "content.opf")

    font_items = ""
    for font in font_list:        
        media_type = "application/x-font-ttf"  # Default for .ttf
        font_path=os.path.basename(font["font_path"])
        if font_path.lower().endswith(".otf"):
            media_type = "application/vnd.ms-opentype"  # Media type for .otf
        font_items += f'<item id="{font["font_name"]}" href="font/{font_path}" media-type="{media_type}"/>\n' 

    content_opf_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<package version="3.0" unique-identifier="bookid" prefix="schema: http://schema.org/ rendition: http://www.idpf.org/vocab/rendition/# ibooks: http://vocabulary.itunes.apple.com/rdf/ibooks/vocabulary-extensions-1.0/" xml:lang="{language}" xmlns="http://www.idpf.org/2007/opf">
    <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
        <dc:title id="title">{title}</dc:title>
        <dc:creator id="creator1">{author}</dc:creator>
        <meta refines="#creator1" property="role" scheme="marc:relators">aut</meta>
        <dc:identifier id="epubISBN">{isbn}</dc:identifier>
        <dc:identifier id="bookid">urn:isbn:{isbn}</dc:identifier>
        <dc:publisher>{publisher}</dc:publisher>
        <dc:language>{language}</dc:language>
        <dc:date>{date}</dc:date>
        <dc:rights>{rights}</dc:rights>
        <dc:description>{description}</dc:description>
     
        <!--a11y options-->
        <meta property="schema:accessibilityFeature">alternativeText</meta>
        <meta property="schema:accessibilityFeature">highContrastDisplay</meta>
        <meta property="schema:accessibilityFeature">readingOrder</meta>
        <meta property="schema:accessibilityFeature">structuralNavigation</meta>
        <meta property="schema:accessibilityFeature">pageNavigation</meta>
        <meta property="schema:accessibilityFeature">pageBreakMarkers</meta>
        <meta property="schema:accessibilityFeature">tableOfContents</meta>
        <meta property="schema:accessModeSufficient">visual</meta>
        <meta property="schema:accessMode">textual</meta>
        <meta property="schema:accessMode">visual</meta>
        <meta property="schema:accessibilityHazard">none</meta>
        <meta property="schema:accessibilitySummary">This publication includes some accessibility features. It conforms to WCAG 2.0 Level A.</meta>

        <meta property="dcterms:modified">{datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')}</meta>
        <meta name="cover" content="cover-image" />
        <meta property="ibooks:specified-fonts">true</meta>
        <meta name="generator" content="convert_fixed_epub.py" />
    
        <!--fixed-layout options-->
        <meta name="fixed-layout" content="true"/>
        <meta name="original-resolution" content="{page_width}x{page_height}"/>
        <meta property="rendition:spread">landscape</meta>
        <meta name="RegionMagnification" content="true"/>
        <meta property="rendition:layout">pre-paginated</meta>
    </metadata>
    <manifest>
        <item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>
        <item id="css" href="{css_folder}/style.css" media-type="text/css"/>
        {font_items}
        {"".join(content_opf_items)}
    </manifest>
    <spine>
        {"".join(xhtml_files)}
    </spine>
</package>
"""
    with open(content_opf_path, "w", encoding="utf-8") as f:
        f.write(content_opf_content)

def write_toc_xhtml(oebps_folder, doc):
    """Generates nav.xhtml Table of Contents. Will add Bookmarks if they are included in the pdf."""
    toc_xhtml_path = os.path.join(oebps_folder, "nav.xhtml")
    toc = doc.get_toc() 
    toc_xhtml_points = []
    # for chapnum, t in enumerate(toc) :
    for t in toc :
        toc_xhtml_points.append(f"""
        <li><a href="page_{t[2]}.xhtml">{titlecase(t[1])}</a></li>
        """)

    toc_xhtml_content = f"""<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="{language}" xml:lang="{language}">
    <head>
        <title>Nav Contents</title>
    </head>
    <body>
        <nav id="toc" role="doc-toc" epub:type="toc">
            <h1>Contents</h1>
            <ol>
                <li><a href="cover.xhtml">Cover</a></li>
                <li><a href="page_1.xhtml">Digital Rights</a></li>
                <li><a href="page_1.xhtml">Title Page</a></li>
                <li><a href="page_1.xhtml">Copyright Page</a></li>
                <li><a href="page_1.xhtml">Start</a></li>
                {"".join(toc_xhtml_points)}
            </ol>
        </nav>
        <nav aria-labelledby="nav_landmarks" id="landmarks" epub:type="landmarks">
            <h1 id="nav_landmarks">Landmarks</h1>
        <ol>
            <li><a epub:type="cover" href="cover.xhtml">Cover</a></li>
            <li><a epub:type="frontmatter" href="page_1.xhtml">Statement of Digital Rights</a></li>
            <li><a epub:type="bodymatter" href="page_1.xhtml">{title}</a></li>
            <li><a epub:type="backmatter" href="page_1.xhtml">Copyright</a></li>
        </ol>
    </nav>
    </body>
</html>
"""
    with open(toc_xhtml_path, "w", encoding="utf-8") as f:
        f.write(toc_xhtml_content)

def write_css_and_font_files(oebps_folder,font_folder_output,page):

    page_width = int(page.rect.width)
    page_height = int(page.rect.height)
        # Step 8: Add a CSS file with @font-face
    css_folder = os.path.join(oebps_folder, "css")
    os.makedirs(css_folder, exist_ok=True)  # Create the 'css' folder if it doesn't exist
    css_path = os.path.join(css_folder, "style.css")
    css_content = ""

    for font in font_list :
        original_extension = os.path.splitext(font['font_path'])[1]
        output_filename_css = f"{font['font_name']}{original_extension}" # Path in CSS
        css_content += f"""@font-face {{
    font-family: \"{font['font_name']}\";
    font-style: normal;
    font-weight: normal;
    src: url(\"../font/{output_filename_css}\");
}}"""
        
    css_content += f"""
body, div, dl, dt, dd, h1, h2, h3, h4, h5, h6, p, pre, code, blockquote, figure {{
	margin:0;
	padding:0;
	border-width:0;
	text-rendering:optimizeSpeed;
}}

div {{ 
    position: absolute;
}}

img {{
	position: absolute; 
	z-index: -1;
}}

body {{
    width: {page_width}px;
    height: {page_height}px;
    position: relative;
    overflow: hidden; /* Prevent text outside page bounds from being visible */
}}
div {{
    position: absolute;
    white-space: pre; 
    -webkit-user-select: text; 
    -moz-user-select: text;   
    -ms-user-select: text;
    user-select: text;
    overflow: visible;
}}

.upper,
strong {{
    font-weight:normal;
	text-transform:uppercase;
}}
"""
    with open(css_path, "w", encoding="utf-8") as f:
        f.write(css_content)

    for font in font_list : 
        original_extension = os.path.splitext(font['font_path'])[1]  # Get the original extension (.ttf or .otf)
        output_filename = f"{font['font_name']}{original_extension}"
        font_path_output = os.path.join(font_folder_output, output_filename)
        shutil.copyfile(font['font_path'], font_path_output)

# Start process
def create_epub_structure_from_pdf(pdf_path, output_folder, generate_json = True):    
    #Create the folder structure and files needed for epub.
    os.makedirs(output_folder, exist_ok=True)
    
    meta_inf_folder = os.path.join(output_folder, "META-INF")
    os.makedirs(meta_inf_folder, exist_ok=True)
    
    oebps_folder = os.path.join(output_folder, "OEBPS")
    os.makedirs(oebps_folder, exist_ok=True)

    font_folder_output = os.path.join(oebps_folder, "font")
    os.makedirs(font_folder_output, exist_ok=True)

    images_folder = os.path.join(oebps_folder, "image")
    os.makedirs(images_folder, exist_ok=True)
    
    write_mimetype_file(output_folder)
    write_meta_inf_container_xml(meta_inf_folder)

    # Initialize content.opf and toc.ncx content
    content_opf_items = []
    xhtml_files = []

    # Loop through PDF pages and generate HTML
    doc = pymupdf.open(pdf_path)

    # Optional generate json for development purposes
    if generate_json : 
        print("Extracting the PDF structure as raw JSON data for verification")
        extract_pdf_to_json(
            doc,
            os.path.join(output_folder, epub_file_name + "_rawstructure.json")
        )

    image_counter = 0
    print("Processing pages: ")

    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)

        if page_num == 0:
            page_name ="cover"  # First page as cover
            page_label ="i"  # First page as Roman numeral (cover)
        else:
            page_name =  "page_" + str(page_num)  # Start second page at 1 
            page_label = str(page_num)  # Start second page at 1 
        # print(page_label)

        html_file_name = f"{page_name}.xhtml"
        html_file_path = os.path.join(oebps_folder, html_file_name)

        # Generate fixed-layout HTML for the page
        page_html, image_counter, image_manifest = generate_html(
            page, page_label, page_name, image_counter
        )

        with open(html_file_path, "w", encoding="utf-8") as f:
            f.write(page_html)
        # Add to manifest and toc
        content_opf_items.append(
            f'<item id="page_{page_num}" href="{html_file_name}" media-type="application/xhtml+xml"/>\n'
        )
        for img in image_manifest:
            content_opf_items.append(
                f'<item id="page_{img["id"]}" href="{img["href"]}" media-type="image/jpeg"/>\n'
            )
        page_id = f"page_{page_num}"
        if page_num != "i":
            spread = "page-spread-right" if (page_num % 2 == 0) else "page-spread-left"
        else:
            spread = "page-spread-left"
        xhtml_files.append(f'<itemref idref="{page_id}" properties="{spread}"/>\n')

    print("     Done processing.")

    # Add a cover image  
    if os.path.exists(cover_image) :
        print("Processing cover image")
        cover_image_name = os.path.basename(cover_image)
        shutil.copy2(cover_image, images_folder)
        
        content_opf_items.append(
                f'<item id="cover-image" href="image/{cover_image_name}" media-type="image/jpeg"/>\n'
            )
    else : print("Cover image missing.")

    print("\nVerify if you have all the fonts actually used in the PDF. Using these exact names, add them to a folder called 'fonts' in the same directory as the pdf.")

    for fnt in fonts_in_pdf:
        print(fnt)
    write_content_opf(oebps_folder,content_opf_items,xhtml_files,page)
    write_toc_xhtml(oebps_folder, doc)
    write_css_and_font_files(oebps_folder,font_folder_output,page)
    print(f"\nEPUB structure created at: {output_folder}")

def generate_html(page, page_num, page_name, image_counter):  # Added language parameter
    """Generates fixed-layout HTML for a single PDF page with one background image. Renders complete sentences without spans or divs except for italics etc.
    """
    page_width = page.rect.width
    page_height = page.rect.height

    # style page titles
    if page_name.startswith("page_") and page_name[5:].isdigit():
        page_title = f"Page {page_name[5:]}"
    else:
        page_title = page_name.title()

    html_content = f"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="{language}" xml:lang="{language}">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width={page_width},height={page_height}" />
    <title>{page_title}</title>
    <link rel="stylesheet" type="text/css" href="css/style.css" />

</head>
<body style="width:{page_width}px;height:{page_height}px; position:relative; overflow: hidden;">
<span epub:type="pagebreak" id="page{page_num}" role="doc-pagebreak" aria-label="Page {page_num}." />
"""

    images = page.get_images(full=True)
    image_manifest = []  # Initialize as empty list

    if images:  # Check if there are any images
        image_filename = f"{page_name}.jpg"  

        if page_title == "Cover": # use external cover image
            image_filename = os.path.basename(cover_image)

        html_content += f'<img alt="ALT_TEXT_HERE" src="image/{image_filename}" style="position:absolute; left:0px; top:0px; width:{page_width}px; height:{page_height}px; z-index: -1;" />\n'

        if page_title != "Cover":
            image_manifest = [{
                'id': f"image_{image_counter}",
                'href': f"image/{image_filename}"
            }]
        image_counter += 1

    text_instances = page.get_text("dict")
    if "blocks" in text_instances:
        for block in text_instances["blocks"]:
            if "lines" in block:
                for line in block.get('lines', []):
                    for span in line.get('spans', []):
                        font_name = span["font"]
                        if font_name not in fonts_in_pdf:
                            fonts_in_pdf.append(font_name)
                        if 'text' in span:
                            left = span['origin'][0]
                            top = span['origin'][1]
                            size = span['size']
                            font = span['font']
                            # check for special characters i.e. &
                            text = span['text'].replace("&", "&amp;")
                            color = span['color']
                            # adjust top to compensate for alignment
                            top = top - size

                            if int(color) != 0:
                                hex_color = int_to_hex_color(int(color))
                                text_color = f" color:{hex_color};"
                            else:
                                text_color = ""
                                
                            # if text is all caps convert to <strong> and title case
                            if convert_allcaps(text):
                                html_content += f'<div style="left:{left:.2f}px; top:{top:.2f}px; font-size:{size:.2f}px; font-family:\'{font}\'; {text_color}"><p><span class="upper">{titlecase(text)}</span></p></div>\n'
                            else:
                                html_content += f'<div style="left:{left:.2f}px; top:{top:.2f}px; font-size:{size:.2f}px; font-family:\'{font}\';{text_color}"><p>{text}</p></div>\n'

    html_content += "</body></html>"

    return html_content, image_counter, image_manifest

def process_images(pdf_path, output_folder_html):
    # Process single background image on the page
    image_path = os.path.join(output_folder_html,"OEBPS/image")
       
    doc = pymupdf.open(pdf_path)

    for page_index in range(len(doc)):
        page = doc[page_index]
        images = page.get_images(full=True)
        
        if images:

            for img_index, img in enumerate(images):
                xref = img[0]

                pix = pymupdf.Pixmap(doc, xref)
                if pix.colorspace.n == 4:  # Check if it's CMYK
                    pix = pymupdf.Pixmap(pymupdf.csRGB, pix)  # Convert to RGB

                image = Image.open(io.BytesIO(pix.tobytes()))
                image = image.convert("RGB") # Ensure PIL also treats it as RGB
                
                if page_index == 0:
                    page_label ="cover"  # First page is cover — don't create image as we will use the external file
                else:
                    page_label =  "page_" + str(page_index)  # Start second page at 1 
                    image.save(f"{image_path}/{page_label}.jpg", "JPEG")

                # Clean up the Pixmap object
                pix = None

    doc.close()

def zip_folder_to_epub(folder_path, epub_path):
    # Zips the folder structure and creates an EPUB file.

    with zipfile.ZipFile(epub_path, 'w', zipfile.ZIP_STORED) as epubFile:
        epubFile.writestr('mimetype', 'application/epub+zip')

        # Navigate to the exportFolderPath and add all files to the EPUB
        os.chdir(folder_path)
        for root, dirs, files in os.walk("."):
            for file in files:
                if file != 'mimetype':
                    epubFile.write(os.path.join(root, file), compress_type=zipfile.ZIP_DEFLATED)
    print(f"\nEPUB file created at: {epub_path}\n")

# Run process
os.makedirs("fonts", exist_ok=True)

font_list = generate_font_list(font_folder)
fonts_in_pdf = []

# Create epub
print("Creating fixed epub")
create_epub_structure_from_pdf(pdf_path, output_folder_html,True)
    # change False to True if you want to see the json
process_images(pdf_path,output_folder_html)
zip_folder_to_epub(output_folder_html, epub_file_path)
