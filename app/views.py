from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.viewsets import ModelViewSet

import json
import pandas as pd
import datetime as dt

from .models import (
    Expense, Project, Employee, Quantity
)
from .forms import (
    FishForm, FishMepondaForm, FishLichingaForm,
    FishToTeacherForm, GergelimSellingForm,
    BeansSellingForm, BeansSellingForm2,
    ReadExcelForm,
)
from .serializers import (
    ProjectSerializer
)
from ._helpers import (
    FishSelling, FishSellingMeponda, ReadExcel, Gergelim,
    BeansSelling, BeansSelling2,
)

import json
import pandas as pd
from decimal import Decimal


def venda_de_feijao(request):
    beans = 0
    values = []
    transport = 0
    food = 0
    accomodation = 0
    fixed_expenses = 0
    authorities = 0
    total_profit = 0
    if request.method == 'POST':
        form = BeansSellingForm2(request.POST)
        if form.is_valid():
            inner_data = form.cleaned_data
            # print(inner_data)
            buy_price = inner_data.get('buy_price')
            sell_price = inner_data.get('sell_price')
            budget = inner_data.get('budget')
            transport = inner_data.get('transport')
            food = inner_data.get('food')
            accomodation = inner_data.get('accomodation')
            authorities = inner_data.get('authorities')
            reinvest = inner_data.get('reinvest')
            fixed_expenses = transport + food + accomodation + authorities
            beans = BeansSelling2(buy_price=buy_price, sell_price=sell_price,
                                  budget=budget, transport=transport, food=food,
                                  accomodation=accomodation, authorities=authorities)
            beans.calculate(n_times=10, reinvest=reinvest)
            total_profit = beans.total_profit
            values = beans.values
            # fixed_expenses = beans.additional_expenses
        else:
            print(form.errors)
    else:
        form = BeansSellingForm2()

    return render(request,
                  'app/venda_de_feijao.html',
                  {'form': form, 'values': values, 'transport': transport,
                   'food': food, 'accomodation': accomodation,
                   'authorities': authorities, 'fixed_expenses': fixed_expenses,
                   'total_profit': total_profit})

def beans_selling(request):
    beans = 0
    if request.method == 'POST':
        form = BeansSellingForm(request.POST)
        if form.is_valid():
            inner_data = form.cleaned_data
            # print(inner_data)
            buy_price = inner_data.get('buy_price')
            sell_price = inner_data.get('sell_price')
            budget = inner_data.get('budget')
            transport = inner_data.get('transport')
            food = inner_data.get('food')
            accomodation = inner_data.get('accomodation')
            authorities = inner_data.get('authorities')
            beans = BeansSelling(buy_price, sell_price, budget, transport, food, accomodation, authorities)
            beans = beans.calculate()
            print(json.dumps(beans, indent=4, default=str))
        else:
            print(form.errors)
    else:
        form = BeansSellingForm()

    return render(request,
                  'app/beans_selling.html',
                  {'form': form, 'beans': beans})


def gergelim_selling(request):
    gergelim = {}
    if request.method == 'POST':
        form = GergelimSellingForm(request.POST)
        if form.is_valid():
            inner_data = form.cleaned_data
            # print(inner_data)
            buy_price = inner_data.get('buy_price')
            sell_price = inner_data.get('sell_price')
            budget = inner_data.get('budget')
            transport = inner_data.get('transport')
            food = inner_data.get('food')
            accomodation = inner_data.get('accomodation')
            authorities = inner_data.get('authorities')
            gergelim = Gergelim(buy_price, sell_price, budget, transport, food, accomodation, authorities)
            gergelim = gergelim.calculate()
            # print(json.dumps(gergelim, indent=4, default=str))
        else:
            print(form.errors)
    else:
        form = GergelimSellingForm()

    return render(request,
                  'app/gergelim_selling.html',
                  {'form': form, 'gergelim': gergelim})


def calculate_teacher_profit(buy_price, sell_price, nr_of_customers, kg_per_customer, nr_of_months, format_pandas=False):
    data = []
    for _ in range(nr_of_months):
        total_buy = buy_price * nr_of_customers * kg_per_customer
        total_sell = sell_price * nr_of_customers * kg_per_customer
        profit = total_sell - total_buy
        transportation_police = 2000
        profit -= transportation_police
        row = {
            'buy_price': buy_price,
            'sell_price': sell_price,
            'nr_of_customers': nr_of_customers,
            'kg_per_customer': kg_per_customer,
            'transportation_police': transportation_police,
            'to_assane': round(profit * Decimal(0.3), 2),
            'owner': round(profit * Decimal(0.7), 2),
            'total_buy': total_buy,
            'total_sell': total_sell,
            'profit': profit
        }
        data.append(row)
        nr_of_customers += 10
    if format_pandas:
        return pd.DataFrame(data)
    return data

