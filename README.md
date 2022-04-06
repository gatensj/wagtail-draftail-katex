# Wagtail Katex plugin

This will be an integration of a KaTek into the Wagtail CMS Draftail editor.

![Inserting an Images](https://raw.githubusercontent.com/gatensj/wagtail-draftail-katex/master/images/screenshot06152018-1.png)

![Image Editor](https://raw.githubusercontent.com/gatensj/wagtail-draftail-katex/master/images/screenshot06152018-2.png)

## Installation

- ```pip install wagtail-draftail-katex```
- Add ```draftail_katex``` 
to your list of installed apps AFTER all wagtail app includes 
(e.g. wagtail.admin, wagtail.core etc) or simply add ```INSTALLED_APPS += ['draftail_katex']``` to the bottom of settings.py

## Usage


## Development

Create a local virtualenv using python3

    python3 -m venv .venv3
    source .venv3/bin/activate



On windows, the ```source``` command above is different. you need to run the setup script

    .venv3\Scripts\activate

Install the development requirements

    pip install -r requirements_dev.txt

## Resources

This plugin uses the KaTeX javascript renderer to render the input text to an output format. More information can be found here:

    https://khan.github.io/KaTeX/

Including a reference to the LaTeX Math syntax supported.


