from tkinter import *
from tkinter import messagebox
from math import ceil
from math_functions import Vector, Point
import sys

w_parametrs = Tk()
w_parametrs.title('Enter parametrs')
w_parametrs.resizable(width=False, height=False)


class Fields:

    ALLOWED_HEIGHT_VAR = StringVar()
    ALLOWED_HEIGHT_LABEL = Label(w_parametrs, text='доп. висота польоту (м):', font='19')
    ALLOWED_HEIGHT_ENTRY = Entry(w_parametrs, width=25, textvar=ALLOWED_HEIGHT_VAR, font=("Times New Roman", 15))

    FOCUS_DISTANCE_VAR = StringVar()
    FOCUS_DISTANCE_LABEL = Label(w_parametrs, text='фок. відстань (мм):', font='19')
    FOCUS_DISTANCE_ENTRY = Entry(w_parametrs, width=25, textvar=FOCUS_DISTANCE_VAR, font=("Times New Roman", 15))

    MATRIX_WIDTH_VAR = StringVar()
    MATRIX_WIDTH_LABEL = Label(w_parametrs, text='ширина фотосенсору (мм):', font='19')
    MATRIX_WIDTH_ENTRY = Entry(w_parametrs, width=25, textvar=MATRIX_WIDTH_VAR, font=("Times New Roman", 15))

    MATRIX_LENGTH_VAR = StringVar()
    MATRIX_LENGTH_LABEL = Label(w_parametrs, text='довжина фотосенсору (мм):', font='19')
    MATRIX_LENGTH_ENTRY = Entry(w_parametrs, width=25, textvar=MATRIX_LENGTH_VAR, font=("Times New Roman", 15))

    BATTERY_FLIGHT_SPENDING_VAR = StringVar()
    BATTERY_FLIGHT_SPENDING_LABEL = Label(w_parametrs, text='витрати заряду на політ (%/м):', font='19')
    BATTERY_FLIGHT_SPENDING_ENTRY = Entry(w_parametrs, width=25, textvar=BATTERY_FLIGHT_SPENDING_VAR, font=("Times New Roman", 15))

    BATTERY_PHOTO_SPENDING_VAR = StringVar()
    BATTERY_PHOTO_SPENDING_LABEL = Label(w_parametrs, text='витрати заряду на фото (%):', font='19')
    BATTERY_PHOTO_SPENDING_ENTRY = Entry(w_parametrs, width=25, textvar=BATTERY_PHOTO_SPENDING_VAR, font=("Times New Roman", 15))

    TERRITORY_LENGTH_VAR = StringVar()
    TERRITORY_LENGTH_LABEL = Label(w_parametrs, text='довжина території (м):', font='19')
    TERRITORY_LENGTH_ENTRY = Entry(w_parametrs, width=25, textvar=TERRITORY_LENGTH_VAR, font=("Times New Roman", 15))

    TERRITORY_WIDTH_VAR = StringVar()
    TERRITORY_WIDTH_LABEL = Label(w_parametrs, text='ширина території (м):', font='19')
    TERRITORY_WIDTH_ENTRY = Entry(w_parametrs, width=25, textvar=TERRITORY_WIDTH_VAR, font=("Times New Roman", 15))

    BATTERY_VAR = StringVar()
    BATTERY_LABEL = Label(w_parametrs, text='заряд батареї (%):', font='19')
    BATTERY_ENTRY = Entry(w_parametrs, width=25, textvar=BATTERY_VAR, font=("Times New Roman", 15))

    CALCULATE_BUTTON = Button(w_parametrs, text='Продовжити', font=19) # background='#008000'


    def __init__(self):

        self.CALCULATE_BUTTON.bind('<Button-1>', self.calculate)

        self.ALLOWED_HEIGHT_LABEL.grid(row=1, column=1, padx=10, pady=10, sticky='E')
        self.ALLOWED_HEIGHT_ENTRY.grid(row=1, column=2, padx=10, pady=10)

        self.FOCUS_DISTANCE_LABEL.grid(row=1, column=3, padx=10, pady=10, sticky='E')
        self.FOCUS_DISTANCE_ENTRY.grid(row=1, column=4, padx=10, pady=10)

        self.MATRIX_WIDTH_LABEL.grid(row=2, column=1, padx=10, pady=10, sticky='E')
        self.MATRIX_WIDTH_ENTRY.grid(row=2, column=2, padx=10, pady=10)

        self.MATRIX_LENGTH_LABEL.grid(row=2, column=3, padx=10, pady=10, sticky='E')
        self.MATRIX_LENGTH_ENTRY.grid(row=2, column=4, padx=10, pady=10)

        self.BATTERY_FLIGHT_SPENDING_LABEL.grid(row=3, column=1, padx=10, pady=10, sticky='E')
        self.BATTERY_FLIGHT_SPENDING_ENTRY.grid(row=3, column=2, padx=10, pady=10)

        self.BATTERY_PHOTO_SPENDING_LABEL.grid(row=3, column=3, padx=10, pady=10, sticky='E')
        self.BATTERY_PHOTO_SPENDING_ENTRY.grid(row=3, column=4, padx=10, pady=10)

        self.TERRITORY_LENGTH_LABEL.grid(row=4, column=1, padx=10, pady=10, sticky='E')
        self.TERRITORY_LENGTH_ENTRY.grid(row=4, column=2, padx=10, pady=10)

        self.TERRITORY_WIDTH_LABEL.grid(row=4, column=3, padx=10, pady=10, sticky='E')
        self.TERRITORY_WIDTH_ENTRY.grid(row=4, column=4, padx=10, pady=10)

        self.BATTERY_LABEL.grid(row=5, column=1, padx=10, pady=10, sticky='E')
        self.BATTERY_ENTRY.grid(row=5, column=2, padx=10, pady=10)

        self.CALCULATE_BUTTON.grid(row=5, columnspan=2, column=3, padx=10, pady=10)


    def validate_allowed_height(self):
        if self.ALLOWED_HEIGHT_VAR.get() == '':
            return False
        try:
            self.allowed_height = float(self.ALLOWED_HEIGHT_VAR.get().replace(',', '.'))
            if 4 < self.allowed_height < 501:
                return True
            messagebox.showinfo("Помилка", "Допустима висота для зйомки має бути в межах від 5 до 500 метрів")
        except ValueError:
            messagebox.showinfo("Помилка", "Допустима висота має бути числом")


    def validate_focus_distance(self):
        if self.FOCUS_DISTANCE_VAR.get() == '':
            return False
        try:
            self.focus_distance = float(self.FOCUS_DISTANCE_VAR.get().replace(',', '.'))
            if 1 < self.focus_distance < 9:
                return True
            messagebox.showinfo("Помилка", "Фокусна відстань для зйомки має бути в межах від 2 до 8 міліметрів")
        except ValueError:
            messagebox.showinfo("Помилка", "Фокусна відстань має бути числом")


    def validate_matrix_width(self):
        if self.MATRIX_WIDTH_VAR.get() == '':
            return False
        try:
            self.matrix_width = float(self.MATRIX_WIDTH_VAR.get().replace(',', '.'))
            if 1 < self.matrix_width < 36:
                return True
            messagebox.showinfo("Помилка", "Ширина матриці має бути в межах від 2 до 35 міліметрів")
        except ValueError:
            messagebox.showinfo("Помилка", "Ширина фотосенсору має бути числом")


    def validate_matrix_length(self):
        if self.MATRIX_LENGTH_VAR.get() == '':
            return False
        try:
            self.matrix_length = float(self.MATRIX_LENGTH_VAR.get().replace(',', '.'))
            if 1 < self.matrix_length < 36:
                return True
            messagebox.showinfo("Помилка", "Довжина матриці має бути в межах від 2 до 35 міліметрів")
        except ValueError:
            messagebox.showinfo("Помилка", "Довжина фотосенсору має бути числом")


    def validate_battery_flight_spending(self):
        if self.BATTERY_FLIGHT_SPENDING_VAR.get() == '':
            return False
        try:
            self.battery_flight_spending = float(self.BATTERY_FLIGHT_SPENDING_VAR.get().replace(',', '.'))
            if 0 < self.battery_flight_spending < 101:
                return True
            messagebox.showinfo("Помилка", "Витрати заряду на фото мають бути в межах від 1 до 100 %")
        except ValueError:
            messagebox.showinfo("Помилка", "Витрати заряду на політ має бути числом")


    def validate_battery_photo_spending(self):
        if self.BATTERY_PHOTO_SPENDING_VAR.get() == '':
            return False
        try:
            self.battery_photo_spending = float(self.BATTERY_PHOTO_SPENDING_VAR.get().replace(',', '.'))
            if 0 < self.battery_photo_spending < 101:
                return True
            messagebox.showinfo("Помилка", "Витрати заряду на політ мають бути в межах від 1 до 100 %")
        except ValueError:
            messagebox.showinfo("Помилка", "Витрати заряду на фото має бути числом")


    def validate_territory_length(self):
        if self.TERRITORY_LENGTH_VAR.get() == '':
            return False
        try:
            self.territory_length = float(self.TERRITORY_LENGTH_VAR.get().replace(',', '.'))
            if 99 < self.territory_length < 600:
                return True
            messagebox.showinfo("Помилка", "Довжина території має бути в межах від 100 до 600 метрів")
        except ValueError:
            messagebox.showinfo("Помилка", "Довжина території має бути числом")


    def validate_territory_width(self):
        if self.TERRITORY_WIDTH_VAR.get() == '':
            return False
        try:
            self.territory_width = float(self.TERRITORY_WIDTH_VAR.get().replace(',', '.'))
            if 99 < self.territory_width < 600:
                return True
            messagebox.showinfo("Помилка", "Ширина території має бути в межах від 100 до 600 метрів")
        except ValueError:
            messagebox.showinfo("Помилка", "Ширина території має бути числом")


    def validate_battery(self):
        if self.BATTERY_VAR.get() == '':
            return False
        try:
            self.battery = float(self.BATTERY_VAR.get().replace(',', '.'))
            if 0 < self.battery < 101:
                return True
            messagebox.showinfo("Помилка", "Заряд аккумулятора має бути в межах від 1 до 100 %")
        except ValueError:
            messagebox.showinfo("Помилка", "Значення заряду має бути числом")


    def calculate(self, instance):
        if self.validate_allowed_height() and self.validate_focus_distance() and self.validate_matrix_width() and self.validate_matrix_length() \
        and self.validate_battery_flight_spending() and self.validate_battery_photo_spending() and self.validate_territory_length() and self.validate_territory_width() and self.validate_battery():
            base = Point(50, 50, (0, 0, 0))

            l1 = min(self.territory_length, self.territory_width)
            l2 = max(self.territory_length, self.territory_width)


            h = self.allowed_height
            F = self.focus_distance
            A1 = min(self.matrix_width, self.matrix_length) # геометрия
            A2 = max(self.matrix_width, self.matrix_length) # матрицы

            b = self.battery 
            bph = self.battery_photo_spending # затраты на фото
            bfl = self.battery_flight_spending # затраты на полет

            L1 = int((A1*h)/F)
            L2 = int((A2*h)/F)

            PH_P = ceil(l2/L1) # фото на проход
            KP = ceil(l1/L2) # кол-во проходов
            K_PH = PH_P * KP # кол-во фото

            bph_all = K_PH*(bph+bfl) # затраты на фото

            x1 = L2/2 + 50
            y1 = L1/2 + 50
            x2 = x1 + L2*(KP-1)
            y2 = y1
            x3 = x2
            y3 = y1 + L1 * PH_P - L1


            s = Vector(x1-base.x, y1-base.y)
            e = Vector(base.x-x2, base.y-y2) if KP % 2 == 0 else Vector(base.x-x3, base.y-y3)

            l_all = 2*h + abs(s) + L1 * PH_P * KP + L2 * (KP - 1) + abs(e)
            bfl_all = l_all * bfl

            b_all = bph_all + bfl_all

            if b_all < b:
                w_parametrs.destroy()
            else:
                messagebox.showinfo("Неможливо", "Неможливий обліт з такими даними")
                




fields = Fields()
w_parametrs.protocol("WM_DELETE_WINDOW", sys.exit)
