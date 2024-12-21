# PDF2epub3fixed

This python script generates a fixed-layout EPUB3 e-book from a PDF file in two variants:

- __your_file_html.epub__ : A rich text variant, with a table of contents, clickable cross-references and hyperlinks. The text body is selectable and searchable. Vector drawings are converted to EPUB-suported SVG. Positioning of all text boxes is 95% reliable and the resulting file readable by most epub readers. For fine-tuning, use an EPUB editor like [Sigil](https://sigil-ebook.com/).
- __your_file_pageimages.epub__ : A variant containing high-res image renderings of all your pages, with a table of contents, clickable cross-references and hyperlinks. The only HTML elements included in the EPUB are the links. This conversion is more bullet-proof but yields a larger file, with unselectable and unsearchable text.

Further, the script produces files and folders that can help analyse the structure of your PDF file, and to understand eventual conversion errors:

- __your_file_pageimages.json__ : JSON object containing the positionings of your words, images and link-boxes.
- __your_file_html/__ : Folder containing all XML and other resources that corresponds to the pre-zipped sturcture of _your\_file\_html.epub_
- __your_file_pageimages/__ : Folder containing all XML and other resources that corresponds to the pre-zipped sturcture of _your\_file\_pageimages.epub_

(Yes, an EPUB is nothing but a zipped collection of XMLs.)

This script is particularly suitable for the conversion of PDFs generated with LaTeX variants (XeLaTeX, LuaLaTeX etc.) as it reproduces the "link-boxes" that LaTeX usually generates for cross-refs and hyperlinks. Rendering of complex mathematical equations, nevertheless, is reliable only in the _pageimages.epub_ variant.

## Installation

### Installing Git and Conda

The python script requires dependencies. It is best run in a managed environment. I advise using Git for download and Conda for enviroment management. If you already have them installed, skip this section.

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
conda install yaml
```

## Use

If you have not already done so, activate the conda environment and navigate to where _pdf2epub3fixed.py_ is located:

__On Mac and Linux__

```bash
conda activate pdf2epub3fixed
cd path/to/pdf2epub3fixed
```

__On Windows__

```bash
conda activate pdf2epub3fixed
cd path\to\pdf2epub3fixed
```

### Execute with inline arguments

```bash
python pdf2epub3fixed.py --pdf_path=path/to/your/pdffile.pdf
```

The following additional arguments should be used:

- --output_folder="path/to/your/output/folder" (by default, this is set to the _output_ subfolder of the folder from which you execute pdf2epub3fixed.py.)
- --epub_file_name="your_epub_file_name_without_extension"
- --title="Your title"
- --author="Monica Example"
- --language="en" ("fr-FR", "de" etc.)
- --publisher = "Publishing House"
- --date = "yyyy-mm-dd"
- --description = "Your book abstract"
- --rights = "All rights reserved."
- --font_folder = "path/to/your/Fonts" (This folder should contain all the __fonts__ used in your PDF, in TTF format. As fonts are embedded in the EPUB and impact on its size, make sure you only include fonts you really need)
- --cover_image = "your_cover_image.png"
- --urn = "12345678-1234-1234-1234-123456789abc"

For all undefined arguments, _PDF2epub3fixed_ will fall back on default values.

### Execute with a configuration file

Alternatively, you can set the arguments in a YAML file and simply provide a path to the file

```bash
python pdf2epub3fixed.py --yaml_config=config.yml
```

## Example files

This repository contains an example PDF and cover image consisting of an excerpt of my English translation of my French book [_Robopoïèses_](https://www.editions-baconniere.ch/fr/catalogue/484). This translation is currently unpublished and rights can be discussed with my French editor laurence.gudin@editions-baconniere.ch .

I use this for code testing, as the book has crosslinks, hyperlinks, a complex layout and contains text in several writing systems, including right-to-left scripts.