def fish_to_teachers(request):
    values = []
    totals = {}
    if request.method == 'POST':
        form = FishToTeacherForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            # print(data)
            buy_price = data.get('buy_price')
            sell_price = data.get('sell_price')
            nr_of_customers = data.get('nr_of_customers')
            kg_per_customer = data.get('kg_per_customer')
            nr_of_months = data.get('nr_of_months')
            values = calculate_teacher_profit(buy_price, sell_price, nr_of_customers, kg_per_customer, nr_of_months)
            df = calculate_teacher_profit(buy_price, sell_price, nr_of_customers, kg_per_customer, nr_of_months, format_pandas=True)
            totals = df[['transportation_police', 'to_assane', 'owner', 'total_buy', 'total_sell', 'profit']].sum(axis=0)
            transportation_police, to_assane, owner, total_buy, total_sell, profit = totals.values.tolist()
            totals = {
                'transportation_police': transportation_police,
                'to_assane': to_assane,
                'owner': owner,
                'total_buy': total_buy,
                'total_sell': total_sell,
                'profit': profit
            }
        else:
            print(form.errors)
    else:
        form = FishToTeacherForm()

    return render(request,
                  'app/fish_to_teachers.html',
                  {'form': form, 'values': values, 'totals': totals})


def calculate_profit(baldes, buy_price, sell_price):
    data = []
    for balde in range(1, baldes+1):
        buying_price = balde * buy_price
        selling_price = balde * sell_price
        profit = selling_price - buying_price
        row = {
            'buy_price': buy_price,
            'sell_price': sell_price,
            'baldes': balde,
            'total_buy_price': buying_price,
            'total_sell_price': selling_price,
            'profit': profit
        }
        data.append(row)
    return data

def fish_lichinga(request):
    values = []
    baldes = None
    buy_price = None
    sell_price = None
    total_buy = None
    total_sell = None
    if request.method == 'POST':
        form = FishLichingaForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            # print(data)
            baldes = int(data.get('baldes'))
            buy_price = float(data.get('buy_price'))
            sell_price = float(data.get('sell_price'))
            total_buy = baldes * buy_price
            total_sell = baldes * sell_price
            values = calculate_profit(baldes, buy_price, sell_price)
            # values = [values.pop()]
            values = values[::-1]
            # print(values)
        else:
            print(form.errors)
    else:
        form = FishLichingaForm()

    return render(request,
                  'app/fish_lichinga.html',
                  {'form': form, 'values': values, 'baldes': baldes,
                   'buy_price': buy_price, 'sell_price': sell_price,
                   'total_buy': total_buy, 'total_sell': total_sell})


def get_dataframe_values(df, is_json=False):
    if is_json:
        df = df[['Data', 'Débito']]
        dates = []
        debits = []
        for row in df.values.tolist():
            dates.append(row[0])
            debits.append(row[1])
        return dates, debits
    else:
        data = []
        for row in df.values.tolist():
            data.append({
                'Data': row[0],
                'Data_Valor': row[1],
                'Descricao': row[2],
                'Referencia': row[3],
                'Debito': row[4],
                'Credito': row[5],
                'Saldo': row[6],
                'Moeda': row[7]
            })
        return data

def to_isoformat(date):
    year, month, day = date.split('-')
    return dt.date(int(year), int(month), int(day))

def bank_statement_api(request, start_date, end_date):
    excel_reader = ReadExcel()
    df = excel_reader.df
    start_date = to_isoformat(start_date)
    end_date = to_isoformat(end_date)

    df_ = df[(df['Data'] >= start_date) &
                (df['Data'] <= end_date)]
    dates, debits = get_dataframe_values(df_, is_json=True)
    dates, debits = dates[::-1], debits[::-1]

    return JsonResponse({
        'dates': dates,
        'debits': debits,
    })

def bank_statement(request):
    excel_reader = ReadExcel()
    df = excel_reader.df
    # print(df.dtypes)
    data = get_dataframe_values(df)

    if request.method == 'POST':
        form = ReadExcelForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            # print(form_data)
            start_date = form_data.get('start_date')
            end_date = form_data.get('end_date')
            df_ = df[(df['Data'] >= start_date) &
                     (df['Data'] <= end_date)]
            data = get_dataframe_values(df_, is_json=False)
            # print(len(data))
        else:
            print(form.errors)
    else:
        form = ReadExcelForm()

    return render(request,
                  'app/bank_statement.html',
                  {'data': data, 'form': form})


