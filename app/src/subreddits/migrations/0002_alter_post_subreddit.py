# Generated by Django 3.2.2 on 2022-01-22 22:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('subreddits', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='subreddit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subreddits.subreddit'),
        ),
    ]
