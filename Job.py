class Job:
    def __init__(self, Job_index, Operation_num):
        """
        :param Job_index: 工件序号
        :param Operation_num: 工序数
        """
        self.Job_index = Job_index
        self.Operation_num = Operation_num
        self.Processed = []  # 记录工件工序的加工进度
        self.J_start = []  # 记录工件工序的开始时间
        self.J_end = []  # 记录工件工序的结束时间
        self.J_machine = []  # 记录工件工序选择的机器
        self.Last_Processing_Machine = None  # 工件当前工序的加工机器
        self.Last_Processing_end_time = 0  # 工件当前工序的结束时间

    # 工件已经加工的工序数
    def Current_Processed(self):
        return len(self.Processed)

    # 工件某工序开始加工
    def _Input(self, W_Eailiest, End_time, Machine):
        """
        :param W_Eailiest: 工件当前工序的开始时间
        :param End_time: 工件当前工序的结束时间
        :param Machine: 工件当前工序选择的加工机器
        :return:
        """
        self.Last_Processing_Machine = Machine
        self.Last_Processing_end_time = End_time
        self.Processed.append(1)
        self.J_start.append(W_Eailiest)
        self.J_end.append(End_time)
        self.J_machine.append(Machine)
