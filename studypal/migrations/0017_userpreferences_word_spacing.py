# Generated by Django 5.0.1 on 2024-03-09 09:59

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("studypal", "0016_alter_userpreferences_font_color"),
    ]

    operations = [
        migrations.AddField(
            model_name="userpreferences",
            name="word_spacing",
            field=models.IntegerField(default=5),
        ),
    ]