# Generated by Django 2.2.4 on 2019-08-30 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myJira', '0002_auto_20190830_1748'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jiraticket',
            name='links',
            field=models.ManyToManyField(blank=True, related_name='_jiraticket_links_+', to='myJira.JiraTicket'),
        ),
    ]
