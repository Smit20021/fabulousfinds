from django import template
register = template.Library()


@register.filter(name='currency')
def currency(number):
    return "₹ " + str(number)

@register.filter(name='TotalCost')
def TotalCost(qty, price):
    return  qty*price


@register.filter(name='TotalPrice')
def TotalPrice(totalprice,count):
    itemsum=0
    for itemsum in range(count):
        itemsum = int(itemsum) + int(totalprice)
    return itemsum