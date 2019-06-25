import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_csv('C:/Users/yuche/Desktop/Masterarbeit/MA_Python/data2.csv', names=['setpoint', 'Temp_Distr'])
fig, ax = plt.subplots(figsize=(8, 6))
ax.set(ylim=[48, 80], ylabel='Temp', xlabel='Setvalue')
plt.xticks([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1],
           ['0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%'])
ax.set_title('Test_distributor', fontsize=15)
ax.scatter(data.setpoint, data.Temp_Distr, c='b', s=20, label='Temp', marker='x', alpha=0.9)

ax.legend(loc='upper left')
plt.show()
