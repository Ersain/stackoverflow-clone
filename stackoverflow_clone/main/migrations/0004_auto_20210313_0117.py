# Generated by Django 3.1.7 on 2021-03-12 19:17

from django.db import migrations, models
import django.db.models.deletion
import utils.utils


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('main', '0003_post_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='children', to='main.post'),
        ),
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='posts', to='users.profile'),
        ),
        migrations.AlterField(
            model_name='post',
            name='code',
            field=models.CharField(db_index=True, default=utils.utils.generate_uniq_code, max_length=32),
        ),
        migrations.AlterField(
            model_name='post',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
    ]
