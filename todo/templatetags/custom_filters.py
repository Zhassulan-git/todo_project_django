from django import template

register = template.Library()

@register.filter
def pluck_status(tasks):
    #Извлекает все статусы из списка задач
    return [task.status for task in tasks]

@register.filter
def unique(items):
    #Возвращает только уникальные элементы
    return list(set(items))