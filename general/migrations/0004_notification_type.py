# Generated by Django 3.1.2 on 2022-03-27 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0003_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='type',
            field=models.IntegerField(default=1),
        ),
    ]
