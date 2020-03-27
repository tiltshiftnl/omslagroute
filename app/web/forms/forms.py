from django import forms
from django.utils.translation import ugettext_lazy as _
from .statics import FIELDS_DICT
from django.forms.utils import ErrorDict, ErrorList
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _
import copy


class GenericForm(forms.Form):
    sections = []

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None, initial=None, error_class=ErrorList,
                 label_suffix=None, empty_permitted=False, field_order=None, use_required_attribute=None,
                 renderer=None, sections=[]):

        self.sections = sections

        super().__init__(data, files, auto_id, prefix, initial, error_class, label_suffix, empty_permitted, field_order,
                         use_required_attribute, renderer)

        for f in self._get_fields(self.sections):
            self.fields[f] = FIELDS_DICT[f]

    def _get_fields(self, sections):
        return [fff for f in sections for ff in f.get('section_list', []) for fff in ff.get('fields', [])]

    def as_sections(self):
        return self._html_section_output(
            normal_row='<div %(html_class_attr)s>%(label)s %(help_text)s %(field)s %(errors)s</div>',
            error_row='%s',
            row_ender='</div>',
            help_text_html=' <p class="help-text">%s</p>',
            errors_on_separate_row=True)

    def _html_section_output(self, normal_row, error_row, row_ender, help_text_html, errors_on_separate_row):
        "Output HTML. Used by as_table(), as_ul(), as_p()."
        top_errors = self.non_field_errors()  # Errors that should be displayed above all fields.
        output, sections_output, hidden_fields = [], {}, []
        sections = copy.deepcopy(self.sections)

        for name, field in self.fields.items():
            html_class_attr = ''
            bf = self[name]
            # Escape and cache in local variable.
            bf_errors = self.error_class([conditional_escape(error) for error in bf.errors])
            if bf.is_hidden:
                if bf_errors:
                    top_errors.extend(
                        [_('(Hidden field %(name)s) %(error)s') % {'name': name, 'error': str(e)}
                         for e in bf_errors])
                hidden_fields.append(str(bf))
            else:
                # Create a 'class="..."' attribute if the row should have any
                # CSS classes applied.
                css_classes = bf.css_classes()
                css_classes += 'form-field form-field--%s' % bf.field.widget.__class__.__name__.lower()
                if css_classes:
                    html_class_attr = ' class="%s"' % css_classes
                if bf.label:
                    label = conditional_escape(bf.label)
                    label = bf.label_tag(label) or ''
                else:
                    label = ''

                if field.help_text:
                    help_text = help_text_html % field.help_text
                else:
                    help_text = ''
                sections_output[name] = mark_safe(normal_row % {
                    'errors': error_row % str(bf_errors),
                    'label': label,
                    'field': bf,
                    'help_text': help_text,
                    'html_class_attr': html_class_attr,
                    'css_classes': css_classes,
                    'field_name': bf.html_name,
                })
        if top_errors:
            output.insert(0, error_row % top_errors)

        if hidden_fields:  # Insert any hidden fields in the last row.
            str_hidden = ''.join(hidden_fields)
            output.append(str_hidden)
        return {
            'errors': mark_safe('\n'.join(output)),
            'hidden_fields': mark_safe(''.join(hidden_fields)),
            'sections': [dict((k, v if not isinstance(v, list) else [dict((kk, vv if not isinstance(vv, list) else [sections_output[sss] for sss in vv]) for kk, vv in ss.items()) for ss in v]) for k, v in s.items()) for s in sections]
        }


class GenericModelForm(forms.ModelForm):
    sections = []

    def __init__(self, sections=[], *args, **kwargs):
        self.sections = sections
        super().__init__(*args, **kwargs)
        for f in self._get_fields(self.sections):
            self.fields[f] = FIELDS_DICT.get(f)

    @staticmethod
    def _get_fields(sections):
        return [fff for f in sections for ff in f.get('section_list', []) for fff in ff.get('fields', [])]

    def as_sections(self):
        return self._html_section_output(
            normal_row='<div %(html_class_attr)s>%(label)s %(help_text)s %(field)s %(errors)s</div>',
            error_row='%s',
            row_ender='</div>',
            help_text_html=' <span class="help-text">%s</span>',
            errors_on_separate_row=True)

    def _html_section_output(self, normal_row, error_row, row_ender, help_text_html, errors_on_separate_row):
        "Output HTML. Used by as_table(), as_ul(), as_p()."
        top_errors = self.non_field_errors()  # Errors that should be displayed above all fields.
        output, sections_output, hidden_fields = [], {}, []
        sections = copy.deepcopy(self.sections)

        for name, field in self.fields.items():
            html_class_attr = ''
            bf = self[name]
            # Escape and cache in local variable.
            bf_errors = self.error_class([conditional_escape(error) for error in bf.errors])
            if bf.is_hidden:
                if bf_errors:
                    top_errors.extend(
                        [_('(Hidden field %(name)s) %(error)s') % {'name': name, 'error': str(e)}
                         for e in bf_errors])
                hidden_fields.append(str(bf))
            else:
                # Create a 'class="..."' attribute if the row should have any
                # CSS classes applied.
                css_classes = bf.css_classes()
                css_classes += ' form-field form-field--%s' % bf.field.widget.__class__.__name__.lower()
                if css_classes:
                    html_class_attr = ' class="%s"' % css_classes
                if bf.label:
                    label = conditional_escape(bf.label)
                    label = bf.label_tag(label) or ''
                else:
                    label = ''

                if field.help_text:
                    help_text = help_text_html % field.help_text
                else:
                    help_text = ''
                sections_output[name] = mark_safe(normal_row % {
                    'errors': error_row % str(bf_errors),
                    'label': label,
                    'field': bf,
                    'help_text': help_text,
                    'html_class_attr': html_class_attr,
                    'css_classes': css_classes,
                    'field_name': bf.html_name,
                })
        if top_errors:
            output.insert(0, error_row % top_errors)

        if hidden_fields:  # Insert any hidden fields in the last row.
            str_hidden = ''.join(hidden_fields)
            output.append(str_hidden)
        return {
            'errors': mark_safe('\n'.join(output)),
            'hidden_fields': mark_safe(''.join(hidden_fields)),
            'sections': [dict((k, v if not isinstance(v, list) else [dict((kk, vv if not isinstance(vv, list) else [sections_output.get(sss, '') for sss in vv]) for kk, vv in ss.items()) for ss in v]) for k, v in s.items()) for s in sections]
        }
