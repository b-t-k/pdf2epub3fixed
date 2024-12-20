# PDF2epub3fixed

This python script generates a fixed-layout EPUB3 e-book from a PDF file in two variants: 

- __your_file_html.epub__ : A rich text variant, with a table of contents, clickable cross-references and hyperlinks. The text body is selectable and searchable. Positioning of all text boxes is 95% reliable and the resulting file readable by most epub readers (Apple Books, Google Play Books, ...). For fine-tuning, use an EPUB editor like [Sigil](https://sigil-ebook.com/).
- __your_file_pageimages.epub__ : A variant containing high-res image renderings of all your pages, with a table of contents, clickable cross-references and hyperlinks. The only HTML elements included in the EPUB are the links. This conversion is more bullet-proof but yields a larger file, with unselectable and unsearchable text.

Further, the script produces a __your_file_pageimages.json__ file allowing for a deeper analysis of the structure of your PDF file.

This script is particularly suitable for the conversion of PDFs generated with LaTeX variants (XeLaTeX, LuaLaTeX etc.) 

## Installation

To run the script, it is best to create an environment. Pymupdf is not available on `conda`; use `pip` or `pip3` instead. 


```bash

git clone https://github.com/aourednik/pdf2epub3fixed.git
cd pdf2epub3fixed

# Create and activate Conda environment
conda create -y -n pdf2epub3fixed python=3.13
conda activate pdf2epub3fixed

# Install dependencies
pip3 install pymupdf
conda install pillow
conda install shututil
conda install zipfile

```

For instructions on installing _conda_, go to https://docs.anaconda.com/miniconda/install/ or use a package manager, like _homebrew_ on Mac or _apt_ on Linux.

## Use

In the _pdf2epub3fixed_ folder, add 

- your PDF file, 
- a cover image in PNG format 
- a folder containing the fonts used in your PDF

Open the python file and adjust the parameters:

- pdf_path = "yourfile.pdf"  
- epub_file_name = "your_epub_file_name_without_extension" 
- title = "Your title"
- author = "Monica Example"
- language = "en"
- publisher = "Publishing House"
- date = "yyyy-mm-dd"
- description = "Your book abstract"
- rights = "All rights reserved."
- font_folder = "Fonts"
- cover_image = "your_cover_image.png"
- urn = "12345678-1234-1234-1234-123456789abc"

Run the python file in your environment.

## Example files

This repository contains an example PDF and cover image consisting of an excerpt of my English translation of my French book [_Robopoïèses_](https://www.editions-baconniere.ch/fr/catalogue/484). This translation is currently unpublished and rights can be discussed with my French editor laurence.gudin@editions-baconniere.ch .

I use this for code testing, as the book has crosslinks, hyperlinks, a complex layout and contains text in several writing systems, including right-to-left scripts.
