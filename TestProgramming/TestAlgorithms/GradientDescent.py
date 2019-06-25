import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# y = mx + b, using batch gradient descent
# m is slope, b is y-intercept
# in current project x is setpoint of circuit, y is temperature of distributor
# initial guess: m = mean(y) / mean(x), b = y(1) - m * x(1)


def compute_error_for_given_points(b, m, points):  # points is array object with n rows(sample size) and 2 columns
    totalerror = 0
    for i in range(len(points)):  # len(points) is the number of data samples, e.g. 21
        x = points.iloc[i, 0]  # x-value at (i+1)-te data sample
        y = points.iloc[i, 1]  # y-value at (i+1)-te data sample
        totalerror += (y - (m * x + b)) ** 2
    return totalerror / (2*len(points))  # Value of cost function with given value of m and b


def step_gradient(b_current, m_current, points, alpha):   # alpha is learning rate / step size
    b_gradient = 0
    m_gradient = 0
    n = len(points)  # sample size
    for i in range(len(points)):
        x = points.iloc[i, 0]
        y = points.iloc[i, 1]
        b_gradient += (1/n) * ((m_current * x + b_current) - y)  # compute derivation for b with iteration
        m_gradient += (1/n) * x * ((m_current * x + b_current) - y)  # compute derivation for m with iteration
    new_b = b_current - (alpha * b_gradient)  # new b after iteration along negative gradient
    new_m = m_current - (alpha * m_gradient)  # new m after iteration along negative gradient
    return [new_b, new_m]


def gradient_descent_runner(points, starting_b, starting_m, alpha, num_iterations):
    b = starting_b
    m = starting_m
    for i in range(num_iterations):
        b, m = step_gradient(b, m, points, alpha)
    return [b, m]


def run():
    points = pd.read_csv('C:/Users/yuche/Desktop/Masterarbeit/MA_Python/data2.csv', names=['Setpoint', 'Temp_Distr'])
    alpha = 0.01
    mean_x = np.mean(points.Setpoint)
    mean_y = np.mean(points.Temp_Distr)
    initial_m = mean_y / mean_x  # initial slope guess
    initial_b = points.iloc[0, 1] - points.iloc[0, 0] * initial_m  # initial y-intercept guess
    num_iterations = 10000
    print("Starting gradient descent at b = {0}, m = {1}, error = {2}".
          format(initial_b, initial_m, compute_error_for_given_points(initial_b, initial_m, points)))
    print("Running...")
    [b, m] = gradient_descent_runner(points, initial_b, initial_m, alpha, num_iterations)
    print("After {0} iterations b = {1}, m = {2}, error = {3}".format(num_iterations, b, m,
                                                                      compute_error_for_given_points(b, m, points)))
    return [b, m]


if __name__ == '__main__':
    [final_b, final_m] = run()
    # Visualization
    data = pd.read_csv('C:/Users/yuche/Desktop/Masterarbeit/MA_Python/data2.csv', names=['Setpoint', 'Temp_Distr'])
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set(ylim=[48, 80], ylabel='Temp', xlabel='Setvalue')
    plt.xticks([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1],
               ['0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%'])
    ax.set_title('Test_distributor', fontsize=15)
    ax.scatter(data.Setpoint, data.Temp_Distr, c='b', s=20, label='Data', marker='x', alpha=0.9)
    f_x = final_m * data.Setpoint + final_b  # Predection according to Gradient Descent
    ax.plot(data.Setpoint, f_x, c='r', linewidth=1.5, linestyle='-', label='Prediction')
    ax.legend(loc='upper left')
    plt.show()
