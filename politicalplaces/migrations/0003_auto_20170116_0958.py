# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-16 09:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('politicalplaces', '0002_auto_20170114_1147'),
    ]

    operations = [
        migrations.RenameField(
            model_name='politicalplace',
            old_name='airport',
            new_name='types',
        ),
        migrations.RenameField(
            model_name='politicalplace',
            old_name='intersection',
            new_name='ward',
        ),
        migrations.RemoveField(
            model_name='mapitem',
            name='custom_zoom',
        ),
        migrations.RemoveField(
            model_name='mapitem',
            name='use_viewport',
        ),
        migrations.RemoveField(
            model_name='politicalplace',
            name='natural_feature',
        ),
        migrations.RemoveField(
            model_name='politicalplace',
            name='neighborhood',
        ),
        migrations.RemoveField(
            model_name='politicalplace',
            name='neighborhood_item',
        ),
        migrations.RemoveField(
            model_name='politicalplace',
            name='park',
        ),
        migrations.RemoveField(
            model_name='politicalplace',
            name='postal_code',
        ),
        migrations.RemoveField(
            model_name='politicalplace',
            name='postal_code_item',
        ),
        migrations.RemoveField(
            model_name='politicalplace',
            name='premise',
        ),
        migrations.RemoveField(
            model_name='politicalplace',
            name='route',
        ),
        migrations.RemoveField(
            model_name='politicalplace',
            name='street_address',
        ),
        migrations.RemoveField(
            model_name='politicalplace',
            name='street_number',
        ),
        migrations.RemoveField(
            model_name='politicalplace',
            name='subpremise',
        ),
        migrations.AddField(
            model_name='mapitem',
            name='types',
            field=models.CharField(default='political', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='politicalplace',
            name='geo_type',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='politicalplace',
            name='response_json',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='politicalplace',
            name='ward_item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='politicalplace_ward_set', to='politicalplaces.MapItem'),
        ),
        migrations.AlterField(
            model_name='mapitem',
            name='response_json',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='politicalplace',
            name='administrative_area_level_1_item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='politicalplace_aal1_set', to='politicalplaces.MapItem'),
        ),
        migrations.AlterField(
            model_name='politicalplace',
            name='administrative_area_level_2_item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='politicalplace_aal2_set', to='politicalplaces.MapItem'),
        ),
        migrations.AlterField(
            model_name='politicalplace',
            name='administrative_area_level_3_item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='politicalplace_aal3_set', to='politicalplaces.MapItem'),
        ),
        migrations.AlterField(
            model_name='politicalplace',
            name='administrative_area_level_4_item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='politicalplace_aal4_set', to='politicalplaces.MapItem'),
        ),
        migrations.AlterField(
            model_name='politicalplace',
            name='administrative_area_level_5_item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='politicalplace_aal5_set', to='politicalplaces.MapItem'),
        ),
        migrations.AlterField(
            model_name='politicalplace',
            name='continent_item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='politicalplace_continent_set', to='politicalplaces.MapItem'),
        ),
        migrations.AlterField(
            model_name='politicalplace',
            name='country_item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='politicalplace_country_set', to='politicalplaces.MapItem'),
        ),
        migrations.AlterField(
            model_name='politicalplace',
            name='locality_item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='politicalplace_locality_set', to='politicalplaces.MapItem'),
        ),
        migrations.AlterField(
            model_name='politicalplace',
            name='sublocality_item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='politicalplace_sublocality_set', to='politicalplaces.MapItem'),
        ),
    ]
