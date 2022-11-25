import numpy as np
import statistics
import math
import matplotlib.pyplot as plt


def graph_with_trend(input_x, input_y, lbl, curve_1, curve_2, curve_3, params,
                     ln_x, ln_y):  # Функция построения графика с линией тренда
  a1 = params[0][0]
  b1 = params[0][1]
  a2 = params[1][0]
  b2 = params[1][1]
  a3 = params[2][0]
  b3 = params[2][1]
  plt.scatter(input_x, input_y)  # Задание точечной диаграммы
  r1 = statistics.correlation(ln_x, input_y)**2
  r2 = statistics.correlation(input_x, ln_y)**2
  r3 = statistics.correlation(ln_x, ln_y)**2
  sign = '+'
  if b1 < 0:
    sign = '-'
    b1 *= -1
  plt.text(
    80, 0.55,
    f"y = {round(a1,4)}ln(x) {sign}{round(b1,4)}\nR^2 = {round(r1,4)}")
  plt.text(600, 1.25,
           f"y = {round(b2,4)}e^( {round(a2,4)}x)\nR^2 = {round(r2,4)}")
  plt.text(700, 0.25,
           f"y = {round(a3,4)}x^( {round(b3,4)})\nR^2 = {round(r3,4)}")
  # trend_line = np.poly1d(coefficients)  # Функция линии тренда
  # plt.plot(input_x, trend_line(input_x))  # Задание линии тренда
  plt.plot(input_x, curve_1)
  plt.plot(input_x, curve_2)
  plt.plot(input_x, curve_3)
  plt.ylabel('y')  # Название оси y
  plt.xlabel('x')  # Название оси x
  plt.title(lbl)  # Название графика
  plt.show()  # Вывод графика


def function_determination(y, y_calc_column, mean_y):
  y_minus_y_calc__pow2 = np.zeros(length)
  nominator = 0
  for j in range(length):
    y_minus_y_calc__pow2[j] = (y[j] - y_calc_column[j])**2
    nominator += y_minus_y_calc__pow2[j]
  y_minus_y_mean__pow2 = np.zeros(length)
  denominator = 0
  for j in range(length):
    y_minus_y_mean__pow2[j] = (y[j] - mean_y)**2
    denominator += y_minus_y_mean__pow2[j]
  determination = 1 - nominator / denominator
  return determination


def curve_y_1(a, b, x_input):
  curve_1 = []
  for j in x_input:
    curve_1.append(a * math.log(j, math.e) + b)
  return curve_1


def curve_y_2(a, b, x_input):
  curve_2 = []
  for j in x_input:
    curve_2.append(b * math.e**(j * a))
  return curve_2


def curve_y_3(a, b, x_input):
  curve_3 = []
  for j in x_input:
    curve_3.append(a * j**b)
  return curve_3


# 1. Стадия выбора
choice = input(
  "Для работы с конкретными данными введите 1. В ином случае будет работа со случайными данными...\n"
)
if choice == '1':
  y_column = np.fromfile('6_y_data.txt', float,
                         sep=" ")  # Создание строки yT из файла
  x_column = np.fromfile('6_x_data.txt', int,
                         sep=" ")  # Создание строки xT из файла
else:
  y_column = np.random.random(
    50)  # Создание строки yT из 50 случайных чисел в промежутке (0; 1)
  x_column = np.random.randint(
    10, 1000,
    50)  # Создание строки xT из случайных чисел в промежутке (10; 1000)

# 2. Стадия расчётов
length = len(x_column)
x_column = np.sort(x_column)
y_column = np.sort(y_column)
y_mean = statistics.mean(y_column)
lnx_column = np.zeros(length)
lny_column = np.zeros(length)
for i in range(length):
  lnx_column[i] = math.log(float(x_column[i]), math.e)
  lny_column[i] = math.log(float(y_column[i]), math.e)

# Логарифмическая регрессия
a_b_1_coefficients = np.polyfit(lnx_column, y_column, 1)
y_calc_1_column = np.zeros(length)
for i in range(length):
  y_calc_1_column[
    i] = a_b_1_coefficients[0] * lnx_column[i] + a_b_1_coefficients[1]
det1 = function_determination(y_column, y_calc_1_column, y_mean)

# Экспоненциальная регрессия
alfa_beta_2_coefficients = np.polyfit(x_column, lny_column, 1)
a_b_2_coefficients = np.copy(alfa_beta_2_coefficients)
a_b_2_coefficients[1] = math.exp(alfa_beta_2_coefficients[1])
y_calc_2_column = np.zeros(length)
for i in range(length):
  y_calc_2_column[i] = math.exp(a_b_2_coefficients[0] * x_column[i] +
                                a_b_2_coefficients[1])
det2 = function_determination(y_column, y_calc_2_column, y_mean)

# Степенная регрессия
alfa_beta_3_coefficients = np.polyfit(lnx_column, lny_column, 1)
a_b_3_coefficients = np.zeros(2)
a_b_3_coefficients[0] = math.exp(alfa_beta_3_coefficients[1])
a_b_3_coefficients[1] = alfa_beta_3_coefficients[0]
y_calc_3_column = np.zeros(length)
for i in range(length):
  y_calc_3_column[
    i] = a_b_3_coefficients[0] * x_column[i]**a_b_3_coefficients[1]
det3 = function_determination(y_column, y_calc_2_column, y_mean)

# 3. Стадия построения графика
curve_y_1 = curve_y_1(a_b_1_coefficients[0], a_b_1_coefficients[1], x_column)
curve_y_2 = curve_y_2(a_b_2_coefficients[0], a_b_2_coefficients[1], x_column)
curve_y_3 = curve_y_3(a_b_3_coefficients[0], a_b_3_coefficients[1], x_column)
params = [a_b_1_coefficients, a_b_2_coefficients, a_b_3_coefficients]
graph_with_trend(x_column, y_column, "Полиномиальная парная регрессия", curve_y_1, curve_y_2,
                 curve_y_3, params, lnx_column, lny_column)
