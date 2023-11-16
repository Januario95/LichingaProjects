import json
import numpy as np
import pandas as pd
from decimal import Decimal

def format_decimal(val):
    return round(val, 2)


class ReadExcel:
    def __init__(self):
        filename = 'Extracto-Movimentos de Conta - 3088566881007.xlsx'
        df = pd.read_excel(filename)
        columns = df.iloc[1:2, :].values[0]
        df.columns = columns
        df = df.iloc[2:-1, :]
        
        df = df.fillna(0)
        df['Data valor'] = df['Data valor'].apply(self.format_float)
        df['Débito'] = df['Débito'].apply(self.format_float)
        df['Crédito'] = df['Crédito'].apply(self.format_float)
        df['Saldo'] = df['Saldo'].apply(self.format_float)
        df[['Débito', 'Crédito', 'Saldo']] = df[['Débito', 'Crédito', 'Saldo']].astype(float)
        df['Data'] = df['Data'].apply(self.to_datetime)
        df['Data'] = df['Data'].apply(self.extract_date)
        self.df = df # .values.tolist()

    def extract_date(self, val):
        return val.date()

    def to_datetime(self, date):
        return pd.to_datetime(date, dayfirst=True)

    def format_float(self, val):
        try:
            return float(val.replace('-', '').replace(',', '.'))
        except Exception as e:
            return val

        


class FishSelling:
    def __init__(self, budget, buy_price_by_kg, sell_price_by_kg, transp, handler):
        self.budget = budget
        self.buy_price_by_kg = buy_price_by_kg
        self.sell_price_by_kg = sell_price_by_kg
        self.transp = transp
        self.handler = handler
        self.quantity = (self.budget - (self.transp + self.handler)) / self.buy_price_by_kg

    def calculate_return2(self, n_times):
        data = []
        profits = 0
        gelo = self.quantity * Decimal(1.5)
        plastics = self.quantity * 5
        CREDELEC = 2000
        for _ in range(n_times):
            return_val = (self.sell_price_by_kg - self.buy_price_by_kg) * self.quantity
            profit = return_val - (self.transp + Decimal(self.handler) + 
                                   Decimal(gelo) + Decimal(plastics) + Decimal(CREDELEC))
            profits += profit
            row = {
                'budget': format_decimal(self.budget),
                'buy_price': format_decimal(self.buy_price_by_kg), 
                'sell_price': format_decimal(self.sell_price_by_kg), 
                'total_buy_price': format_decimal(self.buy_price_by_kg * self.quantity),
                'total_sell_price': format_decimal(self.sell_price_by_kg * self.quantity),
                'quantity': format_decimal(self.quantity),
                'transportation': format_decimal(self.transp),
                'CREDELEC': CREDELEC,
                'plastics': format_decimal(plastics),
                'gelo': format_decimal(gelo),
                'handler': format_decimal(self.handler),
                'return': format_decimal(return_val),
                'profit': format_decimal(profit)
            }
            data.append(row)
        # df = pd.DataFrame(data)
        # print(df)
        # print(df[['budget', 'return', 'profit']].sum(axis=0).T)
        return data, format_decimal(profits)
        
    def calculate_return(self, n_times):
        gelo = self.quantity * Decimal(1.5)
        plastics = self.quantity * 5
        CREDELEC = 2000
        return_val = (self.sell_price_by_kg - self.buy_price_by_kg) * self.quantity
        profit = return_val - (self.transp + Decimal(self.handler) + 
                               Decimal(gelo) + Decimal(plastics) + Decimal(CREDELEC))
        row = {
            'budget': format_decimal(self.budget),
            'buy_price': format_decimal(self.buy_price_by_kg), 
            'sell_price': format_decimal(self.sell_price_by_kg),
            'total_buy_price': format_decimal(self.buy_price_by_kg * self.quantity),
            'total_sell_price': format_decimal(self.sell_price_by_kg * self.quantity),
            'quantity': format_decimal(self.quantity),
            'transportation': format_decimal(self.transp),
            'CREDELEC': CREDELEC,
            'plastics': format_decimal(plastics),
            'gelo': format_decimal(gelo),
            'handler': format_decimal(self.handler),
            'return': format_decimal(return_val),
            'profit': format_decimal(profit)
        }
        data = [row]
        final_profit = 0
        for _ in range(n_times-1):
            self.budget += profit
            self.quantity = (self.budget - (self.transp + self.handler)) / self.buy_price_by_kg
            plastics = self.quantity * 5
            gelo = self.quantity * Decimal(1.5)
            self.transp *= Decimal(1.5)
            self.handler *= Decimal(1.05)
            return_val = (self.sell_price_by_kg - self.buy_price_by_kg) * self.quantity
            profit = return_val - (self.transp + Decimal(self.handler) + 
                                   Decimal(gelo) + Decimal(plastics) + Decimal(CREDELEC))
            final_profit = profit
            row = {
                'budget': format_decimal(self.budget),
                'buy_price': format_decimal(self.buy_price_by_kg), 
                'sell_price': format_decimal(self.sell_price_by_kg),
                'total_buy_price': format_decimal(self.buy_price_by_kg * self.quantity),
                'total_sell_price': format_decimal(self.sell_price_by_kg * self.quantity),
                'quantity': format_decimal(self.quantity),
                'transportation': format_decimal(self.transp),
                'CREDELEC': CREDELEC,
                'plastics': format_decimal(plastics),
                'gelo': format_decimal(gelo),
                'handler': format_decimal(self.handler),
                'return': format_decimal(return_val),
                'profit': format_decimal(profit)
            }
            data.append(row)
        # df = pd.DataFrame(data)
        final_profit = format_decimal(final_profit)
        return data, final_profit
    

