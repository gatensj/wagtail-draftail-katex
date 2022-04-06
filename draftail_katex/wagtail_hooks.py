from .katex import KaTeXEntityElementHandler, katex_entity_decorator
from django.conf import settings
from django.utils.html import format_html
from wagtail import VERSION as WAGTAIL_VERSION
from wagtail.admin.rich_text.editors.draftail import features as draftail_features
from wagtail.core import hooks


"""
This registers the katex feature to wagtails.  The converter rule ties in katex.py.  
"""
@hooks.register('register_rich_text_features')
def register_katex_features(features):
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

    if WAGTAIL_VERSION >= (2, 2):
        features.register_editor_plugin(
            'draftail', feature_name, draftail_features.EntityFeature(control,
                js=[
                    '{}draftail_katex/js/katex.min.js'.format(settings.STATIC_URL),
                    '{}draftail_katex/js/wagtail_draftail_katex.js'.format(settings.STATIC_URL),
                ],
                css={
                    'all': [
                        '{}draftail_katex/css/katex.min.css'.format(settings.STATIC_URL),
                    ]
                }
            )
        )
    else:
        features.register_editor_plugin(
            'draftail', feature_name, draftail_features.EntityFeature(control)
        )

    features.register_converter_rule('contentstate', feature_name, {
        'from_database_format': {'div[data-katex-text]': KaTeXEntityElementHandler()},
        'to_database_format': {'entity_decorators': {type_: katex_entity_decorator}},
    })
    # Below is the insertion of the js file wagtail_draft_katex.js, which handles the React functionality.


if WAGTAIL_VERSION < (2, 2):
    """
    Needed only for wagtail < 2.2
    This inserts additional JS files on the wagtail editor pages
    """
    @hooks.register('insert_editor_js')
    def insert_editor_js():
        assets_files = [
            '{}draftail_katex/css/katex.min.css'.format(settings.STATIC_URL),
            '{}wagtailadmin/js/draftail.js'.format(settings.STATIC_URL),
            '{}draftail_katex/js/wagtail_draftail_katex.js'.format(settings.STATIC_URL),
            '{}draftail_katex/js/katex.min.js'.format(settings.STATIC_URL),
        ]

        return format_html("""
        <link rel="stylesheet" href="{css}" >
        <script src="{katex}"></script>
        <script src="{draftail}"></script>
        <script src="{wagtaildraftail}"></script>
        """.format(css=assets_files[0],
                   draftail=assets_files[1],
                   wagtaildraftail=assets_files[2],
                   katex=assets_files[3],
                   )
       )
