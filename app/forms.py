from django import forms


class DateInput(forms.DateInput):
    input_type = 'date'

class ReadExcelForm(forms.Form):
    start_date = forms.DateField(widget=DateInput)
    end_date = forms.DateField(widget=DateInput)



class BeansSellingForm2(forms.Form):
    buy_price = forms.DecimalField(
        min_value=1, max_value=10001,
        max_digits=10, decimal_places=2,
        widget=forms.NumberInput(), initial=700
    )
    sell_price = forms.DecimalField(
        min_value=5, max_value=10001,
        max_digits=10, decimal_places=2,
        widget=forms.NumberInput(), initial=100
    )
    budget = forms.IntegerField(
        min_value=1, max_value=10_000_000,
        widget=forms.NumberInput(), initial=20_000
    )
    transport = forms.DecimalField(
        min_value=0, max_value=100_000,
        max_digits=10, decimal_places=2,
        widget=forms.NumberInput(), initial=5_000
    )
    food = forms.DecimalField(
        min_value=0, max_value=100_000,
        max_digits=10, decimal_places=2,
        widget=forms.NumberInput(), initial=1_500
    )
    accomodation = forms.DecimalField(
        min_value=0, max_value=50_000,
        max_digits=10, decimal_places=2,
        widget=forms.NumberInput(), initial=1000
    )
    authorities = forms.DecimalField(
        min_value=0, max_value=100_000,
        max_digits=10, decimal_places=2,
        widget=forms.NumberInput(), initial=3_000
    )
    reinvest = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput
    )


class BeansSellingForm(forms.Form):
    buy_price = forms.DecimalField(
        min_value=1, max_value=10001,
        max_digits=10, decimal_places=2,
        widget=forms.NumberInput(), initial=500
    )
    sell_price = forms.DecimalField(
        min_value=5, max_value=10001,
        max_digits=10, decimal_places=2,
        widget=forms.NumberInput(), initial=1100
    )
    budget = forms.IntegerField(
        min_value=1, max_value=10_000_000,
        widget=forms.NumberInput(), initial=50_000
    )
    transport = forms.DecimalField(
        min_value=5, max_value=100_000,
        max_digits=10, decimal_places=2,
        widget=forms.NumberInput(), initial=5_000
    )
    food = forms.DecimalField(
        min_value=5, max_value=100_000,
        max_digits=10, decimal_places=2,
        widget=forms.NumberInput(), initial=2_000
    )
    accomodation = forms.DecimalField(
        min_value=-1, max_value=50_000,
        max_digits=10, decimal_places=2,
        widget=forms.NumberInput(), initial=0
    )
    authorities = forms.DecimalField(
        min_value=5, max_value=100_000,
        max_digits=10, decimal_places=2,
        widget=forms.NumberInput(), initial=3_000
    )

class GergelimSellingForm(forms.Form):
    buy_price = forms.DecimalField(
        min_value=1, max_value=10001,
        max_digits=10, decimal_places=2,
        widget=forms.NumberInput(), initial=60
    )
    sell_price = forms.DecimalField(
        min_value=5, max_value=10001,
        max_digits=10, decimal_places=2,
        widget=forms.NumberInput(), initial=120
    )
    budget = forms.IntegerField(
        min_value=1, max_value=10_000_000,
        widget=forms.NumberInput(), initial=750_000
    )
    transport = forms.DecimalField(
        min_value=5, max_value=100_000,
        max_digits=10, decimal_places=2,
        widget=forms.NumberInput(), initial=50_000
    )
    food = forms.DecimalField(
        min_value=5, max_value=100_000,
        max_digits=10, decimal_places=2,
        widget=forms.NumberInput(), initial=15_000
    )
    accomodation = forms.DecimalField(
        min_value=5, max_value=100_000,
        max_digits=10, decimal_places=2,
        widget=forms.NumberInput(), initial=20_000
    )
    authorities = forms.DecimalField(
        min_value=5, max_value=100_000,
        max_digits=10, decimal_places=2,
        widget=forms.NumberInput(), initial=30_000
    )