class FishSellingMeponda:
    def __init__(self, budget, buy_price_per_bucket, sell_price_per_bucket):
        self.budget = budget
        self.buy_price_per_bucket = buy_price_per_bucket
        self.sell_price_per_bucket = sell_price_per_bucket
        self.transp_handler = 250
        self.handler_food = 500
        self.price_per_bag = 50
        self.transp_fish_per_bag = 150
        self.fish_buying_budget = self.budget - self.additional_costs(2)
        self.quantity = self.fish_buying_budget / self.buy_price_per_bucket
        self.total_sell_price = 0
        self.total_buy_price = 0
        self.cumulative_profits = 0

    def additional_costs(self, qty):
        return (self.transp_handler + 
                self.transp_fish_per_bag * qty + 
                self.handler_food +
                self.price_per_bag * qty)

    def calculate_return2(self, n_times):
        data = []
        profits = 0
        bags = self.quantity * 5
        qty = 2
        for _ in range(n_times):
            return_val = (self.sell_price_per_bucket - self.buy_price_per_bucket) * self.quantity
            profit = return_val - self.additional_costs(qty)
            self.cumulative_profits += profit
            # profits += profit
            row = {
                'budget': format_decimal(self.budget),
                'buy_price': format_decimal(self.buy_price_per_bucket), 
                'sell_price': format_decimal(self.sell_price_per_bucket), 
                'total_buy_price': format_decimal(self.buy_price_per_bucket * self.quantity),
                'total_sell_price': format_decimal(self.sell_price_per_bucket * self.quantity),
                'quantity': format_decimal(self.quantity),
                'transportation': format_decimal(self.transp_fish_per_bag * qty),
                'bags': format_decimal(bags),
                'transp_handler': format_decimal(self.transp_handler),
                'food_handler': self.handler_food,
                'return': format_decimal(return_val),
                'profit': format_decimal(profit),
                'percent_change': round(((profit * 100) / self.budget), 2)
            }
            data.append(row)
            # qty += 2
        # df = pd.DataFrame(data)
        # print(df)
        # print(df[['budget', 'return', 'profit']].sum(axis=0).T)
        return data, format_decimal(profits), self.cumulative_profits
        
    def calculate_return(self, n_times):
        qty = 2
        bags = self.price_per_bag * qty
        self.total_sell_price = format_decimal(self.sell_price_per_bucket * self.quantity)
        self.total_buy_price = format_decimal(self.buy_price_per_bucket * self.quantity)
        return_val = (self.sell_price_per_bucket - self.buy_price_per_bucket) * self.quantity
        profit = return_val - self.additional_costs(qty)
        self.fish_buying_budget = self.total_sell_price - profit
        row_id = 1
        row = {
            'id': row_id,
            'budget': format_decimal(self.budget),
            'buy_price': format_decimal(self.buy_price_per_bucket), 
            'sell_price': format_decimal(self.sell_price_per_bucket),
            'total_buy_price': self.total_buy_price,
            'total_sell_price': self.total_sell_price,
            'quantity': format_decimal(self.quantity),
            'transportation': format_decimal(self.transp_fish_per_bag * qty),
            'bags': format_decimal(bags),
            'transp_handler': format_decimal(self.transp_handler),
            'food_handler': self.handler_food,
            'return': format_decimal(return_val),
            'profit': format_decimal(profit),
            'percent_change': round(((profit * 100) / self.budget), 2)
        }
        data = [row]
        final_profit = 0
        for _ in range(n_times-1):
            qty += 2
            self.fish_buying_budget += (profit - self.additional_costs(qty))
            self.quantity = self.fish_buying_budget / self.buy_price_per_bucket
            self.total_buy_price = format_decimal(self.buy_price_per_bucket * self.quantity)
            self.total_sell_price = format_decimal(self.sell_price_per_bucket * self.quantity)
            bags = self.price_per_bag * qty
            # self.transp *= Decimal(1.5)
            # self.handler = 0 # *= Decimal(1.05)
            return_val = (self.sell_price_per_bucket - self.buy_price_per_bucket) * self.quantity
            profit = return_val - self.additional_costs(qty)
            final_profit = profit
            self.budget = self.fish_buying_budget + self.additional_costs(qty)
            row_id += 1
            row = {
                'id': row_id,
                'budget': format_decimal(self.budget),
                'buy_price': format_decimal(self.buy_price_per_bucket), 
                'sell_price': format_decimal(self.sell_price_per_bucket),
                'total_buy_price': self.total_buy_price,
                'total_sell_price': self.total_sell_price,
                'quantity': format_decimal(self.quantity),
                'transportation': format_decimal(self.transp_fish_per_bag * qty),
                'bags': format_decimal(bags),
                'transp_handler': format_decimal(self.transp_handler),
                'food_handler': self.handler_food,
                'return': format_decimal(return_val),
                'profit': format_decimal(profit),
                'percent_change': round(((profit * 100) / self.budget), 2)
            }
            data.append(row)
        # df = pd.DataFrame(data)
        final_profit = format_decimal(final_profit)
        return data, final_profit
    



