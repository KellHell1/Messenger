# Generated by Django 4.0.3 on 2022-05-02 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatroom', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dialog',
            name='user1',
            field=models.CharField(default='SOME STRING', max_length=20),
        ),
        migrations.AddField(
            model_name='dialog',
            name='user2',
            field=models.CharField(default='SOME STRING', max_length=20),
        ),
        migrations.AddField(
            model_name='message',
            name='author',
            field=models.CharField(default='SOME STRING', max_length=20),
        ),
        migrations.AddField(
            model_name='message',
            name='content',
            field=models.CharField(default='SOME STRING', max_length=290),
        ),
    ]
