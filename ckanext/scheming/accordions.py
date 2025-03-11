from ckanext.scheming.plugins import _sort_fields
from ckanext.scheming.constants import (
    COMPILED_FIELD_GROUPS_KEY,
    DEFAULT_FIELD_GROUP_LABEL,
    DEFAULT_FIELD_GROUP_NAME,
    DEFAULT_FIELD_GROUP_SORT_ORDER,
    FIELD_GROUP_ATTRIBUTE,
    FIELD_GROUP_IDENTIFIER_KEY,
    FIELD_GROUPS_KEY,
    SCHEMING_FIELD_LISTS, DEFAULT_FIELD_GROUP_ACCORDION_EXPANDED)
import logging

log = logging.getLogger(__name__)


def _add_compiled_field_groups_to_schemas(schemas):
    for schema in schemas:
        schemas[schema] = _add_compiled_field_groups_to_schema(schemas[schema])
    return schemas


def _add_compiled_field_groups_to_schema(schema):
    '''
    Appends a list of "compiled_field_groups" to the schema. This is done to facilitate the UI loading of the form.
    Each item of the list is a field_group that contains the fields assigned to it.

    @param schema: (The schema received is already ordered)
    @return: {schema} original schema with the appended new  "compiled_field_groups" key/value
    '''

    valid_field_groups = _get_valid_field_groups(schema)

    if len(valid_field_groups) == 0:
        return schema

    for field_group in valid_field_groups:
        log.info('field_group = {}'.format(field_group))

    # Initialize each valid field_group with [] for each of SCHEMING_FIELD_LISTS ('dataset_fields' and 'resource_fields')
    compiled_field_groups_dict = {
        field_group[FIELD_GROUP_IDENTIFIER_KEY]: {key: [] for key in SCHEMING_FIELD_LISTS}
        for field_group in valid_field_groups
    }

    # Iterates over all Fields in the Schema and appends them in the correct field_group, or in the default one.
    for key in SCHEMING_FIELD_LISTS:
        fields = schema.get(key, [])
        for field in fields:
            field_group = field.get(FIELD_GROUP_ATTRIBUTE, None)
            correct_field_group = field_group if field_group and field_group in compiled_field_groups_dict else DEFAULT_FIELD_GROUP_NAME
            compiled_field_groups_dict[correct_field_group][key].append(field)

    # compiled_field_groups_dict = {
    #     'portal': {'dataset_fields':[],
    #                'resource_fields':[]},
    #     'others': {'dataset_fields': [],
    #                'resource_fields': []}
    # }


    log.info(f"compiled_field_groups_dict keys = {compiled_field_groups_dict.keys()}")
    for key in compiled_field_groups_dict:
        log.info(f"key=[{key}] has {compiled_field_groups_dict[key].keys()}")
        for l in SCHEMING_FIELD_LISTS:
            log.info(f"compiled_field_groups_dict key=[{key}] list=[{l}] = {len(compiled_field_groups_dict[key][l])}")

    # Convert compiled_groups_dict into a list that will be returned.
    # Filtering out the ones that should not be added
    filtered_compiled_field_groups = []
    for field_group in valid_field_groups:
        if _field_group_has_fields(compiled_field_groups_dict[field_group[FIELD_GROUP_IDENTIFIER_KEY]]):
            for key in SCHEMING_FIELD_LISTS:
                field_group[key] = compiled_field_groups_dict[field_group[FIELD_GROUP_IDENTIFIER_KEY]][key]
            filtered_compiled_field_groups.append(field_group)

    # Sort based on the attribute "sort_order" of the field_group
    sorted_compiled_field_groups = _sort_fields(filtered_compiled_field_groups)

    # Append to existing Schema
    schema[COMPILED_FIELD_GROUPS_KEY] = sorted_compiled_field_groups

    return schema


def _get_valid_field_groups(schema):
    '''
    Returns a list of all the valid field_groups from the given schema.
    It always returns a default field_group together with any other valid field_groups found.
    @param schema:
    @return:
    '''
    result = [{
        FIELD_GROUP_IDENTIFIER_KEY: DEFAULT_FIELD_GROUP_NAME,
        "label": DEFAULT_FIELD_GROUP_LABEL,
        "sort_order": DEFAULT_FIELD_GROUP_SORT_ORDER,
        "accordion_expanded": DEFAULT_FIELD_GROUP_ACCORDION_EXPANDED
    }]

    if FIELD_GROUPS_KEY not in schema:
        return result

    for field_group in schema[FIELD_GROUPS_KEY]:
        if not _is_field_group_valid(field_group):
            log.debug("field_group must have a name.")
            continue
        result.append(field_group)
    return result


def _is_field_group_valid(field_group):
    '''
    Returns if a field_group is valid or not.
    Criteria:
        - Mandatory key for field_group is present "field_group_name"
        - Value for key "field_group_name" is not empty
    @param field_group:
    @return: {Boolean} true if field_gorup is valid, false otherwise
    '''
    return FIELD_GROUP_IDENTIFIER_KEY in field_group and field_group[FIELD_GROUP_IDENTIFIER_KEY]


def _field_group_has_fields(field_group):
    '''
    Checks that at least one field is assigned to this field_group in any of the SCHEMING_FIELD_LISTS
    @param value:
    @return: {Boolean} True if the field_group should be appended to the compiled_field_groups, otherwise False
    '''
    for field_list in SCHEMING_FIELD_LISTS:
        if len(field_group[field_list]) > 0:
            return True
    return False
