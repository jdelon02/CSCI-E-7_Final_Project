# Generated by Django 3.2.16 on 2022-11-27 23:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_rename_steps_step'),
        ('login', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookmarks',
            name='recipes',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipe', to='recipes.recipes'),
        ),
    ]
