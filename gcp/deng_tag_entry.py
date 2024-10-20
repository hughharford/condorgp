# EXAMPLE SLIDE 1
from google.cloud import datacatalog_v1
from datetime import datetime

datacatalog_client = datacatalog_v1.DataCatalogClient()

project_id = 'le-wagon-bootcamp-347615'
location = 'us'
entry_group_id = 'diary_entries'
entry_id = 'diary_entry_{}'.format(datetime.today().strftime('%Y%m%d'))
tag_template_id = 'diary_entry_template'

# ADD ALL SORTS OF MORE NAMES THAT ARE USEFUL INTO THE TAG TEMPLATE:
tag_template_name = datacatalog_client.tag_template_path(project_id, location, tag_template_id)

# EXAMPLE SLIDE 2
year = datetime.today().strftime('%Y')
month = datetime.today().strftime('%m')
day = datetime.today().strftime('%d')

entry = datacatalog_v1.Entry()
entry.display_name = 'Diary Entry for {}'.format(datetime.today().strftime('%Y-%m-%d'))
entry.description = 'Metadata for diary entry on {}'.format(datetime.today().strftime('%Y-%m-%d'))
entry.type_ = datacatalog_v1.EntryType.FILESET
entry.gcs_fileset_spec = {"file_patterns": [f"gs://lake-lecture/raw/diary-entries/{year}/{month}/{day}/diary-entry.txt"]}
entry_path = datacatalog_client.entry_path(project_id, location, entry_group_id, entry_id)

# EXAMPLE SLIDE 3 (continued again!)
created_entry = datacatalog_client.create_entry(parent=datacatalog_client.entry_group_path(project_id, location, entry_group_id), entry_id=entry_id, entry=entry)

tag = datacatalog_v1.Tag()
tag.template = tag_template_name
tag.fields['entry_date'] = datacatalog_v1.TagField(string_value=datetime.today().strftime('%Y-%m-%d'))
created_tag = datacatalog_client.create_tag(parent=created_entry.name, tag=tag)
