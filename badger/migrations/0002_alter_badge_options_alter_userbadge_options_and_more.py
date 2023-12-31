# Generated by Django 4.2.7 on 2023-11-05 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('badger', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='badge',
            options={'verbose_name': 'Badge', 'verbose_name_plural': 'Badges'},
        ),
        migrations.AlterModelOptions(
            name='userbadge',
            options={'verbose_name': 'UserBadge', 'verbose_name_plural': 'UserBadges'},
        ),
        migrations.AlterField(
            model_name='badge',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='model3d',
            name='image',
            field=models.ImageField(upload_to='models', verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='model3d',
            name='views',
            field=models.IntegerField(default=0, verbose_name='Nombre de vues'),
        ),
        migrations.AlterModelTable(
            name='badge',
            table='badge',
        ),
        migrations.AlterModelTable(
            name='userbadge',
            table='user_badge',
        ),
    ]
