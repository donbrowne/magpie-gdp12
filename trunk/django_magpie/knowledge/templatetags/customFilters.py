from django import template

register = template.Library()

def lslice(string, amount):
    return string[int(amount):]
    
def contains(string, substring):
    return substring in string
    
def isImg(string):
    types = ['jpg','jpeg','png','svg','gif']
    stringArray = string.split(".")[-1:]
    return stringArray[0] in types

register.filter('lslice', lslice)
register.filter('contains', contains)
register.filter('isImg', isImg)
