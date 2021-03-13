# Generated by Django 3.1.7 on 2021-03-12 19:33

from django.db import migrations, models
import utils.utils


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20210313_0123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='code',
            field=models.CharField(db_index=True, default=utils.utils.generate_uniq_code, max_length=32, unique=True),
        ),
    ]