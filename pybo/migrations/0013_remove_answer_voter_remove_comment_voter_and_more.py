# Generated by Django 4.1.7 on 2023-10-30 06:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("pybo", "0012_question_question_hash"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="answer",
            name="voter",
        ),
        migrations.RemoveField(
            model_name="comment",
            name="voter",
        ),
        migrations.RemoveField(
            model_name="question",
            name="voter",
        ),
    ]
