import random

import numpy as np


class Encode:
    def __init__(self, Matrix, Pop_size, J, J_num, M_num):
        """
        :param Matrix: 机器加工时间矩阵
        :param Pop_size: 种群数量
        :param J: 各工件对应的工序数
        :param J_num: 工件数
        :param M_num: 机器数
        """
        self.Matrix = Matrix
        self.J = J
        self.J_num = J_num
        self.M_num = M_num
        self.CHS = []
        self.GS_num = int(0.6 * Pop_size)  # 全局选择初始化
        self.LS_num = int(0.2 * Pop_size)  # 局部选择初始化
        self.RS_num = int(0.2 * Pop_size)  # 随机选择初始化
        self.Len_Chromo = 0
        for i in J.values():
            self.Len_Chromo += i

    # 生成工序准备的部分
    def OS_List(self):
        OS_list = []
        for k, v in self.J.items():
            OS_add = [k - 1 for j in range(v)]
            OS_list.extend(OS_add)
        return OS_list

    # 生成初始化矩阵
    def CHS_Matrix(self, C_num):
        return np.zeros([C_num, self.Len_Chromo], dtype=int)

    # 定位每个工件的每道工序的位置
    def Site(self, Job, Operation):
        O_num = 0
        for i in range(len(self.J)):
            if i == Job:
                return O_num + Operation
            else:
                O_num = O_num + self.J[i + 1]
        return O_num

    # 全局初始化
    def Global_initial(self):
        MS = self.CHS_Matrix(self.GS_num)  # 根据GS_num生成种群
        OS_list = self.OS_List()
        OS = self.CHS_Matrix(self.GS_num)
        for i in range(self.GS_num):
            Machine_time = np.zeros(self.M_num, dtype=int)  # 步骤1 生成一个整型数组，长度为机器数，且初始化每个元素为0
            random.shuffle(OS_list)  # 生成工序排序部分
            OS[i] = np.array(OS_list)  # 随机打乱后将其赋值给OS的某一行（因为有一个种群，第i则是赋值在OS的第i行，以此生成完整的OS）
            GJ_list = [i_1 for i_1 in range(self.J_num)]  # 生成工件集
            random.shuffle(GJ_list)  # 随机打乱工件集,为的是下一步可以随机抽出第一个工件
            for g in GJ_list:  # 选择第一个工件（由于上一步已经打乱工件集，抽出第一个也是“随机”）
                h = self.Matrix[g]  # h为第一个工件包含的工序对应的时间矩阵
                for j in range(len(h)):  # 从此工件的第一个工序开始
                    D = h[j]  # D为第一个工件的第一个工序对应的时间矩阵
                    List_Machine_weizhi = []
                    for k in range(len(D)):  # 确定工序可用的机器位于第几个位置
                        Useing_Machine = D[k]
                        if Useing_Machine != 9999:
                            List_Machine_weizhi.append(k)
                    Machine_Select = []
                    for Machine_add in List_Machine_weizhi:  # 将机器时间数组对应位置和工序可选机器的时间相加
                        Machine_Select.append(Machine_time[Machine_add] + D[Machine_add])
                    Min_time = min(Machine_Select)  # 选出时间最小的机器
                    K = Machine_Select.index(Min_time)  # 第一次出现最小时间的位置，确定最小负荷为哪个机器,即为该工序可选择的机器里的第K个机器，并非Mk
                    I = List_Machine_weizhi[K]  # 所有机器里的第I个机器，即Mi
                    Machine_time[I] += Min_time  # 相应的机器位置加上最小时间
                    site = self.Site(g, j)  # 定位每个工件的每道工序的位置
                    MS[i][site] = K  # 即将每个工序选择的第K个机器赋值到每个工件的每道工序的位置上去 即生成MS的染色体
        CHS1 = np.hstack((MS, OS))  # 将MS和OS整合为一个矩阵
        return CHS1

    # 局部初始化
    def Local_initial(self):
        MS = self.CHS_Matrix(self.LS_num)  # 根据LS_num生成局部选择的种群大小
        OS_list = self.OS_List()
        OS = self.CHS_Matrix(self.LS_num)
        for i in range(self.LS_num):
            random.shuffle(OS_list)  # 生成工序排序部分
            OS[i] = np.array(OS_list)  # 随机打乱后将其赋值给OS的某一行（因为有一个种群，第i则是赋值在OS的第i行，以此生成完整的OS）
            GJ_List = [i_1 for i_1 in range(self.J_num)]  # 生成工件集
            for g in GJ_List:  # 选择第一个工件（注意：不用随机打乱了）
                Machine_time = np.zeros(self.M_num,
                                        dtype=int)  # 设置一个整型数组 并初始化每一个元素为0，由于局部初始化，每个工件的所有工序结束后都要重新初始化，所以和全局初始化不同，此步骤应放在此处
                h = self.Matrix[g]  # h为第一个工件包含的工序对应的时间矩阵
                for j in range(len(h)):  # 从选择的工件的第一个工序开始
                    D = h[j]  # 此工件第一个工序对应的机器加工时间矩阵
                    List_Machine_weizhi = []
                    for k in range(len(D)):  # 确定工序可用的机器位于第几个位置
                        Useing_Machine = D[k]
                        if Useing_Machine != 9999:
                            List_Machine_weizhi.append(k)
                    Machine_Select = []
                    for Machine_add in List_Machine_weizhi:  # 将机器时间数组对应位置和工序可选机器的时间相加
                        Machine_Select.append(Machine_time[Machine_add] + D[Machine_add])
                    Min_time = min(Machine_Select)  # 选出这些时间里最小的
                    K = Machine_Select.index(Min_time)  # 第一次出现最小时间的位置，确定最小负荷为哪个机器,即为该工序可选择的机器里的第K个机器，并非Mk
                    I = List_Machine_weizhi[K]  # 所有机器里的第I个机器，即Mi
                    Machine_time[I] += Min_time
                    site = self.Site(g, j)  # 定位每个工件的每道工序的位置
                    MS[i][site] = K  # 即将每个工序选择的第K个机器赋值到每个工件的每道工序的位置上去
        CHS1 = np.hstack((MS, OS))  # 将MS和OS整合为一个矩阵
        return CHS1

    # 随机初始化
    def Random_initial(self):
        MS = self.CHS_Matrix(self.RS_num)  # 根据RS_num生成随机选择的种群大小
        OS_list = self.OS_List()
        OS = self.CHS_Matrix(self.RS_num)
        for i in range(self.RS_num):
            random.shuffle(OS_list)
            OS[i] = np.array(OS_list)
            GJ_List = [i_1 for i_1 in range(self.J_num)]  # 生成工件集
            for g in GJ_List:  # 选择第一个工件
                h = self.Matrix[g]
                for j in range(len(h)):  # 选择第一个工件的第一个工序
                    D = h[j]  # 此工件第一个工序可加工的机器对应的时间矩阵
                    List_Machine_weizhi = []
                    for k in range(len(D)):
                        Useing_Machine = D[k]
                        if Useing_Machine != 9999:
                            List_Machine_weizhi.append(k)
                    number = random.choice(List_Machine_weizhi)  # 从可选择的机器编号中随机选择一个（此编号就是机器编号）
                    K = List_Machine_weizhi.index(number)  # 即为该工序可选择的机器里的第K个机器，并非Mk
                    site = self.Site(g, j)  # 定位每个工件的每道工序的位置
                    MS[i][site] = K  # 即将每个工序选择的第K个机器赋值到每个工件的每道工序的位置上去
        CHS1 = np.hstack((MS, OS))
        return CHS1