def fish_selling_meponda(request):
    excel_reader = ReadExcel()
    df = excel_reader.df
    # print(df[:5])
    data1, data2 = [], []
    total_fixed_expenses = 0
    profits2 = 0
    final_profit = 0
    fixed_expenses = []
    show_data1 = False
    show_data2 = False
    cumulative_profits = 0
    profits_minus_fixed_expenses = 0
    profits_minus_fixed_expenses2 = 0
    if request.method == 'POST':
        form = FishMepondaForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            # print(data)
            budget = data.get('budget')
            buy_price = data.get('buy_price')
            sell_price = data.get('sell_price')
            transportation = data.get('transportation')
            n_times = data.get('n_times')
            handler = data.get('handler')
            option = data.get('option')

            fixed_expenses.append({'congelador': 0})
            fixed_expenses.append({'colman': 0})
            fixed_expenses.append({'sacos': 0})
            fixed_expenses.append({'balança': 0})

            for row in fixed_expenses:
                total_fixed_expenses += sum(row.values())
            total_fixed_expenses = round(total_fixed_expenses, 2)

            if option == 'Option 1':
                calc = FishSellingMeponda(budget, buy_price, sell_price) # , transportation, handler)
                data1, final_profit = calc.calculate_return(n_times)
                profits_minus_fixed_expenses = final_profit - total_fixed_expenses
                show_data1 = True
            elif option == 'Option 2':
                calc2 = FishSellingMeponda(budget, buy_price, sell_price) # , transportation, handler)
                data2, profits2, cumulative_profits = calc2.calculate_return2(n_times)
                profits_minus_fixed_expenses2 = profits2 - total_fixed_expenses
                show_data2 = True
            elif option == 'Both':
                calc = FishSellingMeponda(budget, buy_price, sell_price) # , transportation, handler)
                data1, final_profit = calc.calculate_return(n_times)
                calc2 = FishSellingMeponda(budget, buy_price, sell_price) # , transportation, handler)
                data2, profits2 = calc2.calculate_return2(n_times)
                show_data1, show_data2 = True, True

                profits_minus_fixed_expenses = final_profit - total_fixed_expenses
                profits_minus_fixed_expenses2 = profits2 - total_fixed_expenses
        else:
            print(form.errors)
    else:
        form = FishMepondaForm()
        
    return render(request,
                  'app/fish_selling_meponda.html',
                  {'form': form, 'data1': data1, 'data2': data2, 'profits2': profits2,
                   'total_fixed_expenses': total_fixed_expenses,
                   'fixed_expenses': fixed_expenses, 'final_profit': final_profit,
                   'profits_minus_fixed_expenses': profits_minus_fixed_expenses,
                   'profits_minus_fixed_expenses2': profits_minus_fixed_expenses2,
                   'show_data1': show_data1, 'show_data2': show_data2,
                   'cumulative_profits': cumulative_profits})


def fish_selling(request):
    excel_reader = ReadExcel()
    df = excel_reader.df
    # print(df[:5])
    data1, data2 = [], []
    total_fixed_expenses = 0
    profits2 = 0
    final_profit = 0
    fixed_expenses = []
    show_data1 = False
    show_data2 = False
    profits_minus_fixed_expenses = 0
    profits_minus_fixed_expenses2 = 0
    if request.method == 'POST':
        form = FishForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            # print(data)
            budget = data.get('budget')
            buy_price = data.get('buy_price')
            sell_price = data.get('sell_price')
            transportation = data.get('transportation')
            n_times = data.get('n_times')
            handler = data.get('handler')
            option = data.get('option')

            fixed_expenses.append({'congelador': 0})
            fixed_expenses.append({'colman': 0})
            fixed_expenses.append({'sacos': 0})
            fixed_expenses.append({'balança': 0})

            for row in fixed_expenses:
                total_fixed_expenses += sum(row.values())
            total_fixed_expenses = round(total_fixed_expenses, 2)

            if option == 'Option 1':
                calc = FishSelling(budget, buy_price, sell_price, transportation, handler)
                data1, final_profit = calc.calculate_return(n_times)
                profits_minus_fixed_expenses = final_profit - total_fixed_expenses
                show_data1 = True
            elif option == 'Option 2':
                calc2 = FishSelling(budget, buy_price, sell_price, transportation, handler)
                data2, profits2 = calc2.calculate_return2(n_times)
                profits_minus_fixed_expenses2 = profits2 - total_fixed_expenses
                show_data2 = True
            elif option == 'Both':
                calc = FishSelling(budget, buy_price, sell_price, transportation, handler)
                data1, final_profit = calc.calculate_return(n_times)
                calc2 = FishSelling(budget, buy_price, sell_price, transportation, handler)
                data2, profits2 = calc2.calculate_return2(n_times)
                show_data1, show_data2 = True, True

                profits_minus_fixed_expenses = final_profit - total_fixed_expenses
                profits_minus_fixed_expenses2 = profits2 - total_fixed_expenses
        else:
            print(form.errors)
    else:
        form = FishForm()

    return render(request,
                  'app/fish_selling.html',
                  {'form': form, 'data1': data1, 'data2': data2, 'profits2': profits2,
                   'total_fixed_expenses': total_fixed_expenses,
                   'fixed_expenses': fixed_expenses, 'final_profit': final_profit,
                   'profits_minus_fixed_expenses': profits_minus_fixed_expenses,
                   'profits_minus_fixed_expenses2': profits_minus_fixed_expenses2,
                   'show_data1': show_data1, 'show_data2': show_data2})

def project_detail_view(request, project_name):
    try:
        project = Project.objects.get(title=project_name)
    except Project.DoesNotExist:
        project = None

    return render(request,
                  'app/project_detail_view.html',
                  {'project': project})

def projects_view(request):
    projects = Project.objects.all()
    # projects = ['fish_selling', 'fish_to_teachers', 'fish_lichinga',
    #             'gergelim_selling', 'beans_selling']
    return render(request,
                  'app/projects.html',
                  {'projects': projects})

class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

