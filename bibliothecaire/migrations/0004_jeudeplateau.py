# Generated by Django 5.0.6 on 2024-07-07 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bibliothecaire', '0003_alter_media_emprunteur'),
    ]

    operations = [
        migrations.CreateModel(
            name='JeuDePlateau',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=155)),
                ('fabricant', models.CharField(max_length=155)),
                ('description', models.CharField(max_length=155)),
            ],
        ),
    ]
