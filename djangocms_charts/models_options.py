import json

from django.conf import settings
from django.contrib.sites.models import Site
from django.db import models
from django.utils.translation import ugettext_lazy as _

import djangocms_charts.cache as charts_cache


# Dataset Configuration
# Options may be configured directly on the dataset. The dataset options can be changed at 3 different levels and are evaluated with the following priority:
#
# per dataset: dataset.*
# per chart: options.datasets[type].*
# or globally: Chart.defaults.global.datasets[type].*

# --------------------------------------

# Options Models

# --------------------------------------
class OptionsBase(models.Model):
    label = models.CharField(_('Namespace Label'),
                             help_text=_('Include the namespaces for options below root, e.g. hover.mode'),
                             max_length=150)

    type = models.CharField(_('Data Type'),
                             help_text=_('Select the input data type'),
                             max_length=10,
                             default='text')

    value = models.TextField(_('Option Value'),
                             help_text=_('Value of the option JSON allowed'))

    def get_json_value(self, check_val=None, check_type=None):
        val = check_val or self.value
        val_type = check_type or self.type
        if val_type == 'text':
            val = val.strip()
        elif val_type == 'number':
            if '.' in val:
                val = float(val)
            else:
                val = int(val)
        elif val_type == 'boolean':
            if val.isnumeric():
                val = bool(int(val))
            else:
                val = val.lower() == 'true'
        elif val_type == 'json':
            val = json.loads(val.replace("'", '"'))
        elif val_type == 'array':
            sep ="\n" if "\n" in val else \
                "," if "," in val else \
                "\t" if "\t" in val else " "
            val = val.split(sep)
            val = list(filter(None, [v.replace(sep, '').strip() for v in val]))
        elif val_type == 'function':
            clean = ['\n', '\r', '\t', '  ',]
            for c in clean:
                val = val.replace(c, '')
            val = f'FUNC_START:{val}:FUNC_END'

        # Dump all values to json
        val = json.dumps(val)
        return val

    def __str__(self):
        return self.label

    class Meta:
        ordering = ['label',]
        abstract = True


# --------------------------------------

# Options Group

# --------------------------------------
class OptionsGroupBase(models.Model):
    name = models.CharField(_('Options Group Name'),
                             help_text=_('Save and Reuse Options groups'),
                             max_length=100)

    def get_as_list(self):
        return [(opt.label, opt.get_json_value()) for opt in self.options.all()]

    def get_as_dict(self):
        options_dict = {}
        for opt in self.options.all():
            labels = opt.label.split(".")
            inner_opts = options_dict
            # Loop to penultimate level: options.hover.setting = 1 > ['options']['hover']['setting'] = 1
            for lbl in labels[:-1]:
                # Set the default as empty dict if missing
                inner_opts = inner_opts.setdefault(lbl, {})

            inner_opts[labels[-1]] = json.loads(opt.get_json_value())

        return options_dict

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        charts_cache.clear_all()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name', ]
        abstract = True


# Global Options Model
# --------------------------------------
class GlobalOptionsGroupModel(OptionsGroupBase):
    # Enable flag to switch global settings on/off
    enabled = models.BooleanField(_("Enable Global Settings"), blank=True, default=True)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)

    @classmethod
    def get_global_options_list(cls, site_id=None):
        site_id = site_id or settings.SITE_ID

        # Get Cached
        # -------------------
        cached_global_options = charts_cache.get(cls.__name__, site_id)
        if cached_global_options:
            return cached_global_options

        global_options = cls.objects.filter(site_id=site_id, enabled=True)
        if global_options.exists():
            cached_global_options = global_options.first().get_as_list()
            charts_cache.set(cls.__name__, site_id, cached_global_options)
            return cached_global_options


class GlobalOptionsModel(OptionsBase):
    options_group = models.ForeignKey('GlobalOptionsGroupModel', on_delete=models.CASCADE, related_name='options')


# Chart Options Model
# --------------------------------------
class ChartOptionsGroupModel(OptionsGroupBase):
    pass

class ChartOptionsModel(OptionsBase):
    options_group = models.ForeignKey('ChartOptionsGroupModel', on_delete=models.CASCADE, related_name='options')


# Dataset Options Model
# --------------------------------------
class DatasetOptionsGroupModel(OptionsGroupBase):
    pass

class DatasetOptionsModel(OptionsBase):
    options_group = models.ForeignKey('DatasetOptionsGroupModel', on_delete=models.CASCADE, related_name='options')


# Axis Options Model
# --------------------------------------
class AxisOptionsGroupModel(OptionsGroupBase):
    pass

class AxisOptionsModel(OptionsBase):
    options_group = models.ForeignKey('AxisOptionsGroupModel', on_delete=models.CASCADE, related_name='options')