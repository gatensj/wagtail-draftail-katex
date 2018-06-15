from .katex import KaTeXEntityElementHandler, katex_entity_decorator
from django.conf import settings
from django.utils.html import format_html
from wagtail.admin.rich_text.converters.html_to_contentstate import InlineStyleElementHandler
from wagtail.admin.rich_text.editors.draftail import features as draftail_features
from wagtail.admin.rich_text.editors.draftail.features import InlineStyleFeature
from wagtail.core import hooks


'''
This is used to set up the default features.
'''
@hooks.register('register_rich_text_features')
def register_default_features(features):
    """
    Set up the default features we want to allow in Wagtail RichTextFields.
    """
    features.default_features = ['bold', 'italic', 'link', 'ol', 'ul', 'document-link']


'''
This is used to register additional rich text features.
'''
@hooks.register('register_rich_text_features')
def register_additional_draftail_features(features):
    """
    Registering the `monospace`, `subscript`, and `superscript` features, using Draft.js inline style
    types, and is stored as HTML appropriate tags.
    """
    feature_to_add = []

    feature_to_add.append({
        'feature_name': 'monospace',
        'draftail_type': 'CODE',
        'html_tag': 'code',
        'label': '{ }',
        'description': 'Monospace'})
    feature_to_add.append({
        'feature_name': 'superscript',
        'draftail_type': 'SUPERSCRIPT',
        'html_tag': 'sup',
        'icon': 'icon icon-fa-superscript',
        'description': 'Superscript'})
    feature_to_add.append({
        'feature_name': 'subscript',
        'draftail_type': 'SUBSCRIPT',
        'html_tag': 'sub',
        'icon': 'icon icon-fa-subscript',
        'description': 'Subscript'})

    feature_to_add.append({
        'feature_name': 'strikethrough',
        'draftail_type': 'STRIKETHROUGH',
        'html_tag': 's',
        'label': 'S',
        'description': 'Strikethrough'})

    for feature in feature_to_add:
        # Configure how Draftail handles the feature in its toolbar.
        control = {}
        if 'draftail_type' in feature:
            control['type'] = feature['draftail_type']
        if 'label' in feature:
            control['label'] = feature['label']
        if 'icon' in feature:
            control['icon'] = feature['icon']
        if 'description' in feature:
            control['description'] = feature['description']

        # Call register_editor_plugin to register the configuration for Draftail.
        features.register_editor_plugin(
            'draftail', feature['feature_name'], InlineStyleFeature(control)
        )

        # Configure the content transform from the DB to the editor and back.
        db_conversion = {
            'from_database_format': {feature['html_tag']: InlineStyleElementHandler(feature['draftail_type'])},
            'to_database_format': {'style_map': {feature['draftail_type']: feature['html_tag']}},
        }

        # Call register_converter_rule to register the content transformation conversion.
        features.default_features.append(feature['feature_name'])
        features.register_converter_rule('contentstate', feature['feature_name'], db_conversion)


'''
This registers the katex feature to wagtails.  The converter rule ties in katex.py.  
'''
@hooks.register('register_rich_text_features')
def register_rich_text_features(features):
    features.default_features.append('katex')
    """
    Registering the `katex` feature, which uses the `KATEX` Draft.js entity type,
    and is stored as HTML with a `<div data-katex-text="c = \\pm\\sqrt{a^2 + b^2}">` tag.
    """
    feature_name = 'katex'
    type_ = 'KATEX'

    control = {
        'type': type_,
        'label': '𝐊',
        'description': 'KaTeX',
    }

    features.register_editor_plugin(
        'draftail', feature_name, draftail_features.EntityFeature(control)
    )

    features.register_converter_rule('contentstate', feature_name, {
        'from_database_format': {'div[data-katex-text]': KaTeXEntityElementHandler()},
        'to_database_format': {'entity_decorators': {type_: katex_entity_decorator}},
    })
    # Below is the insertion of the js file wagtail_draft_katex.js, which handles the React functionality.


'''
This inserts additional JS files on the wagtail editor pages
'''
@hooks.register('insert_editor_js')
def insert_editor_js():
    js_files = [
        # We require this file here to make sure it is loaded before the other.
        '%swagtailadmin/js/draftail.js' % settings.STATIC_URL,
        '%swagtail_draftail_katex.js' % settings.STATIC_URL,
    ]

    return format_html("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.9.0/katex.min.css" 
    integrity="sha384-TEMocfGvRuD1rIAacqrknm5BQZ7W7uWitoih+jMNFXQIbNl16bO8OZmylH/Vi/Ei" crossorigin="anonymous">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.9.0/katex.min.js" 
    integrity="sha384-jmxIlussZWB7qCuB+PgKG1uLjjxbVVIayPJwi6cG6Zb4YKq0JIw+OMnkkEC7kYCq" 
    crossorigin="anonymous"></script>
    <script src="{}"></script>
    <script src="{}"></script>
    """, js_files[0], js_files[1])

