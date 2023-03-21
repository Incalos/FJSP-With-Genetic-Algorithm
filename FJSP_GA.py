import random

import matplotlib.pyplot as plt
import numpy as np

from Decode import Decode
from Encode import Encode
from GA import GA
from Instance import *


def Gantt(Machines):
    M = ['red', 'blue', 'yellow', 'orange', 'green', 'palegoldenrod', 'purple', 'pink', 'Thistle', 'Magenta',
         'SlateBlue', 'RoyalBlue', 'Cyan', 'Aqua', 'floralwhite', 'ghostwhite', 'goldenrod', 'mediumslateblue',
         'navajowhite', 'navy', 'sandybrown', 'moccasin']
    for i in range(len(Machines)):
        Machine = Machines[i]
        Start_time = Machine.O_start
        End_time = Machine.O_end
        for i_1 in range(len(End_time)):
            plt.barh(i, width=End_time[i_1] - Start_time[i_1], height=0.8, left=Start_time[i_1],
                     color=M[Machine.assigned_task[i_1][0] - 1], edgecolor='black')
            plt.text(x=Start_time[i_1] + (End_time[i_1] - Start_time[i_1]) / 2 - 0.5, y=i,
                     s=Machine.assigned_task[i_1][0])
    plt.yticks(np.arange(len(Machines) + 1), np.arange(1, len(Machines) + 2))
    plt.title('Scheduling Gantt chart')
    plt.ylabel('Machines')
    plt.xlabel('Time(min)')
    plt.savefig('优化后排程方案的甘特图.png')
    plt.show()


if __name__ == '__main__':
    Optimal_fit = 9999  # 最佳适应度（初始化）
    Optimal_CHS = 0  # 最佳适应度对应的基因个体（初始化）
    g = GA()
    e = Encode(Processing_time, g.Pop_size, J, J_num, M_num, O_num)
    C = e.Initial()
    Best_fit = []  # 记录适应度在迭代过程中的变化，便于绘图
    for i in range(g.Max_Itertions):
        print("iter_{} start!".format(i))
        Fit = g.fitness(C, J, Processing_time, M_num, O_num)
        Best = C[Fit.index(min(Fit))]
        best_fitness = min(Fit)
        if best_fitness < Optimal_fit:
            Optimal_fit = best_fitness
            Optimal_CHS = Best
            Best_fit.append(Optimal_fit)
            print('best_fitness', best_fitness)
            d = Decode(J, Processing_time, M_num)
            Fit.append(d.decode(Optimal_CHS, O_num))
            Gantt(d.Machines)
        else:
            Best_fit.append(Optimal_fit)
        for j in range(len(C)):
            Cafter = []
            if random.random() < g.Pc:
                N_i = random.choice(np.arange(len(C)))
                if random.random() < g.Pv:
                    Cross = g.machine_cross(C[j], C[N_i], O_num)
                else:
                    Cross = g.operation_cross(C[j], C[N_i], O_num, J_num)
                Cafter.append(Cross[0])
                Cafter.append(Cross[1])
                Cafter.append(C[j])
            if random.random() < g.Pm:
                if random.random() < g.Pw:
                    Variance = g.machine_variation(C[j], Processing_time, O_num, J)
                else:
                    Variance = g.operation_variation(C[j], O_num, J_num, J, Processing_time, M_num)
                Cafter.append(Variance)
            if Cafter != []:
                Fit = g.fitness(Cafter, J, Processing_time, M_num, O_num)
                C[j] = Cafter[Fit.index(min(Fit))]
    # 绘制甘特图
    x = np.linspace(0, 50, g.Max_Itertions)
    plt.plot(x, Best_fit, '-k')
    plt.title('the maximum completion time of each iteration')
    plt.ylabel('Cmax')
    plt.xlabel('Test Num')
    plt.savefig('最大完成时间的优化过程.png')
    plt.show()
