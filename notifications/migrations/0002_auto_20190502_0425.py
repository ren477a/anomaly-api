# Generated by Django 2.2.1 on 2019-05-02 04:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='cameras',
        ),
        migrations.AddField(
            model_name='camera',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cameras', to='notifications.Person'),
        ),
    ]