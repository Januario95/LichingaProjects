from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import (
    Expense, Project, Employee, Quantity,
    Ingredient, RecipePreparation, Recipe
)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'quantity', 'unit', 'price')
    list_display_links = ('id', 'name')
    list_editable = ('quantity', 'unit', 'price')

@admin.register(RecipePreparation)
class RecipePreparationAdmin(admin.ModelAdmin):
    list_display = ('id', 'step', 'description')
    list_display_links = ('id', 'step')

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'ingredients_', 'recipe_cost_', 'estimated_sell_price_',
                    'profit_')
    list_display_links = ('id', 'name')
    # list_editable = ('estimated_sell_price',)

    def profit_(self, obj):
        profit = obj.profit()
        color = 'green'
        if profit < 0:
            color = 'red'
        return mark_safe(f'<b style="color:{color};">{profit} MZN</b>')
    profit_.short_description = 'Profit'

    def ingredients_(self, obj):
        ingredients = obj.ingredients.all()
        ol = '<ol>'
        for ingre in ingredients:
            ol += f'<li>{ingre}</li>'
        ol += '</ol>'
        return mark_safe(ol)
    ingredients_.short_description = 'Ingredients'

    def estimated_sell_price_(self, obj):
        estimated_sell_price = obj.estimated_sell_price
        color = 'green'
        if estimated_sell_price < obj.recipe_cost():
            color = 'red'
        return mark_safe(f'<b style="font-weight:bold;">{estimated_sell_price} MZN</b>')
    estimated_sell_price_.short_description = 'Estimated Sell Price'

    def recipe_cost_(self, obj):
        recipe_cost = obj.recipe_cost()
        color = 'green'
        if recipe_cost > obj.estimated_sell_price:
            color = 'red'
        return mark_safe(f'<b style="font-weight:bold;">{recipe_cost} MZN</b>')
    recipe_cost_.short_description = 'Recipe Cost'

@admin.register(Quantity)
class QuantityAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount', 'unit')

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'amount', 'date')
    list_editable = ('date',)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'buy_price', 'sell_price', 'quantity',
                    'expenses_', 'start_operation', 'end_operation')
    
    def expenses_(self, obj):
        expenses = obj.expenses.all()
        ol = '<ol>'
        for expense in expenses:
            ol += f'<li><a href="/admin/app/expense/{expense.pk}/change/">{expense}</a></li>'
        ol += '<ol>'
        return mark_safe(ol)
    expenses_.short_description = 'Expenses'
    
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'potision', 'salary', 'payment_type')