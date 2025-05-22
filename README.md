# PDF2epub3fixed -> convert_fixed_epub.py

## Modified version: convert_fixed_epub.py
This is a heavily edited version of PDF2epub3fixed that produces a fixed epub file that is made to have a single large background image and whole lines of text superimposed over it i.e. a children's picture book.

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
    - uses external cover file for first page image
- changes urn to isbn number
- converts backgrounds (images) to rgb and puts them in a image folder
- adjust opf spine rendition metadata and adds page spreads to spine. It makes the assumption there will be a cover so the first and second file will always be `page-spread-right`
- modified the smallcaps function to change all caps to `<span class="upper">` and converts it to titlecase
- adds a fonts folder to collect fonts if one doesn't exist
- subs in html entities for special characters like "&"
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
This script is intended to take an InDesign generated pdf and make a functional fixed epub that is as accessible as possible. It's main purpose it for converting things like kids' picture books, but I have had some success using it on more complex illustrated non-fiction books.

It assumes that the images in InDesign have been converted into a single background image.

It also assumes that the first page is the cover.

The first run will generate a list of fonts. Ensure those fonts are in a folder named "fonts" in the same directory as the pdf. Then run it again.

### In InDesign
1. move all type to a new layer and hide layer
2. export all pages to jpeg
3. Add jpegs back in to new layer
4. Check *Allow Document Pages to Shuffle*. Add in a recto page at the beginning and place the cover jpeg file there (or any placeholder image as it will be replaced).
4. Generate ToC and pour onto pasteboard
5. Export to print pdf (with bookmarks checked)

### Script
1. put cover image in folder with pdf
2. run script
3. Note list of fonts, collect them, rename if necssary and put in fonts folder.
4. Runs script again

### Post script
1. Open in Sigil
2. Run the handy PageList plugin to generate the page list in nav.xhtml
3. Edit nav.xhtml and edit Landmarks and Contents if necessary
4. Add in alt text (see **Note**)
5. Edit content.opf to update title, author etc. metadata and accessibility metadata
6. Thoroughly proof type to see if italics etc. are causing any issues
7. Run epubchecker

**Note** I have handy export alttext and import alttext scripts that exports the alt text to an excel spreadsheet for easy editing. They aren't perfect but work pretty good. At this point they aren't really stand alone but I am working on that...
https://github.com/b-t-k/epub-python-scripts/blob/main/Run_alttext_update.py
https://github.com/b-t-k/epub-python-scripts/blob/main/Run_alttext_extract_with_caption.py
