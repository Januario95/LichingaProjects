from django import template

register = template.Library()

@register.filter
def get_total_dict(dicti):
	total = 0
	for row in dicti:
		total += sum(row.values())
	return total

@register.filter
def get_key(value):
	return list(value.keys())[0].title()

@register.filter
def get_value(value):
	return list(value.values())[0]

@register.filter
def format_payment_type(value):
	if value == 'onetime':
		return 'Uma vez'
	elif value == 'weekly':
		return 'Semanal'
	elif value == 'monthly':
		return 'Mensal'

@register.filter
def format_gender(value):
	if value == 'female':
		return 'Feminino'
	elif value == 'male':
		return 'Masculino'


@register.filter
def get_first_letter(value):
	return value[0].upper()

@register.filter
def capitalize(value):
	return value.title()

@register.filter
def format_test(value):
	value = value.split('st')
	value = value[0].title() + 'st' + value[-1]
	return value






