import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from numpy import dot

# using batch gradient descent
# y = theta0 + theta1 * x ..., theta as parameter matrix (row=1) consisting of all theta value
# theta1, theta2 ... is slope, theta0 is y-intercept
# in current project x is setpoint of circuit, y is temperature of distributor
# initial guess: m = mean(y) / mean(x), b = y(1) - m * x(1)
# solution with method of least squares: theta = (x'x)^(-1)x'y, dot(dot(inv(dot(X.T, X)), X.T), y)


def training_data_processing():
    data_original = pd.read_csv('C:/Users/yuche/Desktop/Masterarbeit/MA_Python/data2.csv', names=['Setpoint',
                                                                                                  'Temp_Distr'])
    data_original.insert(0, 'Ones', 1)  # insert one column
    n = int(data_original.shape[0])  # sample size
    col = data_original.shape[1] - 1  # column of original DataFrame
    x = np.mat(data_original.iloc[:, :col].values)  # variable x as matrix (n*col)
    y = np.mat(data_original.iloc[:, -1].values)  # target variable y as matrix (1*n)
    y = y.T  # target variable y as matrix (n*1)
    return x, y, n


def compute_error_for_given_points(theta):  # theta as parameter matrix (row vector)
    x, y, n = training_data_processing()
    innererror = np.power((dot(x, theta.T) - y), 2)  # matrix (n*1)
    totalerror = np.sum(innererror)
    return totalerror / (2*n)  # value of cost function with given theta value


def gradient_descent_runner(alpha, epsilon):   # alpha as learning rate, epsilon as threshold for stopping iteration
    x, y, n = training_data_processing()
    theta = np.mat(np.zeros(x.shape[1]))  # zero matrix, initial guess: all theta parameter as 0
    theta_new = np.mat(np.zeros(theta.shape))  # zero matrix for iteration
    num_parameter = int(theta.shape[1])  # number of parameter theta
    error0 = 0
    cost = []
    while True:
        error1 = compute_error_for_given_points(theta)
        cost.append(error1)  # list of cost function for each iteration
        for i in range(num_parameter):
            gradient = np.multiply((dot(x, theta.T) - y), x[:, i]) / n  # compute derivation for one parameter
            theta_new[0, i] = theta[0, i] - (alpha * np.sum(gradient))  # new parameter after iteration
        theta = theta_new
        if abs(error1 - error0) > epsilon:
            error0 = error1
        else:
            break  # stop iteration when reaching threshold
    num_iter = len(cost)
    return theta, cost, num_iter


if __name__ == '__main__':
    a = input('please input appropriate learning rate:')
    alpha_input = float(a)
    e = input('please input appropriate threshold value:')
    epsilon_input = float(e)
    # Visualization
    theta_final, cost_final, num_iter_final = gradient_descent_runner(alpha_input, epsilon_input)
    theta_initial = np.mat(np.array([0, 0]))
    print('Starting gradient descent, vector of parameters = {0}, error = {1}'.
          format(theta_initial, compute_error_for_given_points(theta_initial)))
    print('Running...')
    print('Done after {0} iterations, vector of parameters = {1}, error = {2}'.
          format(num_iter_final, theta_final, cost_final[-1]))
    # plot training data and curve fitting
    data = pd.read_csv('C:/Users/yuche/Desktop/Masterarbeit/MA_Python/data2.csv', names=['Setpoint', 'Temp_Distr'])
    fig, ax1 = plt.subplots(figsize=(7, 5))
    ax1.set(ylim=[48, 80], ylabel='Temp', xlabel='Setvalue')
    plt.xticks([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1],
               ['0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%'])
    ax1.set_title('Test_distributor', fontsize=13)
    ax1.scatter(data.Setpoint, data.Temp_Distr, c='b', s=20, label='Data', marker='x', alpha=0.9)
    f_x = theta_final[0, 1] * data.Setpoint + theta_final[0, 0]  # predection according to Gradient Descent
    ax1.plot(data.Setpoint, f_x, c='r', linewidth=1.5, linestyle='-', label='Prediction')
    ax1.annotate('y = %.3f + %.3fx' % (theta_final[0, 0], theta_final[0, 1]),
                 xy=(0.5, theta_final[0, 1] * 0.5 + theta_final[0, 0]),
                 xycoords='data', xytext=(-120, +50), textcoords='offset points', fontsize=12,
                 arrowprops=dict(arrowstyle='->', connectionstyle="arc3,rad=.2"))
    ax1.legend(loc='upper left')
    plt.show()
    # plot iteration process
    cost_array = np.zeros(num_iter_final)
    for j in range(num_iter_final):
        cost_array[j] = float(cost_final[j])
    fig, ax2 = plt.subplots(figsize=(7, 5))
    ax2.set(ylabel='Cost', xlabel='Number of iterations')
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.set_title('Iteration process with learning rate = %s' % a, fontsize=13)
    ax2.plot(np.arange(num_iter_final), cost_array, c='darkgreen', linewidth=1.4, linestyle='-', label='Iter')
    ax2.legend(loc='upper right')
    plt.show()
