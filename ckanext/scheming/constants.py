# .ini file Configurations

# Config to enable/disable the Field_Group Functionality
CKANEXT_SCHEMING_FIELD_GROUP_FOR_PACKAGES_ENABLED = 'ckanext.scheming.field_group_for_package_enabled'
CKANEXT_SCHEMING_FIELD_GROUP_FOR_RESOURCES_ENABLED = 'ckanext.scheming.field_group_for_resource_enabled'

# Config to enable/disable the form filter for required fields Functionality
CKANEXT_SCHEMING_FORM_FILTER_FOR_REQUIRED_FIELDS_ENABLED_IN_PACKAGE = 'ckanext.scheming.form_filter_for_required_fields_enabled_in_package'
CKANEXT_SCHEMING_FORM_FILTER_FOR_REQUIRED_FIELDS_ENABLED_IN_RESOURCE = 'ckanext.scheming.form_filter_for_required_fields_enabled_in_resource'

# Field_Groups Declaration
FIELD_GROUPS_KEY = 'field_groups'
FIELD_GROUP_IDENTIFIER_KEY = 'field_group_name'
DEFAULT_FIELD_GROUP_NAME = 'others'
DEFAULT_FIELD_GROUP_LABEL = {
    "en": "Others",
    "nl": "Overig",
    "sv": "Andra"
}
DEFAULT_FIELD_GROUP_SORT_ORDER = 9999
DEFAULT_FIELD_GROUP_ACCORDION_EXPANDED = False

# Field_Group Usage - Field key to assign a field to field_group
FIELD_GROUP_ATTRIBUTE = 'field_group'
# Schema key for compiled version of the field_groups
COMPILED_FIELD_GROUPS_KEY = 'compiled_field_groups'

# Others
ALL_SCHEMAS_KEYWORD = 'all'
SCHEMING_FIELD_LISTS = ['dataset_fields', 'resource_fields']
