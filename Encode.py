import random

import numpy as np


class Encode:
    def __init__(self, Matrix, Pop_size, J, J_num, M_num, O_num):  # Pop_size 种群数量
        self.Matrix = Matrix  # 工件各工序对应各机器加工时间矩阵
        self.Pop_size = Pop_size  # 种群数量
        self.J = J  # 各工件对应的工序数
        self.J_num = J_num  # 工件数
        self.M_num = M_num  # 机器数
        self.O_num = O_num  # 工序数

    # 生成工序准备的部分，便于后续基因的工序排序部分编码
    def OS_List(self):
        OS_list = []
        for k, v in self.J.items():
            OS_add = [k - 1 for j in range(v)]
            OS_list.extend(OS_add)
        return OS_list

    # 种群初始化
    def Initial(self):
        MS = np.zeros([self.Pop_size, self.O_num], dtype=int)
        OS_list = self.OS_List()
        OS = np.zeros([self.Pop_size, self.O_num], dtype=int)
        for i in range(self.Pop_size):
            # 生成基因的工序排序部分
            random.shuffle(OS_list)
            OS_gongxu = OS_list
            OS[i] = np.array(OS_gongxu)
            # 生成基因的机器选择部分
            GJ_list = [j for j in range(self.J_num)]
            A = 0
            for gon in GJ_list:
                g = gon  # 随机选择工件集的第一个工件并从工件集中剔除这个工件
                h = np.array(self.Matrix[g])  # 第一个工件及其对应工序的加工时间
                for j in range(len(h)):  # 从工件的第一个工序开始选择机器
                    D = np.array(h[j])
                    List_Machine_weizhi = []
                    Site = 0
                    for k in range(len(D)):  # 每道工序可使用的机器以及机器的加工时间
                        if D[k] == 9999:  # 确定可加工该工序的机器
                            continue
                        else:
                            List_Machine_weizhi.append(Site)
                            Site += 1
                    Machine_Index_add = random.choice(List_Machine_weizhi)
                    MS[i][A] = MS[i][A] + Machine_Index_add
                    A += 1
        CHS = np.hstack((MS, OS))
        return CHS  # 种群基因
