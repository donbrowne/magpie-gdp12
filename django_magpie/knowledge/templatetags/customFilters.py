from django import template

register = template.Library()

def lslice(string, amount):
    return string[int(amount):]
    
def contains(string, substring):
    return substring in string

register.filter('lslice', lslice)
register.filter('contains', contains)
