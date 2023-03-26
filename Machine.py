class Machine_Time_window:
    def __init__(self, Machine_index):
        """
        :param Machine_index: 加工机器序号
        """
        self.Machine_index = Machine_index
        self.assigned_task = []  # 机器分配的任务记录，包括工件序号以及工序序号
        self.O_start = []  # 各任务工序的开始时间记录
        self.O_end = []  # 各任务工序的结束时间记录
        self.End_time = 0

    # 机器的哪些时间窗是空的,此处只考虑内部封闭的时间窗,类似甘特图每一行往后叠加
    def Empty_time_window(self):
        """
        :return: 空格时间的开始、结束、时长
        """
        time_window_start = []
        time_window_end = []
        len_time_window = []
        if self.O_end is None:
            pass
        elif len(self.O_end) == 1:
            if self.O_start[0] != 0:
                time_window_start = [0]
                time_window_end = [self.O_start[0]]
        elif len(self.O_end) > 1:
            if self.O_start[0] != 0:
                time_window_start.append(0)
                time_window_end.append(self.O_start[0])
            time_window_start.extend(self.O_end[:-1])  # 因为使用时间窗的结束点就是空时间窗的开始点
            time_window_end.extend(self.O_start[1:])
        if time_window_end is not None:
            len_time_window = [time_window_end[i] - time_window_start[i] for i in range(len(time_window_end))]
        return time_window_start, time_window_end, len_time_window

    # 机器投入新一轮加工
    def _Input(self, Job, M_Ealiest, P_t, O_num):
        if self.O_end != []:
            # 如果当前机器加工的最早开始时间比记录的大，则依次往后排任务，否则将任务插入中间的分配任务记录
            if self.O_start[-1] > M_Ealiest:
                for i in range(len(self.O_end)):
                    if self.O_start[i] >= M_Ealiest:
                        self.assigned_task.insert(i, [Job + 1, O_num + 1])
                        break
            else:
                self.assigned_task.append([Job + 1, O_num + 1])
        else:
            self.assigned_task.append([Job + 1, O_num + 1])
        self.O_start.append(M_Ealiest)
        self.O_start.sort()
        self.O_end.append(M_Ealiest + P_t)
        self.O_end.sort()
        self.End_time = self.O_end[-1]
