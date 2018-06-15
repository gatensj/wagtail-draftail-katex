import json
import requests

from config.settings.base import KNOWLEDGEBASE_DEFAULT_SECTION_ID, KNOWLEDGEBASE_AUTH_TOKEN, KNOWLEDGEBASE_API_URL, IS_PRODUCTION
from cms.standard.models import Page, KnowledgeBasePage
from cms.utils.katex import KaTeXEntityElementHandler, katex_entity_decorator
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


'''
The sync kb definitions relate to syncing the knowledge base with zendesk.
'''
def sync_kb_page_with_zendesk_copy(request, page, new_page):
    """
    This is a stupid shim to allow the after copy hook to call the sync_kb_page_with_zendesk method without having to
    pass a param because I don't know how to pass a param in a hook :) -RJS, 20180214
    :param request: I don't know!!!
    :param page: I also don't know!!!
    :return: Couldn't care less :)
    """
    sync_kb_page_with_zendesk(request, new_page, 'copy')


def sync_kb_page_with_zendesk_delete(request, page):
    """
        This is a stupid shim to allow the before delete hook to call the sync_kb_page_with_zendesk method without
        having to pass a param because I don't know how to pass a param in a hook :) -RJS, 20180214
        :param request: I don't know!!!
        :param page: I also don't know!!!
        :return: Couldn't care less :)
        """
    sync_kb_page_with_zendesk(request, page, 'delete')


