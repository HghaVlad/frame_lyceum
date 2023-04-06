from django import template

register = template.Library()


@register.filter(name="get_left")  # Количество оставшихся мест/штук
def amount_left(quantity: int, used: int):  # quantity - всего, used - купили или записалось
    return quantity - used

