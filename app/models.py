from django.db import models
from django.db.models import Sum


class Ingredient(models.Model):
    UNITS = (
        ('cm', 'Cm'),
        ('lt', 'Lt'),
        ('kg', 'Kg'),
        ('gramas', 'Gramas'),
        ('peças', 'peças')
    )
    name = models.CharField(max_length=200)
    quantity = models.IntegerField()
    unit = models.CharField(
        max_length=8,
        choices=UNITS,
        default='kg'
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f'{self.name}'

class RecipePreparation(models.Model):
    step = models.CharField(max_length=150)
    description = models.TextField()

    def __str__(self):
        return f'{self.step} - {self.description[:30]}'

class Recipe(models.Model):
    name = models.CharField(max_length=200)
    ingredients = models.ManyToManyField(
        to=Ingredient, blank=True

    )
    preparation_steps = models.ManyToManyField(
        to=RecipePreparation, blank=True
    )
    estimated_sell_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=150
    )

    def recipe_cost(self):
        total = 0
        for recipe in self.ingredients.all():
            total += recipe.price
        return total
    
    def profit(self):
        return self.estimated_sell_price - self.recipe_cost()

    def __str__(self):
        return f'{self.name}'

class FishMeponda(models.Model):
    buy_date = models.DateField()
    sell_date = models.DateField()
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    buy_price = models.DecimalField(max_digits=10, decimal_places=2)
    sell_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_buy_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_sell_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    transportation = models.DecimalField(max_digits=10, decimal_places=2)
    bags = models.DecimalField(max_digits=10, decimal_places=2)
    transp_handler = models.DecimalField(max_digits=10, decimal_places=2)
    food_handler = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.buy_date}-{self.sell_date}'

    class Meta:
        verbose_name = 'Fish Meponda'
        verbose_name_plural = 'Fish Meponda'
        

class Expense(models.Model):
    name = models.CharField(max_length=150)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f'{self.name} - {self.amount}'
    

class Employee(models.Model):
    TYPES = (
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('onetime', 'Onetime')
    )
    name = models.CharField(max_length=150)
    potision = models.CharField(max_length=50)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    payment_type = models.CharField(
        max_length=20,
        choices=TYPES,
        default='onetime'
    )

    def __str__(self):
        return f'{self.name} - {self.potision}'

class Quantity(models.Model):
    UNITS = (
        ('cm', 'Cm'),
        ('lt', 'Lt'),
        ('kg', 'Kg'),
        ('peças', 'peças')
    )
    amount = models.IntegerField()
    unit = models.CharField(
        max_length=5,
        choices=UNITS,
        default='kg'
    )

    def __str__(self):
        return f'{self.amount} {self.unit}'
    
    class Meta:
        verbose_name = 'Quantity'
        verbose_name_plural = 'Quantities'

class Project(models.Model):
    title = models.CharField(max_length=150)
    buy_price = models.DecimalField(max_digits=10, decimal_places=2)
    sell_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.ForeignKey(
        to=Quantity,
        on_delete=models.CASCADE,
        blank=True, null=True)
    #budget = models.DecimalField(max_digits=10, decimal_places=2, default=10000.00)
    start_operation = models.DateField()
    end_operation = models.DateField()
    expenses = models.ManyToManyField(
        to=Expense, blank=True
    )
    employees = models.ManyToManyField(to=Employee, blank=True)

    def __str__(self):
        return f'{self.title}'
    
    def calc_return(self):
        return (self.sell_price - self.buy_price) * self.quantity.amount

    def total_buy_price(self):
        return self.buy_price * self.quantity.amount
    
    def total_sell_price(self):
        return self.sell_price * self.quantity.amount

    def total_expenses(self):
        expenses = self.expenses.all()
        expenses = expenses.aggregate(total=Sum('amount'))
        return expenses['total']

    def total_salaries(self):
        employees = self.employees.all()
        employees = employees.aggregate(total=Sum('salary'))
        return employees['total']   

    def profit(self):
        return self.calc_return() - (self.total_salaries() + self.total_expenses())    

    def total_cost(self):
        return self.total_buy_price() + self.total_salaries() + self.total_expenses() 

