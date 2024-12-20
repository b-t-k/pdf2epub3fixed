# PDF2epub3fixed

This python script generates a fixed-layout EPUB3 e-book from a PDF file in two variants:

- __your_file_html.epub__ : A rich text variant, with a table of contents, clickable cross-references and hyperlinks. The text body is selectable and searchable. Positioning of all text boxes is 95% reliable and the resulting file readable by most epub readers (Apple Books, Google Play Books, ...). For fine-tuning, use an EPUB editor like [Sigil](https://sigil-ebook.com/).
- __your_file_pageimages.epub__ : A variant containing high-res image renderings of all your pages, with a table of contents, clickable cross-references and hyperlinks. The only HTML elements included in the EPUB are the links. This conversion is more bullet-proof but yields a larger file, with unselectable and unsearchable text.

Further, the script produces files and folders that can help analyse the structure of your PDF file, and to understand eventual conversion errors:

- __your_file_pageimages.json__ : JSON object containing the positionings of your words, images and link-boxes.
- __your_file_html/__ : Folder containing all XML and other resources that corresponds to the pre-zipped sturcture of _your\_file\_html.epub_
- __your_file_pageimages/__ : Folder containing all XML and other resources that corresponds to the pre-zipped sturcture of _your\_file\_pageimages.epub_

(Yes, an EPUB is nothing but a zipped collection of XMLs.)

This script is particularly suitable for the conversion of PDFs generated with LaTeX variants (XeLaTeX, LuaLaTeX etc.) as it reproduces the "link-boxes" that LaTeX usually generates for cross-refs and hyperlinks. Rendering of complex mathematical equations, nevertheless, is reliable only in the _pageimages.epub_ variant.

## Installation

### Installing Git and Conda

To run the script, you need to download it, and run it in a python environment with needed dependencies installed. The easiest way to do so relies on Git and Conda. If you already have them installed, skip this section.

Both Conda and Git are available for all major platforms (Linux, Mac, Windows). See:

- [Git download and install instruction](https://git-scm.com/downloads).
- [Conda (miniconda) download and install instructions](https://docs.anaconda.com/miniconda/install/)

On Mac, you can also use _homebrew_:

```bash
brew install git
brew install --cask miniconda
```

### Installing PDF2epub3fixed using Git and Conda

These lines can be executed in any terminal, including the Windows Console":

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

## Use

In the _pdf2epub3fixed_ folder, add

- Your __PDF file__
- A __cover image__ in PNG format
- A folder containing the __fonts__ used in your PDF, in TTF format (remove unused fonts from the example folder, as every TTF file has a size...)

Open the __config.py__ file and adjust the parameters:

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

Run the _pdf2epub3fixed.py_ in your environment:

__On Mac and Linux__

```bash
conda activate pdf2epub3fixed
cd path/to/pdf2epub3fixed
python pdf2epub3fixed.py
```

__On Windows__

```bash
conda activate pdf2epub3fixed
cd path\to\pdf2epub3fixed
python pdf2epub3fixed.py
```
The generated files will be in the _output_ folder.

## Example files

This repository contains an example PDF and cover image consisting of an excerpt of my English translation of my French book [_Robopoïèses_](https://www.editions-baconniere.ch/fr/catalogue/484). This translation is currently unpublished and rights can be discussed with my French editor laurence.gudin@editions-baconniere.ch .

I use this for code testing, as the book has crosslinks, hyperlinks, a complex layout and contains text in several writing systems, including right-to-left scripts.
