# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-06-11 14:25
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Invoices',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organisation', models.CharField(blank=True, max_length=100)),
                ('supplier_ref', models.CharField(blank=True, max_length=100)),
                ('our_ref', models.CharField(max_length=100)),
                ('invoice', models.FileField(upload_to='static/invoice/%Y/%m/')),
                ('invoice_date', models.DateField(default=datetime.datetime.now, verbose_name='invoice date')),
                ('invoice_value', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('supplier_name', models.CharField(blank=True, max_length=200)),
                ('vat_number', models.CharField(blank=True, max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='invoices',
            name='supplier_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invoice.Supplier'),
        ),
    ]
