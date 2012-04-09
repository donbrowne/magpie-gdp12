from django import template

register = template.Library()

def lslice(string, amount):
    return string[int(amount):]
    
def contains(string, substring):
    return substring in string
    
def isImg(string):
    types = ['jpg','jpeg','png','svg','gif','bmp']
    stringArray = string.split(".")[-1:]
    extension = stringArray[0].lower()
    return extension in types

def escapeForJS(string):
    chars = [' ','"','\'','(',')','<','>','[',']']
    for c in chars:
        string = string.replace(c,'')
    return string

register.filter('lslice', lslice)
register.filter('contains', contains)
register.filter('isImg', isImg)
register.filter('escapeForJS', escapeForJS)
