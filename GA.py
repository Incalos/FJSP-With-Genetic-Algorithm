import itertools
import random

import numpy as np

from Decode import Decode
from Instance import *


class GA():
    def __init__(self):
        self.Pop_size = 400  # 种群数量
        self.Pc = 0.8  # 交叉概率
        self.Pm = 0.3  # 变异概率
        self.Pv = 0.5  # 选择何种方式进行交叉的概率阈值
        self.Pw = 0.95  # 选择何种方式进行变异的概率阈值
        self.Max_Itertions = 100  # 最大迭代次数

    # 适应度
    def fitness(self, CHS, J, Processing_time, M_num, Len):
        Fit = []
        for i in range(len(CHS)):
            d = Decode(J, Processing_time, M_num)
            Fit.append(d.decode(CHS[i], Len))
        return Fit

    # 机器部分交叉
    def machine_cross(self, CHS1, CHS2, T0):
        """
        :param CHS1: 机器选择部分的基因1
        :param CHS2: 机器选择部分的基因2
        :param T0: 工序总数
        :return: 交叉后的机器选择部分的基因
        """
        T_r = [j for j in range(T0)]
        r = random.randint(1, 10)  # 在区间[1,T0]内产生一个整数r
        random.shuffle(T_r)
        R = T_r[0:r]  # 按照随机数r产生r个互不相等的整数
        OS_1 = CHS1[O_num:2 * T0]
        OS_2 = CHS2[O_num:2 * T0]
        MS_1 = CHS2[0:T0]
        MS_2 = CHS1[0:T0]
        for i in R:
            K, K_2 = MS_1[i], MS_2[i]
            MS_1[i], MS_2[i] = K_2, K
        CHS1 = np.hstack((MS_1, OS_1))
        CHS2 = np.hstack((MS_2, OS_2))
        return CHS1, CHS2

    # 工序部分交叉
    def operation_cross(self, CHS1, CHS2, T0, J_num):
        """
        :param CHS1: 工序选择部分的基因1
        :param CHS2: 工序选择部分的基因2
        :param T0: 工序总数
        :param J_num: 工件总数
        :return: 交叉后的工序选择部分的基因
        """
        OS_1 = CHS1[T0:2 * T0]
        OS_2 = CHS2[T0:2 * T0]
        MS_1 = CHS1[0:T0]
        MS_2 = CHS2[0:T0]
        Job_list = [i for i in range(J_num)]
        random.shuffle(Job_list)
        r = random.randint(1, J_num - 1)
        Set1 = Job_list[0:r]
        new_os = list(np.zeros(T0, dtype=int))
        for k, v in enumerate(OS_1):
            if v in Set1:
                new_os[k] = v + 1
        for i in OS_2:
            if i not in Set1:
                Site = new_os.index(0)
                new_os[Site] = i + 1
        new_os = np.array([j - 1 for j in new_os])
        CHS1 = np.hstack((MS_1, new_os))
        CHS2 = np.hstack((MS_2, new_os))
        return CHS1, CHS2

    # 机器部分变异
    def machine_variation(self, CHS, O, T0, J):
        """
        :param CHS: 机器选择部分的基因
        :param O: 加工时间矩阵
        :param T0: 工序总数
        :param J: 各工件加工信息
        :return: 变异后的机器选择部分的基因
        """
        Tr = [i_num for i_num in range(T0)]
        MS = CHS[0:T0]
        OS = CHS[T0:2 * T0]
        # 机器选择部分
        r = random.randint(1, T0 - 1)  # 在变异染色体中选择r个位置
        random.shuffle(Tr)
        T_r = Tr[0:r]
        for num in T_r:
            T_0 = [j for j in range(T0)]
            K = []
            Site = 0
            for k, v in J.items():
                K.append(T_0[Site:Site + v])
                Site += v
            for i in range(len(K)):
                if num in K[i]:
                    O_i = i
                    O_j = K[i].index(num)
                    break
            Machine_using = O[O_i][O_j]
            Machine_time = []
            for j in Machine_using:
                if j != 9999:
                    Machine_time.append(j)
            Min_index = Machine_time.index(min(Machine_time))
            MS[num] = Min_index
        CHS = np.hstack((MS, OS))
        return CHS

    # 工序部分变异
    def operation_variation(self, CHS, T0, J_num, J, O, M_num):
        """
        :param CHS: 工序选择部分的基因
        :param T0: 工序总数
        :param J_num: 工件总数
        :param J: 各工件加工信息
        :param O: 加工时间矩阵
        :param M_num: 机器总数
        :return: 变异后的工序选择部分的基因
        """
        MS = CHS[0:T0]
        OS = list(CHS[T0:2 * T0])
        r = random.randint(1, J_num - 1)
        Tr = [i for i in range(J_num)]
        random.shuffle(Tr)
        Tr = Tr[0:r]
        J_os = dict(enumerate(OS))  # 随机选择r个不同的基因
        J_os = sorted(J_os.items(), key=lambda d: d[1])
        Site = []
        for i in range(r):
            Site.append(OS.index(Tr[i]))
        A = list(itertools.permutations(Tr, r))
        A_CHS = []
        for i in range(len(A)):
            for j in range(len(A[i])):
                OS[Site[j]] = A[i][j]
            C_I = np.hstack((MS, OS))
            A_CHS.append(C_I)
        Fit = []
        for i in range(len(A_CHS)):
            d = Decode(J, O, M_num)
            Fit.append(d.decode(CHS, T0))
        return A_CHS[Fit.index(min(Fit))]
