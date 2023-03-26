import numpy as np

from Job import Job
from Machine import Machine_Time_window


class Decode:
    def __init__(self, J, Processing_time, M_num):
        """
        :param J: 各工件对应的工序数字典
        :param Processing_time: 各工件的加工时间矩阵
        :param M_num: 加工机器数
        """
        self.Processing_time = Processing_time
        self.M_num = M_num
        self.J = J
        self.Machines = []  # 存储机器类
        self.Scheduled = []  # 已经排产过的工序
        self.fitness = 0  # 适应度
        self.Machine_State = np.zeros(M_num, dtype=int)  # 在机器上加工的工件是哪个
        self.Jobs = []  # 存储工件类
        for j in range(M_num):
            self.Machines.append(Machine_Time_window(j))
        for k, v in J.items():
            self.Jobs.append(Job(k, v))

    # 时间顺序矩阵和机器顺序矩阵，根据基因的MS部分转换
    def Order_Matrix(self, MS):
        JM = []
        T = []
        Ms_decompose = []
        Site = 0
        # 按照基因的MS部分按工件序号划分
        for S_i in self.J.values():
            Ms_decompose.append(MS[Site:Site + S_i])
            Site += S_i
        for i in range(len(Ms_decompose)):  # len(Ms_decompose)表示工件数
            JM_i = []
            T_i = []
            for j in range(len(Ms_decompose[i])):  # len(Ms_decompose[i])表示每一个工件对应的工序数
                O_j = self.Processing_time[i][j]  # 工件i的工序j可选择的加工时间列表
                M_ij = []
                T_ij = []
                for Mac_num in range(len(O_j)):  # 寻找MS对应部分的机器时间和机器顺序
                    if O_j[Mac_num] != 9999:
                        M_ij.append(Mac_num)
                        T_ij.append(O_j[Mac_num])
                    else:
                        continue
                JM_i.append(M_ij[Ms_decompose[i][j]])
                T_i.append(T_ij[Ms_decompose[i][j]])
            JM.append(JM_i)
            T.append(T_i)
        return JM, T

    # 确定工序的最早加工时间
    def Earliest_Start(self, Job, O_num, Machine):
        P_t = self.Processing_time[Job][O_num][Machine]
        last_O_end = self.Jobs[Job].Last_Processing_end_time  # 上道工序结束时间
        Selected_Machine = Machine
        M_window = self.Machines[Selected_Machine].Empty_time_window()  # 当前机器的空格时间
        M_Tstart = M_window[0]
        M_Tend = M_window[1]
        M_Tlen = M_window[2]
        Machine_end_time = self.Machines[Selected_Machine].End_time
        ealiest_start = max(last_O_end, Machine_end_time)
        if M_Tlen is not None:  # 此处为全插入时窗
            for le_i in range(len(M_Tlen)):
                # 当前空格时间比加工时间大可插入
                if M_Tlen[le_i] >= P_t:
                    # 当前空格开始时间比该工件上一工序结束时间大可插入该空格，以空格开始时间为这一工序开始
                    if M_Tstart[le_i] >= last_O_end:
                        ealiest_start = M_Tstart[le_i]
                        break
                    # 当前空格开始时间比该工件上一工序结束时间小但空格可满足插入该工序，以该工序的上一工序的结束为开始
                    if M_Tstart[le_i] < last_O_end and M_Tend[le_i] - last_O_end >= P_t:
                        ealiest_start = last_O_end
                        break
        M_Ealiest = ealiest_start  # 当前工件当前工序的最早开始时间
        End_work_time = M_Ealiest + P_t  # 当前工件当前工序的结束时间
        return M_Ealiest, Selected_Machine, P_t, O_num, last_O_end, End_work_time

    # 解码操作
    def decode(self, CHS, Len_Chromo):
        """
        :param CHS: 种群基因
        :param Len_Chromo: MS与OS的分解线
        :return: 适应度，即最大加工时间
        """
        MS = list(CHS[0:Len_Chromo])
        OS = list(CHS[Len_Chromo:2 * Len_Chromo])
        Needed_Matrix = self.Order_Matrix(MS)
        JM = Needed_Matrix[0]
        for i in OS:
            Job = i
            O_num = self.Jobs[Job].Current_Processed()  # 现在加工的工序
            Machine = JM[Job][O_num]  # 用基因的OS部分的工件序号以及工序序号索引机器顺序矩阵的机器序号
            Para = self.Earliest_Start(Job, O_num, Machine)
            self.Jobs[Job]._Input(Para[0], Para[5], Para[1])  # 工件完成该工序
            if Para[5] > self.fitness:
                self.fitness = Para[5]
            self.Machines[Machine]._Input(Job, Para[0], Para[2], Para[3])  # 机器完成该工件该工序
        return self.fitness
