class Job:
    def __init__(self, Job_index, Operation_num):
        self.Job_index = Job_index  # 工件序号
        self.Operation_num = Operation_num  # 工序数
        self.Processed = []  # 记录工件工序的加工进度
        self.J_start = []  # 记录工件工序的开始时间
        self.J_end = []  # 记录工件工序的结束时间
        self.J_machine = []  # 记录工件工序选择的机器
        self.Last_Processing_Machine = None  # 工件当前工序的加工机器
        self.Last_Processing_end_time = 0  # 工件当前工序的结束时间

    def Current_Processed(self):
        return len(self.Processed)

    def _Input(self, W_Eailiest, End_time, Machine):  # 工件当前工序的开始时间、结束时间、选择加工机器
        self.Last_Processing_Machine = Machine
        self.Last_Processing_end_time = End_time
        self.Processed.append(1)
        self.J_start.append(W_Eailiest)
        self.J_end.append(End_time)
        self.J_machine.append(Machine)