class FishToTeacherForm(forms.Form):
    buy_price = forms.DecimalField(
        min_value=1, max_value=10001,
        max_digits=10, decimal_places=2,
        widget=forms.NumberInput(), initial=130
    )
    sell_price = forms.DecimalField(
        min_value=5, max_value=10001,
        max_digits=10, decimal_places=2,
        widget=forms.NumberInput(), initial=270
    )
    nr_of_customers = forms.IntegerField(
        min_value=1, max_value=500,
        widget=forms.NumberInput(), initial=100
    )
    kg_per_customer = forms.IntegerField(
        min_value=1, max_value=500,
        widget=forms.NumberInput(), initial=5
    )
    nr_of_months = forms.IntegerField(
        min_value=1, max_value=24,
        widget=forms.NumberInput(), initial=12
    )


class FishLichingaForm(forms.Form):
    baldes = forms.IntegerField(
        min_value=1, max_value=500,
        widget=forms.NumberInput(), initial=30
    )
    buy_price = forms.DecimalField(
        min_value=1, max_value=10001,
        max_digits=10, decimal_places=2,
        widget=forms.NumberInput(), initial=500
    )
    sell_price = forms.DecimalField(
        min_value=5, max_value=10001,
        max_digits=10, decimal_places=2,
        widget=forms.NumberInput(), initial=1000
    )


class FishMepondaForm(forms.Form):
    OPTIONS = (
        ('Option 1', 'Option 1'),
        ('Option 2', 'Option 2'),
        ('Both', 'Both')
    )
    budget = forms.DecimalField(
        min_value=1000, max_value=500000,
        max_digits=10, decimal_places=2,
        widget=forms.NumberInput(), initial=9900
    )
    buy_price = forms.DecimalField(
        min_value=1, max_value=10001,
        max_digits=10, decimal_places=2,
        widget=forms.NumberInput(), initial=400
    )
    sell_price = forms.DecimalField(
        min_value=5, max_value=10001,
        max_digits=10, decimal_places=2,
        widget=forms.NumberInput(), initial=800
    )
    transportation = forms.DecimalField(
        min_value=0, max_value=10001,
        max_digits=10, decimal_places=2,
        widget=forms.NumberInput(), initial=300
    )
    n_times = forms.IntegerField(widget=forms.NumberInput(), initial=8)
    handler = forms.DecimalField(
        min_value=0, max_value=100000,
        max_digits=10, decimal_places=2,
        widget=forms.NumberInput(), initial=200
    )
    option = forms.ChoiceField(
        choices=OPTIONS,
        required=False
    )

  

class FishForm(forms.Form):
    OPTIONS = (
        ('Option 1', 'Option 1'),
        ('Option 2', 'Option 2'),
        ('Both', 'Both')
    )
    budget = forms.DecimalField(
        min_value=1000, max_value=500000,
        max_digits=10, decimal_places=2,
        widget=forms.NumberInput(), initial=9600
    )
    buy_price = forms.DecimalField(
        min_value=1, max_value=10001,
        max_digits=10, decimal_places=2,
        widget=forms.NumberInput(), initial=400
    )
    sell_price = forms.DecimalField(
        min_value=5, max_value=10001,
        max_digits=10, decimal_places=2,
        widget=forms.NumberInput(), initial=800
    )
    transportation = forms.DecimalField(
        min_value=0, max_value=10001,
        max_digits=10, decimal_places=2,
        widget=forms.NumberInput(), initial=1200
    )
    n_times = forms.IntegerField(widget=forms.NumberInput(), initial=4)
    handler = forms.DecimalField(
        min_value=0, max_value=100000,
        max_digits=10, decimal_places=2,
        widget=forms.NumberInput(), initial=2000
    )
    option = forms.ChoiceField(
        choices=OPTIONS,
        required=False
    )

    
