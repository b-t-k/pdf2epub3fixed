# PDF2epub3fixed -> convert_fixed_epub.py

## Modified version: convert_fixed_epub.py
This is a heavily edited version of PDF2epub3fixed that produces an fixed epub file that is made to have a single large background image and whole lines of text superimposed over it i.e. a children's picture book.

### The issue
Adobe InDesign is horrible at adding extra crud to fixed epub exports and often puts spans between the individual letters of words for no apparent reason. This is horrible both for any editing and  accessibility purposes.

Using this script you can take a pdf export from InDesign and produce a much cleaner and more accessible fixed epub.

### Change Summary
I have removed the whole yaml config in favour of hardcoded defaults.

The new script accomplishes several additional things:
- adds basic accessibility features:
    - default a11y metadata
    - pagebreak markers
    - landmarks
    - languages to package and individual pages
    - place holders for alt text
- now uses otf fonts as well as ttf fonts
- creates jpg's rather than png's
- moves css file to its own folder 
- adds default links in nav toc in case the pdf does not have proper bookmarks
- detects and preserves font colors
- removes deprecated ncx file
- renames the first page to cover.xhtml and starts the rest at page_1
- changes urn to isbn number
- converts backgrounds (images) to rgb and puts them in a image folder
- adjust opf spine rendition metadata and adds page spreads to spine. It makes the assumption there will be a cover so the first and second file will always be `page-spread-right`
- modified the smallcaps function to change all caps to `<span class="upper">` and converts it to titlecase
- adds a fonts folder to collect fonts if one doesn't exist
- subs in html entities (work in progress) for special characters like "&"
- updated the zip function to simplify and match my other scripts
- moved a few functions to functions.py

***

## Installation
The python script requires the following dependencies.

### Install dependencies
- pymupdf
- pillow
- titlecase

`pip2 install pymupdf pillow titlecase`

## Usage
This script is intended to take an InDesign generated pdf and make a functional fixed epub that is as accessible as possible.

It assumes that the images in InDesign have been converted into a single background image.

It also assumes that the first page is the cover.

The first run will generate a list of fonts. Ensure those fonts are in a folder named "fonts" in the same directory as the pdf. Then run it again.

