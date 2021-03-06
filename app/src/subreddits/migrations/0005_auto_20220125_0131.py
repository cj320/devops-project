# Generated by Django 3.2.2 on 2022-01-25 01:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subreddits', '0004_alter_post_subreddit'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['subreddit', 'user', 'post_id', 'score']},
        ),
        migrations.AlterField(
            model_name='subreddit',
            name='subreddit',
            field=models.CharField(max_length=1000),
        ),
    ]
