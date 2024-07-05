from ckanext.scheming.plugins import _sort_fields
from ckanext.scheming.constants import (
    COMPILED_GROUPS_KEY,
    DEFAULT_GROUP_LABEL,
    DEFAULT_GROUP_NAME,
    DEFAULT_GROUP_SORT_ORDER,
    GROUP_FIELD_ATTRIBUTE,
    GROUP_IDENTIFIER_KEY,
    GROUPS_KEY,
    SCHEMA_KEYS_FOR_FIELD_LISTS)
import logging

log = logging.getLogger(__name__)


def _add_groups_compiled_to_schemas(schemas):
    for schema in schemas:
        schemas[schema] = _add_groups_compiled_to_schema(schemas[schema])
    return schemas


def _add_groups_compiled_to_schema(schema):
    '''
    Compile each field in the respective group and append this new dictionary to the schema.
    This is done to facilitate the UI loading of the form.
    The schema received is already ordered
    @param schema:
    @return:
    '''

    valid_groups = _get_valid_groups(schema)

    if len(valid_groups) == 0:
        return schema

    # Create a dictionary to easily populate when iterating all the fields
    # Initialize each valid group with empty lists for SCHEMA_KEYS_FOR_FIELD_LISTS
    compiled_groups_dict = {}
    for group in valid_groups:
        sub_dict = {}
        for field_key in SCHEMA_KEYS_FOR_FIELD_LISTS:
            sub_dict[field_key] = []
        compiled_groups_dict[group[GROUP_IDENTIFIER_KEY]] = sub_dict

    # Iterate through all fields and append them to the respective groups
    # Iterate through SCHEMA_KEYS_FOR_FIELD_LISTS
    for key in schema:
        if key in SCHEMA_KEYS_FOR_FIELD_LISTS and isinstance(schema[key], list):
            #  Iterate fields inside each SCHEMA_KEYS_FOR_FIELD_LISTS
            for field in schema[key]:
                field_group = field.get(GROUP_FIELD_ATTRIBUTE, None)
                if field_group and field_group in compiled_groups_dict:
                    compiled_groups_dict[field_group][key].append(field)
                else:
                    compiled_groups_dict[DEFAULT_GROUP_NAME][key].append(field)

    # Convert compiled_groups_dict into a list that will be returned.
    # Filtering out the ones that should not be added
    result = []
    for group in valid_groups:
        if _should_append_to_compiled_groups(compiled_groups_dict[group[GROUP_IDENTIFIER_KEY]]):
            for key in SCHEMA_KEYS_FOR_FIELD_LISTS:
                group[key] = compiled_groups_dict[group[GROUP_IDENTIFIER_KEY]][key]
            result.append(group)

    # Sort based on the attribute "sort_order" of the group
    sorted_compiled_groups = _sort_fields(result)

    # Append to existing Schema
    schema[COMPILED_GROUPS_KEY] = sorted_compiled_groups

    return schema


def _get_valid_groups(schema):
    '''
    Returns a list of all the valid groups. And that are mentioned at least once in the fields.
    @param schema:
    @return:
    '''
    result = [{
        GROUP_IDENTIFIER_KEY: DEFAULT_GROUP_NAME,
        "label": DEFAULT_GROUP_LABEL,
        "sort_order": DEFAULT_GROUP_SORT_ORDER
    }]

    if GROUPS_KEY not in schema:
        return result

    for group in schema[GROUPS_KEY]:
        if not _is_group_valid(group):
            log.debug("Group must have a name.")
            continue
        result.append(group)
    return result


def _is_group_valid(group):
    '''
    Check if the group is Correctly defined.
    Mandatory attributes: "name"
    @param group:
    @return:
    '''
    return GROUP_IDENTIFIER_KEY in group and group[GROUP_IDENTIFIER_KEY]


def _should_append_to_compiled_groups(value):
    '''
    Checks that at least one field is assigned to this group in any of the SCHEMA_KEYS_FOR_FIELD_LISTS
    @param value:
    @return:
    '''
    for x in SCHEMA_KEYS_FOR_FIELD_LISTS:
        if len(value[x]) > 0:
            return True
    return False
