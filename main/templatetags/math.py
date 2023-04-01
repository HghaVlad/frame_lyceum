from django import template

register = template.Library()


@register.filter(name="get_left")  # Количество оставшихся мест/штук
def amount_left(amount: int, used: int):  # Amount - всего, used - купили или записалось
    return amount - used

