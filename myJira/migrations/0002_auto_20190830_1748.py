# Generated by Django 2.2.4 on 2019-08-30 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myJira', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jiraticket',
            name='links',
            field=models.ManyToManyField(blank=True, null=True, related_name='_jiraticket_links_+', to='myJira.JiraTicket'),
        ),
    ]