class Gergelim:
    def __init__(self, buy_price, sell_price, budget, transport, food, accomodation, authorities):
        self.buy_price = buy_price
        self.sell_price = sell_price
        self.budget = budget
        self.transport = transport
        self.food = food
        self.accomodation = accomodation
        self.authorities = authorities

    def calculate(self):
        buying_budget = self.budget - (self.transport + self.food + self.accomodation + self.authorities)
        quantity = buying_budget / self.buy_price
        total_buy_price = quantity * self.buy_price
        total_sell_price = quantity * self.sell_price
        profit = total_sell_price - total_buy_price
        ROI = profit - (self.transport + self.food + self.accomodation + self.authorities)
        return {
            'buy_price': self.buy_price,
            'sell_price': self.sell_price,
            'budget': self.budget,
            'transport': self.transport,
            'food': self.food,
            'accomodation': self.accomodation,
            'authorities': self.authorities,
            'buying_budget': round(buying_budget, 2),
            'quantity': round(quantity, 2),
            'total_buy_price': round(total_buy_price, 2),
            'total_sell_price': round(total_sell_price, 2),
            'profit': round(profit, 2),
            'ROI': round(ROI, 2),
            'percent_profit': round((round(ROI, 2) * 100) / self.budget, 2)
        }
    

class BeansSelling:
    def __init__(self, buy_price, sell_price, budget, transport, food, accomodation, authorities):
        self.buy_price = buy_price
        self.sell_price = sell_price
        self.budget = budget
        self.transport = transport
        self.food = food
        self.accomodation = accomodation
        self.authorities = authorities

    def calculate(self):
        buying_budget = self.budget - (self.transport + self.food + self.accomodation + self.authorities)
        quantity = buying_budget / self.buy_price
        total_buy_price = quantity * self.buy_price
        total_sell_price = quantity * self.sell_price
        profit = total_sell_price - total_buy_price
        ROI = profit - (self.transport + self.food + self.accomodation + self.authorities)
        return {
            'buy_price': self.buy_price,
            'sell_price': self.sell_price,
            'budget': self.budget,
            'transport': self.transport,
            'food': self.food,
            'accomodation': self.accomodation,
            'authorities': self.authorities,
            'buying_budget': round(buying_budget, 2),
            'quantity': round(quantity, 2),
            'total_buy_price': round(total_buy_price, 2),
            'total_sell_price': round(total_sell_price, 2),
            'profit': round(profit, 2),
            'ROI': round(ROI, 2),
            'percent_profit': round((round(ROI, 2) * 100) / self.budget, 2)
        }
    

class BeansSelling2:
    def __init__(self, buy_price, sell_price, budget, transport,
                 food, accomodation, authorities):
        self.buy_price = buy_price
        self.sell_price = sell_price
        self.budget = budget
        self.transport = transport
        self.food = food
        self.accomodation = accomodation
        self.authorities = authorities
        self.additional_expenses = self.transport + self.food + self.accomodation + self.authorities
        self.total_buy_price = 0
        self.quantity = 0
        self.total_sell_price = 0
        self.profit = 0
        self.total_profit = 0
        self.values = []

    def update(self, reinvest):
        self.total_buy_price = self.budget - self.additional_expenses
        self.quantity = (self.total_buy_price / self.buy_price) * 25
        self.total_sell_price = self.quantity * self.sell_price
        self.profit = self.total_sell_price - self.total_buy_price
        self.total_profit += round(self.profit, 2)
        data = {
            'buy_price': self.buy_price,
            'sell_price': self.sell_price,
            'budget': round(self.budget, 2),
            'transport': self.transport,
            'food': self.food,
            'accomodation': self.accomodation,
            'authorities': self.authorities,
            'additional_expenses': round(self.additional_expenses, 2),
            'total_buy_price': round(self.total_buy_price, 2),
            'quantity': round(self.quantity, 2),
            'quantity_sacos': round(round(self.quantity, 2) / 50, 2),
            'total_sell_price': round(self.total_sell_price, 2),
            'profit': round(self.profit, 2),
        }
        self.values.append(data)
        if reinvest:
            self.additional_expenses *= Decimal(1.25)
        # print(self.additional_expenses)
        # print(json.dumps(data, indent=4, default=str))

    def calculate(self, n_times=1, reinvest=False):
        for _ in range(n_times):
            self.update(reinvest)
            if reinvest:
                self.budget += self.profit


