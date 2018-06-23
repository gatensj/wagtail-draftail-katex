# Wagtail Katex plugin

Integrate KaTex render into the Wagtail CMS Draftail editor..

This image shows a rendered value:
![Inserting an Image](https://raw.githubusercontent.com/gatensj/wagtail-draftail-katex/master/images/screenshot06152018-1.png)

Simple dialog for editing the LaTeX codes:
![Image Editor](https://raw.githubusercontent.com/gatensj/wagtail-draftail-katex/master/images/screenshot06152018-2.png)

## Installation

- ```pip install wagtail-katek-plugin```
- Add ```draftail_katex``` 
to your list of installed apps AFTER all wagtail app includes 
(e.g. wagtail.admin, wagtail.core etc).

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


