# Generated by Django 2.2.16 on 2020-10-22 12:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0022_auto_20180620_1551'),
        ('sites', '0002_alter_domain_unique'),
        ('djangocms_charts', '0004_auto_20200521_2007'),
    ]

    operations = [
        migrations.CreateModel(
            name='AxisOptionsGroupModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Save and Reuse Options groups', max_length=100, verbose_name='Options Group Name')),
                ('type', models.CharField(blank=True, choices=[('linear', 'linear'), ('logarithmic', 'logarithmic'), ('category', 'category'), ('time', 'time'), ('radial', 'radial')], max_length=10, null=True, verbose_name='Axis Type')),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
                ('display', models.CharField(blank=True, choices=[('true', 'true'), ('false', 'false'), ('auto', 'auto')], help_text='Controls the axis global visibility (visible when true, hidden when false). When display: auto, the axis is visible only if at least one associated dataset is visible.', max_length=100, null=True, verbose_name='display')),
                ('weight', models.IntegerField(blank=True, help_text='The weight used to sort the axis. Higher weights are further away from the chart area.', null=True, verbose_name='weight')),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AxisOptionsModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(help_text='Include the namespaces for options below root, e.g. hover.mode', max_length=150, verbose_name='Namespace Label')),
                ('type', models.CharField(default='text', help_text='Select the input data type', max_length=10, verbose_name='Data Type')),
                ('value', models.TextField(help_text='Value of the option JSON allowed', verbose_name='Option Value')),
                ('options_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='djangocms_charts.AxisOptionsGroupModel')),
            ],
            options={
                'ordering': ['label'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ChartModel',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='djangocms_charts_chartmodel', serialize=False, to='cms.CMSPlugin')),
                ('label', models.CharField(blank=True, max_length=256, null=True, verbose_name='Name')),
                ('type', models.CharField(choices=[('line', 'line'), ('line_xy', 'line_xy'), ('bar', 'bar'), ('horizontalBar', 'horizontalBar'), ('radar', 'radar'), ('polarArea', 'polarArea'), ('pie', 'pie'), ('doughnut', 'doughnut'), ('bubble', 'bubble'), ('scatter', 'scatter')], max_length=50, verbose_name='Chart Type')),
                ('table_data', models.TextField(blank=True, verbose_name='Chart Table data')),
                ('labels_top', models.BooleanField(default=True, verbose_name='Labels top row')),
                ('labels_left', models.BooleanField(default=True, verbose_name='Labels left column')),
                ('data_series_format', models.CharField(choices=[('rows', 'rows'), ('cols', 'cols')], default='rows', max_length=10, verbose_name='Multiple Datasets in Rows or Columns')),
                ('color_by_dataset', models.BooleanField(blank=True, default=False, help_text='True to color each Dataset, False to color each element in a Series', null=True, verbose_name='Color by Dataset')),
                ('caption', models.TextField(blank=True, null=True, verbose_name='Caption text below chart')),
                ('display_title', models.BooleanField(default=True, verbose_name='Display Title')),
                ('chart_width', models.CharField(blank=True, max_length=50, null=True, verbose_name='Chart Width')),
                ('chart_height', models.CharField(blank=True, max_length=50, null=True, verbose_name='Chart Height')),
                ('chart_container_classes', models.TextField(blank=True, verbose_name='Additional classes for Chart Container')),
                ('chart_classes', models.TextField(blank=True, verbose_name='Additional classes for Chart')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin', models.Model),
        ),
        migrations.CreateModel(
            name='ChartOptionsGroupModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Save and Reuse Options groups', max_length=100, verbose_name='Options Group Name')),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ChartOptionsModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(help_text='Include the namespaces for options below root, e.g. hover.mode', max_length=150, verbose_name='Namespace Label')),
                ('type', models.CharField(default='text', help_text='Select the input data type', max_length=10, verbose_name='Data Type')),
                ('value', models.TextField(help_text='Value of the option JSON allowed', verbose_name='Option Value')),
                ('options_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='djangocms_charts.ChartOptionsGroupModel')),
            ],
            options={
                'ordering': ['label'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ColorGroupModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Color Group Name')),
            ],
            options={
                'verbose_name': 'Color Groups',
                'verbose_name_plural': 'Color Groups',
            },
        ),
        migrations.CreateModel(
            name='ColorModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('types', models.TextField(verbose_name='Select the Chart Types')),
                ('labels', models.TextField(verbose_name='Select the Namespace Labels')),
                ('colors', models.TextField(verbose_name='Select Multiple Colors')),
                ('color_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='colors', to='djangocms_charts.ColorGroupModel')),
            ],
        ),
        migrations.CreateModel(
            name='DatasetModel',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='djangocms_charts_datasetmodel', serialize=False, to='cms.CMSPlugin')),
                ('label', models.CharField(blank=True, max_length=256, null=True, verbose_name='Name')),
                ('type', models.CharField(choices=[('line', 'line'), ('line_xy', 'line_xy'), ('bar', 'bar'), ('horizontalBar', 'horizontalBar'), ('radar', 'radar'), ('polarArea', 'polarArea'), ('pie', 'pie'), ('doughnut', 'doughnut'), ('bubble', 'bubble'), ('scatter', 'scatter')], max_length=50, verbose_name='Chart Type')),
                ('table_data', models.TextField(blank=True, verbose_name='Chart Table data')),
                ('labels_top', models.BooleanField(default=True, verbose_name='Labels top row')),
                ('labels_left', models.BooleanField(default=True, verbose_name='Labels left column')),
                ('data_series_format', models.CharField(choices=[('rows', 'rows'), ('cols', 'cols')], default='rows', max_length=10, verbose_name='Multiple Datasets in Rows or Columns')),
                ('color_by_dataset', models.BooleanField(blank=True, default=False, help_text='True to color each Dataset, False to color each element in a Series', null=True, verbose_name='Color by Dataset')),
                ('colors', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='datasetmodel_colors', to='djangocms_charts.ColorGroupModel')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin', models.Model),
        ),
        migrations.CreateModel(
            name='DatasetOptionsGroupModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Save and Reuse Options groups', max_length=100, verbose_name='Options Group Name')),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DatasetOptionsModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(help_text='Include the namespaces for options below root, e.g. hover.mode', max_length=150, verbose_name='Namespace Label')),
                ('type', models.CharField(default='text', help_text='Select the input data type', max_length=10, verbose_name='Data Type')),
                ('value', models.TextField(help_text='Value of the option JSON allowed', verbose_name='Option Value')),
                ('options_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='djangocms_charts.DatasetOptionsGroupModel')),
            ],
            options={
                'ordering': ['label'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GlobalOptionsGroupModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Save and Reuse Options groups', max_length=100, verbose_name='Options Group Name')),
                ('enabled', models.BooleanField(blank=True, default=True, verbose_name='Enable Global Settings')),
                ('colors', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='global_colors', to='djangocms_charts.ColorGroupModel')),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sites.Site')),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GlobalOptionsModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(help_text='Include the namespaces for options below root, e.g. hover.mode', max_length=150, verbose_name='Namespace Label')),
                ('type', models.CharField(default='text', help_text='Select the input data type', max_length=10, verbose_name='Data Type')),
                ('value', models.TextField(help_text='Value of the option JSON allowed', verbose_name='Option Value')),
                ('options_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='djangocms_charts.GlobalOptionsGroupModel')),
            ],
            options={
                'ordering': ['label'],
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='datasetmodel',
            name='options',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='datasetmodel_options', to='djangocms_charts.DatasetOptionsGroupModel'),
        ),
        migrations.AddField(
            model_name='datasetmodel',
            name='xAxis',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='datasetmodel_xAxis', to='djangocms_charts.AxisOptionsGroupModel'),
        ),
        migrations.AddField(
            model_name='datasetmodel',
            name='yAxis',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='datasetmodel_yAxis', to='djangocms_charts.AxisOptionsGroupModel'),
        ),
        migrations.AddField(
            model_name='chartmodel',
            name='chart_options',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='chart_options', to='djangocms_charts.ChartOptionsGroupModel'),
        ),
        migrations.AddField(
            model_name='chartmodel',
            name='colors',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='chartmodel_colors', to='djangocms_charts.ColorGroupModel'),
        ),
        migrations.AddField(
            model_name='chartmodel',
            name='options',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='chartmodel_options', to='djangocms_charts.DatasetOptionsGroupModel'),
        ),
        migrations.AddField(
            model_name='chartmodel',
            name='xAxis',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='chartmodel_xAxis', to='djangocms_charts.AxisOptionsGroupModel'),
        ),
        migrations.AddField(
            model_name='chartmodel',
            name='yAxis',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='chartmodel_yAxis', to='djangocms_charts.AxisOptionsGroupModel'),
        ),
    ]
