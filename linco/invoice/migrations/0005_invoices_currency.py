# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-07-02 09:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0004_invoices_refund'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoices',
            name='currency',
            field=models.CharField(blank=True, max_length=600),
        ),
    ]