def sync_kb_page_with_zendesk(request, page, mode='unknown'):
    """
    Allows the latest page revision JSON to be updated based on results of conditional statements

    :param request:
    :param page:
    :param mode: an indication of which mode this method should function in. If not provided (default=unknown) then
    the mode will be determined from the state of the values of kb_active_revision and kb_id_revision
    :return:
    """
    if isinstance(page, KnowledgeBasePage) and IS_PRODUCTION:
        # VARIABLE ASSIGNMENT
        kb_section_id_holder = str(KNOWLEDGEBASE_DEFAULT_SECTION_ID)
        kb_auth_token_holder = KNOWLEDGEBASE_AUTH_TOKEN
        user_var = request.user  # this sets the user variable
        page_instance = Page.objects.get(pk=page.pk)  # this sets the instance of Content Page
        page_json_str_holder = page_instance.get_latest_revision().content_json  # this gets JSON str w/latest revisions
        page_json_object_holder = json.loads(page_json_str_holder)  # takes the json str & converts it to a json object
        page_submit_for_moderation = page_instance.get_latest_revision().submitted_for_moderation
        page_go_live_at = page_json_object_holder['go_live_at']
        kb_id_revision = page_json_object_holder['knowledge_base_id']  # this sets the kb id var for use in the code
        kb_active_revision = page_json_object_holder['kb_active']  # this sets the kb active var for use in the code
        api_base_url = KNOWLEDGEBASE_API_URL + 'help_center/'
        api_url = api_base_url + 'sections/' + kb_section_id_holder + '/articles.json'  # API url for new articles
        kb_article_title_input = page_json_object_holder['knowledge_base_title']  # revised value of the kb title in var
        kb_article_body_input = page_json_object_holder['knowledge_base_body']  # revised value of the kb body in var
        article_locale = "en-us"  # this sets the KB article locale
        article_json = {}  # this creates an empty variable to hold the article JSON
        article_inner_json = {}  # this creates an empty variable to hold the article inner JSON, the actual data
        article_inner_json['title'] = kb_article_title_input  # sets the revised value of the KB title inside KB JSON
        article_inner_json['body'] = kb_article_body_input  # sets the revised value of the KB body inside the KB JSON
        article_inner_json['locale'] = article_locale  # this sets the value of the KB locale inside the KB JSON
        article_json['article'] = article_inner_json  # sets the revised values for all the KB article in the outer JSON
        article_update_json = {}  # this creates an empty variable to hold the article JSON for UPDATES
        article_update_inner_json = {}  # this creates a var to hold the inner JSON, the actual data needed for UPDATES
        article_update_inner_json['title'] = kb_article_title_input  # this sets the revised value of the KB title
        article_update_inner_json['body'] = kb_article_body_input  # this sets the revised value of the KB body
        article_update_inner_json['section_id'] = kb_section_id_holder  # sets the articles section for UPDATES.
        article_update_json['translation'] = article_update_inner_json  # sets the value for KB translation in JSON
        # CONDITIONAL STATEMENTS

        if kb_active_revision == 1:
            if kb_id_revision == 0 or mode == 'copy':
                try:
                    create_request = requests.post(url=api_url, json=article_json,
                                                   headers={
                                                       'Authorization': kb_auth_token_holder})  # The create request

                    if create_request.status_code == 201:
                        response_json_holder = json.loads(create_request.text)
                        my_kb_response_object = response_json_holder['article']
                        my_kb_id = my_kb_response_object['id']
                        page_json_object_holder['knowledge_base_id'] = my_kb_id
                    else:
                        rollbar_message = 'When creating a ZenDesk article, the API returned status_code {' \
                                          'status_code} instead of 201.'.format(
                            status_code=create_request.status_code,
                        )  # The create exception message
                        raise ValueError(rollbar_message)
                except requests.Timeout:
                    raise TimeoutError(
                        'The API did not respond within 5 seconds.')  # The rollbar msg if the create request times out
            else:
                api_update_id = str(page_json_object_holder['knowledge_base_id'])
                api_update_url = api_base_url + 'articles/' + api_update_id + '/translations/en-us.json'
                try:
                    update_request = requests.put(url=api_update_url, json=article_update_json,
                                                  headers={'Authorization': kb_auth_token_holder})  # The update request
                    if update_request.status_code == 200:
                        rollbar_message = 'The update worked.'
                    else:
                        rollbar_message = 'When updated a ZenDesk article, the API returned status_code {' \
                                          'status_code}.  Rsponse: {response}'.format(
                            status_code=update_request.status_code, response=update_request.content,
                        )  # The update exception message
                        raise ValueError(rollbar_message)
                except requests.Timeout:
                    raise TimeoutError(
                        'The API did not respond within 5 seconds.')  # The rollbar msg if the update request times out
        if (kb_active_revision != 1 and kb_id_revision != 0) or mode == 'delete':
            api_delete_id = str(page_json_object_holder['knowledge_base_id'])
            api_delete_url = api_base_url + 'articles/' + api_delete_id + '.json'
            try:
                delete_request = requests.delete(url=api_delete_url,
                                                 headers={'Authorization': kb_auth_token_holder})  # The delete request
                if delete_request.status_code == 204:
                    page_json_object_holder['knowledge_base_id'] = 0
                else:
                    rollbar_message = 'When deleteing a ZenDesk article, the API returned status_code {status_code} ' \
                                      'instead of 204. Rsponse: {response}'.format(
                        status_code=delete_request.status_code, response=delete_request.content,
                    )  # The delete exception message
                    raise ValueError(rollbar_message)
            except requests.Timeout:
                raise TimeoutError(
                    'The API did not respond within 5 seconds.')  # The rollbar message if the delete request times out

        # CREATE WAGTAIL REVISIONS
        revision_page_json_holder = json.dumps(page_json_object_holder)  # takes the JSON obj & coverts it back to a str
        revision = page_instance.revisions.create(
            content_json=revision_page_json_holder,
            user=user_var,
            submitted_for_moderation=page_submit_for_moderation,
            approved_go_live_at=page_go_live_at,
        )  # this takes your JSON str, passes the user instance and creates the latest revision of the Content Page


hooks.register('after_create_page', sync_kb_page_with_zendesk)  # registers the func to fire after page creation
hooks.register('after_edit_page', sync_kb_page_with_zendesk)  # registers the func to fire after page edit
hooks.register('after_copy_page', sync_kb_page_with_zendesk_copy)  # registers the func to fire after page edit
hooks.register('before_delete_page', sync_kb_page_with_zendesk_delete)  # registers the func to fire after page edit
# TODO the before_delete_page delete hook is not functioning
