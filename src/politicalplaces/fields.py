from django.db.models import ForeignKey
from django.forms import ModelChoiceField
from .models import PoliticalPlace
from .widgets import PlaceWidget


class PlaceChoiceField(ModelChoiceField):

    def clean(self, value):
        fk_value = value
        if value not in ("", None):
            fk_value = PoliticalPlace.get_or_create_from_address(value).pk
        return super(PlaceChoiceField, self).clean(fk_value)

    def prepare_value(self, value):
        # TODO is there any way to get address without doing an extra query?
        if value and isinstance(value, int):
            value = PoliticalPlace.objects.get(pk=value).address
        return super(PlaceChoiceField, self).prepare_value(value)


class PlaceField(ForeignKey):

    def __init__(
            self, to='politicalplaces.PoliticalPlace', on_delete=None,
            related_name=None, related_query_name=None,
            limit_choices_to=None, parent_link=False,
            to_field=None, db_constraint=True, **kwargs):
        super(PlaceField, self).__init__(
            to, on_delete, related_name, related_query_name,
            limit_choices_to, parent_link, to_field,
            db_constraint, **kwargs)

    def formfield(self, **kwargs):
        defaults = {
            'widget': PlaceWidget,
            'form_class': PlaceChoiceField}
        defaults.update(kwargs)
        return super(PlaceField, self).formfield(**defaults)
