import requests
import re
from tkinter import *
import tkinter as tk
from tkinter import ttk

class RealTimeCurrencyConverter:
    def __init__(self, url):
        try:
            self.data = requests.get(url).json()
            self.currencies = self.data.get('rates', {})
        except Exception as e:
            print("Error fetching currency data:", e)
            self.currencies = {}  # Default to empty dictionary

    def convert(self, from_currency, to_currency, amount):
        if from_currency not in self.currencies or to_currency not in self.currencies:
            return "Invalid Currency"

        if from_currency != 'USD':
            amount = amount / self.currencies[from_currency]
        
        return round(amount * self.currencies[to_currency], 4)

class App(tk.Tk):
    def __init__(self, converter):
        super().__init__()
        self.title("Currency Converter")
        self.geometry("500x250")
        self.currency_converter = converter

        # Labels
        Label(self, text="Welcome to Currency Converter", fg="blue", font=("Courier", 14, "bold")).grid(row=0, column=1, pady=10)
        self.date_label = Label(self, text="", font=("Arial", 10))
        self.date_label.grid(row=1, column=1)

        # Validate function
        self.registered_validation = (self.register(self.restrictNumberOnly), "%d", "%P")

        # Amount field
        Label(self, text="Amount:").grid(row=2, column=0, padx=10, pady=5)
        self.amount_field = Entry(self, validate="key", validatecommand=self.registered_validation)
        self.amount_field.grid(row=2, column=1, padx=10, pady=5)

        # Dropdowns
        Label(self, text="From Currency:").grid(row=3, column=0)
        self.from_currency_variable = StringVar(self)
        self.from_currency_variable.set("INR")
        self.from_currency_dropdown = ttk.Combobox(self, textvariable=self.from_currency_variable, values=list(converter.currencies.keys()), state="readonly", width=12)
        self.from_currency_dropdown.grid(row=3, column=1)

        Label(self, text="To Currency:").grid(row=4, column=0)
        self.to_currency_variable = StringVar(self)
        self.to_currency_variable.set("USD")
        self.to_currency_dropdown = ttk.Combobox(self, textvariable=self.to_currency_variable, values=list(converter.currencies.keys()), state="readonly", width=12)
        self.to_currency_dropdown.grid(row=4, column=1)

        # Convert button
        self.convert_button = Button(self, text="Convert", command=self.perform, font=("Courier", 10, "bold"))
        self.convert_button.grid(row=5, column=1, pady=10)

        # Result label
        self.converted_amount_label = Label(self, text="", font=("Arial", 12, "bold"), fg="green")
        self.converted_amount_label.grid(row=6, column=1)

        # Update exchange rate info
        self.update_rate_label()

    def update_rate_label(self):
        if "INR" in self.currency_converter.currencies and "USD" in self.currency_converter.currencies:
            rate = self.currency_converter.convert("INR", "USD", 1)
            self.date_label.config(text=f"1 INR = {rate} USD | Date: {self.currency_converter.data.get('date', 'N/A')}")

    def perform(self):
        try:
            amount = float(self.amount_field.get())
            from_currency = self.from_currency_variable.get()
            to_currency = self.to_currency_variable.get()
            converted_amount = self.currency_converter.convert(from_currency, to_currency, amount)
            self.converted_amount_label.config(text=f"Converted: {converted_amount}")
        except ValueError:
            self.converted_amount_label.config(text="Invalid Input", fg="red")

    def restrictNumberOnly(self, action, value_if_allowed):
        return bool(re.match(r"^\d*\.?\d*$", value_if_allowed))

if __name__ == "__main__":
    url = "https://api.exchangerate-api.com/v4/latest/USD"
    converter = RealTimeCurrencyConverter(url)
    app = App(converter)
    app.mainloop()

