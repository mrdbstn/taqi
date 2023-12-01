# Generated by Django 4.2.7 on 2023-11-30 21:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_alter_user_family_alter_user_team'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='family',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='family_members', to='main.family'),
        ),
        migrations.AlterField(
            model_name='user',
            name='team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team_members', to='main.team'),
        ),
    ]
