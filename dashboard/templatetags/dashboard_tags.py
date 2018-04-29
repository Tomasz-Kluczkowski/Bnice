from django import template

register = template.Library()


@register.simple_tag
def set_var(variable):
    return variable


@register.filter
def get_model_name(value):
    return value.__class__.__name__
