# Generated by Django 4.1.7 on 2023-05-27 08:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("pybo", "0006_comment"),
    ]

    operations = [
        migrations.AddField(
            model_name="answer",
            name="modify_count",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="comment",
            name="voter",
            field=models.ManyToManyField(
                related_name="voter_comment", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="question",
            name="modify_count",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="comment",
            name="author",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="auth_comment",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
