from django import template

register = template.Library()

#Unit tested
def lslice(string, amount):
    return string[int(amount):]
    
#Unit tested
def contains(string, substring):
    return substring in string
    
#Unit tested
def isImg(string):
    types = ['jpg','jpeg','png','svg','gif','bmp']
    stringArray = string.split(".")[-1:]
    extension = stringArray[0].lower()
    return extension in types

#Unit tested
def escapeForJS(string):
    chars = [' ','"','\'','(',')','<','>','[',']','\\']
    for c in chars:
        string = string.replace(c,'')
    return string

register.filter('lslice', lslice)
register.filter('contains', contains)
register.filter('isImg', isImg)
register.filter('escapeForJS', escapeForJS)
