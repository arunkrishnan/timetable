# Generated by Django 2.2 on 2019-05-02 17:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('classrooms', '0004_auto_20190404_0150'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='periodadjustment',
            unique_together={('adjusted_date', 'period')},
        ),
    ]