from django import template

register = template.Library()

@register.filter
def rd(value):
    try:
        v = float(value)
    except (TypeError, ValueError):
        return value
    return f"RD$ {v:,.2f}"
