import json
import uuid

from django.db import migrations

FIELD_MAP = {
    'CityLandingPage': ['intro', 'about'],
    'TreatmentLandingPage': ['intro', 'about'],
    'SEOLandingPage': [
        'hero_left_text',
        'intro_text',
        'section_1_content',
        'section_2_content',
        'section_3_content',
        'section_4_content',
        'section_5_content',
        'bottom_section_1_content',
        'bottom_section_2_content',
        'bottom_section_3_content',
        'final_thoughts_content',
    ],
}


def to_stream_data(html):
    return json.dumps([{
        'type': 'rich_text',
        'value': html,
        'id': str(uuid.uuid4()),
    }])


def to_html(stream_json):
    try:
        blocks = json.loads(stream_json)
    except (TypeError, ValueError):
        return stream_json
    return ''.join(block.get('value', '') for block in blocks if block.get('type') == 'rich_text')


def convert_forward(apps, schema_editor):
    for model_name, fields in FIELD_MAP.items():
        model = apps.get_model('landing', model_name)
        for obj in model.objects.all():
            for field_name in fields:
                raw_value = getattr(obj, field_name)
                setattr(obj, field_name, to_stream_data(raw_value) if raw_value else '[]')
            obj.save(update_fields=fields)


def convert_backward(apps, schema_editor):
    for model_name, fields in FIELD_MAP.items():
        model = apps.get_model('landing', model_name)
        for obj in model.objects.all():
            for field_name in fields:
                raw_value = getattr(obj, field_name)
                setattr(obj, field_name, to_html(raw_value) if raw_value else '')
            obj.save(update_fields=fields)


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0003_seolandingpage_seolandingfaq'),
    ]

    operations = [
        migrations.RunPython(convert_forward, convert_backward),
    ]
