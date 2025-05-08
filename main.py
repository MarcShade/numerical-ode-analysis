import time 
import csv
import os
import math

_cleared_files = set()

# User-defined variables - Make sure a > 0 and h > 0
a = 0.5
b = 1
h = 0.1
initial_conditions = (0,0)

# Keep duration 500 or below if you want manageable data
duration = 250

def current_time_millis():
    return round(time.time() * 1000)

# Reports division by zero and returns 'NaN'
def safe_divide(numerator, denominator):
    try:
        return numerator / denominator
    except ZeroDivisionError:
        print("[Warning] ZeroDivisionError returning: \"NaN\"")
        return(float('nan'))

# Here the differential equation and explicit solution are set
# The differential equation can be swapped out, but the explicit solution as well as 
# parameters, variables and arguments throughout the program will have to be changed 
def differential_equation(a,b,y):
    return a * y + b

def solution(a, b, t):
    return safe_divide(b, a) * math.exp(a * t) - safe_divide(b, a)

# This function writes data to a fresh CSV-file
def write_to_csv(filename, a, b):
    global _cleared_files

    if filename not in _cleared_files:
        try:
            os.remove(filename)
        except FileNotFoundError:
            pass
        _cleared_files.add(filename)

    with open(filename, 'a', newline='') as csvfile:
        writer_obj = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer_obj.writerow([a, b])

# Eulers method for numerical approximation of solution to differential equations
def euler():
    now = current_time_millis()
    t_n, y_n = initial_conditions

    while current_time_millis() - now < duration:

        write_to_csv('euler.csv', t_n, y_n)

        y_n += h * differential_equation(a, b, y_n)
        t_n = t_n + h

    print(f"Euler method has run for {duration/1000} second(s)\n")

# The 4th order Runge-Kutta method (RK4) for numerical approximation of solution to differential equations
def runge_kutta():
    now = current_time_millis()
    t_n, y_n = initial_conditions

    while current_time_millis() - now < duration:

        write_to_csv('rungekutta.csv', t_n, y_n)

        k1 = differential_equation(a, b, y_n)
        k2 = differential_equation(a, b, y_n + (h * (k1/2)))
        k3 = differential_equation(a, b, y_n + (h * (k2/2)))
        k4 = differential_equation(a, b, y_n + (h * k3))

        y_n += (h/6) * (k1 + 2 * k2 + 2 * k3 + k4)
        t_n = t_n + h

    print(f"\nRunge-Kutta method has run for {duration/1000} second(s)")

# This function compares the output data of the numerical solutions to the real explicit solution 
def create_method_analysis(method):
    with open(f'{method}.csv', 'r') as csvfile:
        reader_obj = csv.reader(csvfile)
        for row in reader_obj:
                # Accuracy metric based on the relationship between numerical approximation and real solution at t_n
                # The accuracy metric is bounded to [0, 1] where 1 means perfect accuracy
                # The metric is logarithmically symmetric in ratio-space 
                y_solution = solution(a, b, float(row[0]))
                y_approximation = float(row[1])
                accuracy = math.exp(math.log(abs((safe_divide(y_approximation, y_solution)))))
                # Creates a CSV-file holding the method-specific accuracy metric for each value of t_n
                # Errorhandling in case the accuracy value is a number - Ignores the case of initial_value = (0, 0)
                if not math.isnan(accuracy):
                    write_to_csv(f'{method}_accuracy.csv', row[0], accuracy)
                elif y_solution == y_approximation:
                    write_to_csv(f'{method}_accuracy.csv', row[0], 1)
                    print(f"[Notice] Overriding ZeroDivisionError as y_solution == y_approximation at ({row[0]}, {y_approximation}) for method '{method}'")
                else:
                    print(f"[Warning] NaN encountered for accuracy at t_n = {row[0]} for method '{method}'")        

    print(f"Finished analysis of method '{method}'\n")

if __name__ == "__main__":
    runge_kutta()
    euler()
    for method in ['rungekutta', 'euler']:
        create_method_analysis(method)