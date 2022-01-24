from matplotlib import pyplot as plt
import pandas as pd

def angle_ploter(angle_file):
    phi_psi = pd.read_csv(angle_file, delim_whitespace=True)
    angles = [phi_psi.columns]
    plots = len(angles[0])
    if plots < 6 :
        x , y = 1, 5
    elif plots >=6 and plots < 13:
        x, y = 2, 6
    else:
        x , y = 3 , 10
    ax = plt.figure(figsize=(20,8))
    ax = plt.title(f'{phi_psi}')
    for i in range(plots):
        plt.subplot(x, y, i+1)
        plt.title(f'{angle_file[0:3]} {angles[0][i]}')
        plt.plot(phi_psi[angles[0][i]])
    plt.tight_layout()
    plt.show()

angle_ploter(input("file to plot 'phi.txt or psi.txt'> "))