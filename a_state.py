import time
import copy


class a_state:
    def __init__(self, chessboard):
        self.chessboard = chessboard
        # open_list:(当前棋盘二维状态，cost+heuristic)
        self.open_list = []
        # closed_list:{棋盘一维状态字符串，cost+heuristic}
        self.close_list = {}
        # depth_list:{棋盘一维状态字符串：深度}
        self.depth_dict = {}
        # 关系表，用来记录父子关系{子一维棋盘:父一维棋盘}
        self.dict_link = {}
        # 记录当前最深
        self.maxdepth = 0

    def a_star(self, maxdep):
        # 记录Node
        self.open_list = [(self.chessboard, self.heuristic(self.chessboard, 2))]
        self.depth_dict = {self.three2one(self.chessboard): 0}
        result = self.chessboard
        # open_list不为空
        while self.open_list:
            # 按照搜索代价排序
            self.open_list.sort(key=lambda open_list: open_list[1])
            # 如果到达最大层数，记录最上层并退出
            # if self.maxdepth > maxdep:
            # result = self.open_list[0][0]
            # break
            # 移除已搜索过的节点
            while self.three2one(self.open_list[0][0]) in self.close_list:
                self.open_list.pop()
            # 若白子已赢，则返回该棋盘
            if self.is_goal(self.open_list[0][0], 2):
                print("本次最大层数：",self.maxdepth)
                result = self.open_list[0][0]
                break
            # 取出估价函数较小数据到open
            top = self.open_list[0]
            self.open_list[0:1] = []
            # 标识该状态已被搜索
            self.close_list[self.three2one(top[0])] = top[1]
            # 得到下一位的所有子结点(列表，其中是一维字符串)
            successors = self.get_successors(top[0])
            # 计算深度
            depth = self.depth_dict[self.three2one(top[0])] + 1
            # 更新深度
            if depth > self.maxdepth:
                self.maxdepth = depth
            # 遍历所有可能性
            for i in successors:
                # 不在close表中
                if i not in self.close_list.keys():
                    kk = -1
                    # 是否在open_list中
                    i1 = self.one2three(i)
                    for l in range(len(self.open_list)):
                        if i1 == self.open_list[l][0]:
                            kk = l
                            break
                    # 不在open_list中
                    if kk == -1:
                        self.open_list.append((i1, depth + self.heuristic(i1, 2)))
                        self.depth_dict[i] = depth
                        self.dict_link[i] = self.three2one(top[0])
                    # 在open_list中
                    else:
                        if self.open_list[kk][1] > depth + self.heuristic(i1, 2):
                            self.open_list[kk][1] = depth + self.heuristic(i1, 2)
                            self.dict_link[i] = self.three2one(top[0])
                            self.depth_dict[i] = depth
        return self.getSource(self.three2one(result), self.three2one(self.chessboard))

    # 一维字符串——二维数组
    def one2three(self, before):
        result = []
        k = 0
        for i in range(15):
            temp = []
            for j in range(15):
                temp.append(int(before[k]))
                k = k + 1
            result.append(temp)
        return result

    # 二维数组——一维字符串
    def three2one(self, before):
        result = []
        for i in range(15):
            for j in range(15):
                result.append(str(before[i][j]))
        return ''.join(result)

    # 输入：棋盘状态，玩家号(2代表白子)，输出：评分
    def heuristic(self, state, player):
        player_score = 0
        opponent_score = 0
        for i in range(15):
            for j in range(15):
                # 遍历到对应颜色
                if state[i][j] == player:
                    # 检测垂直
                    chain = 1
                    for k in range(1, 5):
                        if i + k < 15 and state[i + k][j] == player:
                            chain += 1
                        else:
                            break
                    # 二子连珠
                    if chain == 2:
                        # 一半被堵住
                        if (i == 0 and state[i + 2][j] == 0) or (i == 13 and state[i - 1][j] == 0) or (
                                (i >= 1 and i <= 12) and state[i - 1][j] == 3 - player and state[i + 2][j] == 0) or (
                                (i >= 1 and i <= 12) and state[i + 2][j] == 3 - player and state[i - 1][j] == 0):
                            player_score = player_score + 10
                        # 未被堵住
                        elif (i >= 1 and i <= 12) and state[i + 2][j] == 0 and state[i - 1][j] == 0:
                            player_score = player_score + 30
                    # 三子连珠
                    elif chain == 3:
                        # 一半被堵住
                        if (i == 0 and state[i + 3][j] == 0) or (i == 12 and state[i - 1][j] == 0) or (
                                (i >= 1 and i <= 11) and state[i - 1][j] == 3 - player and state[i + 3][j] == 0) or (
                                (i >= 1 and i <= 11) and state[i + 3][j] == 3 - player and state[i - 1][j] == 0):
                            player_score = player_score + 30
                        # 未被堵住
                        elif (i >= 1 and i <= 11) and state[i + 3][j] == 0 and state[i - 1][j] == 0:
                            player_score = player_score + 60
                    # 四子连珠
                    elif chain == 4:
                        # 一半被堵住
                        if (i == 0 and state[i + 4][j] == 0) or (i == 11 and state[i - 1][j] == 0) or (
                                (i >= 1 and i <= 10) and state[i - 1][j] == 3 - player and state[i + 4][j] == 0) or (
                                (i >= 1 and i <= 10) and state[i + 4][j] == 3 - player and state[i - 1][j] == 0):
                            player_score = player_score + 60
                        # 未被堵住
                        elif (i >= 1 and i <= 10) and state[i + 4][j] == 0 and state[i - 1][j] == 0:
                            player_score = 150000
                    # 五子连珠
                    elif chain == 5:
                        player_score = 1000000
                    # 检测水平
                    chain = 1
                    for k in range(1, 5):
                        if j + k < 15 and state[i][j + k] == player:
                            chain += 1
                        else:
                            break
                    # 二子连珠
                    if chain == 2:
                        # 一半被堵住
                        if (j == 0 and state[i][j + 2] == 0) or (j == 13 and state[i][j - 1] == 0) or (
                                (j >= 1 and j <= 12) and state[i][j - 1] == 3 - player and state[i][j + 2] == 0) or (
                                (j >= 1 and j <= 12) and state[i][j + 2] == 3 - player and state[i][j - 1] == 0):
                            player_score = player_score + 10
                        # 未被堵住
                        elif (j >= 1 and j <= 12) and state[i][j + 2] == 0 and state[i][j - 1] == 0:
                            player_score = player_score + 30
                    # 三子连珠
                    elif chain == 3:
                        # 一半被堵住
                        if (j == 0 and state[i][j + 3] == 0) or (j == 12 and state[i][j - 1] == 0) or (
                                (j >= 1 and j <= 11) and state[i][j - 1] == 3 - player and state[i][j + 3] == 0) or (
                                (j >= 1 and j <= 11) and state[i][j + 3] == 3 - player and state[i][j - 1] == 0):
                            player_score = player_score + 30
                        # 未被堵住
                        elif (j >= 1 and j <= 11) and state[i][j + 3] == 0 and state[i][j - 1] == 0:
                            player_score = player_score + 60
                    # 四子连珠
                    elif chain == 4:
                        # 一半被堵住
                        if (i == 0 and state[i + 4][j] == 0) or (i == 11 and state[i - 1][j] == 0) or (
                                (j >= 1 and j <= 10) and state[i][j - 1] == 3 - player and state[i][j + 4] == 0) or (
                                (j >= 1 and j <= 10) and state[i][j + 4] == 3 - player and state[i][j - 1] == 0):
                            player_score = player_score + 60
                        # 未被堵住
                        elif (j >= 1 and j <= 10) and state[i][j + 4] == 0 and state[i][j - 1] == 0:
                            player_score = 150000
                    # 五子连珠
                    elif chain == 5:
                        player_score = 1000000

                    # 左上到右下
                    chain = 1
                    for k in range(1, 5):
                        if i + k < 15 and j + k < 15 and state[i + k][j + k] == player:
                            chain += 1
                        else:
                            break
                    # 二子连珠
                    if chain == 2:
                        # 一半被堵住
                        if (((j == 0 and i <= 12) or (i == 0 and j <= 12)) and state[i + 2][j + 2] == 0) or (
                                ((j == 13 and i >= 1) or (i == 13 and j >= 1)) and state[i - 1][j - 1] == 0) or (
                                (1 <= i <= 12 and 1 <= j <= 12) and state[i - 1][j - 1] == 3 - player and state[i + 2][
                            j + 2] == 0) or (
                                (1 <= i <= 12 and 1 <= j <= 12) and state[i + 2][j + 2] == 3 - player and state[i - 1][
                            j - 1] == 0):
                            player_score = player_score + 10
                        # 未被堵住
                        elif (1 <= i <= 12 and 1 <= j <= 12) and state[i + 2][j + 2] == 0 and state[i - 1][j - 1] == 0:
                            player_score = player_score + 30
                    # 三子连珠
                    elif chain == 3:
                        # 一半被堵住
                        if (((j == 0 and i <= 11) or (i == 0 and j <= 11)) and state[i + 3][j + 3] == 0) or (
                                ((j == 12 and i >= 1) or (i == 12 and j >= 1)) and state[i - 1][j - 1] == 0) or (
                                (1 <= i <= 11 and 1 <= j <= 11) and state[i - 1][j - 1] == 3 - player and state[i + 3][
                            j + 3] == 0) or (
                                (1 <= i <= 11 and 1 <= j <= 11) and state[i + 3][j + 3] == 3 - player and state[i - 1][
                            j - 1] == 0):
                            player_score = player_score + 30
                        # 未被堵住
                        elif (1 <= i <= 11 and 1 <= j <= 11) and state[i + 3][j + 3] == 0 and state[i - 1][j - 1] == 0:
                            player_score = player_score + 60
                    # 四子连珠
                    elif chain == 4:
                        # 一半被堵住
                        if (((j == 0 and i <= 10) or (i == 0 and j <= 10)) and state[i + 4][j + 4] == 0) or (
                                ((j == 11 and i >= 1) or (i == 11 and j >= 1)) and state[i - 1][j - 1] == 0) or (
                                (1 <= i <= 10 and 1 <= j <= 10) and state[i - 1][j - 1] == 3 - player and state[i + 4][
                            j + 4] == 0) or (
                                (1 <= i <= 10 and 1 <= j <= 10) and state[i + 4][j + 4] == 3 - player and state[i - 1][
                            j - 1] == 0):
                            player_score = player_score + 60
                        # 未被堵住
                        elif (1 <= i <= 10 and 1 <= j <= 10) and state[i + 4][j + 4] == 0 and state[i - 1][j - 1] == 0:
                            player_score = 150000
                    # 五子连珠
                    elif chain == 5:
                        player_score = 1000000

                    # 左下到右上
                    chain = 1
                    for k in range(1, 5):
                        if i - k >= 0 and j + k < 15 and state[i - k][j + k] == player:
                            chain += 1
                        else:
                            break
                    # 二子连珠
                    if chain == 2:
                        # 一半被堵住
                        if (((j == 0 and i >= 2) or (i == 14 and j <= 13)) and state[i - 2][j + 2] == 0) or (
                                ((j == 13 and i <= 13) or (i == 1 and j >= 1)) and state[i + 1][j - 1] == 0) or (
                                (2 <= i <= 13 and 1 <= j <= 12) and state[i - 2][j + 2] == 3 - player and state[i + 1][
                            j - 1] == 0) or (
                                (2 <= i <= 13 and 1 <= j <= 12) and state[i + 1][j - 1] == 3 - player and state[i - 2][
                            j + 2] == 0):
                            player_score = player_score + 10
                        # 未被堵住
                        elif (2 <= i <= 13 and 1 <= j <= 12) and state[i - 2][j + 2] == 0 and state[i + 1][j - 1] == 0:
                            player_score = player_score + 30
                    # 三子连珠
                    elif chain == 3:
                        # 一半被堵住
                        if ((j == 0 or i == 14) and state[i - 3][j + 3] == 0) or (
                                (j == 12 or i == 0) and state[i - 1][j + 1] == 0) or (
                                (3 <= i <= 13 and 1 <= j <= 11) and state[i - 3][j + 3] == 3 - player and state[i + 1][
                            j - 1] == 0) or (
                                (3 <= i <= 13 and 1 <= j <= 11) and state[i + 1][j - 1] == 3 - player and state[i - 3][
                            j + 3] == 0):
                            player_score = player_score + 30
                        # 未被堵住
                        elif (3 <= i <= 13 and 1 <= j <= 11) and state[i - 3][j + 3] == 0 and state[i + 1][j - 1] == 0:
                            player_score = player_score + 60
                    # 四子连珠
                    elif chain == 4:
                        # 一半被堵住
                        if ((j == 0 or i == 14) and state[i - 4][j + 4] == 0) or (
                                (j == 11 or i == 0) and state[i - 1][j - 1] == 0) or (
                                (4 <= i <= 13 and 1 <= j <= 10) and state[i - 4][j + 4] == 3 - player and state[i + 1][
                            j - 1] == 0) or (
                                (4 <= i <= 13 and 1 <= j <= 10) and state[i + 1][j - 1] == 3 - player and state[i - 4][
                            j + 4] == 0):
                            player_score = player_score + 60
                        # 未被堵住
                        elif (4 <= i <= 13 and 1 <= j <= 10) and state[i - 4][j + 4] == 0 and state[i + 1][j - 1] == 0:
                            player_score = 150000
                    # 五子连珠
                    elif chain == 5:
                        player_score = 1000000
                elif state[i][j] != 0:
                    # 检测垂直
                    chain = 1
                    for k in range(1, 5):
                        if i + k < 15 and state[i + k][j] == 3 - player:
                            chain += 1
                        else:
                            break
                    # 二子连珠
                    if chain == 2:
                        # 一半被堵住
                        if (i == 0 and state[i + 2][j] == 0) or (i == 13 and state[i - 1][j] == 0) or (
                                (i >= 1 and i <= 12) and state[i - 1][j] == player and state[i + 2][j] == 0) or (
                                (i >= 1 and i <= 12) and state[i + 2][j] == player and state[i - 1][j] == 0):
                            opponent_score = opponent_score + 10
                        # 未被堵住
                        elif (i >= 1 and i <= 12) and state[i + 2][j] == 0 and state[i - 1][j] == 0:
                            opponent_score = opponent_score + 30
                    # 三子连珠
                    elif chain == 3:
                        # 一半被堵住
                        if (i == 0 and state[i + 3][j] == 0) or (i == 12 and state[i - 1][j] == 0) or (
                                (i >= 1 and i <= 11) and state[i - 1][j] == player and state[i + 3][j] == 0) or (
                                (i >= 1 and i <= 11) and state[i + 3][j] == player and state[i - 1][j] == 0):
                            opponent_score = opponent_score + 30
                        # 未被堵住
                        elif (j >= 1 and j <= 11) and state[i + 3][j] == 0 and state[i - 1][j] == 0:
                            opponent_score = 120000
                    # 四子连珠
                    elif chain == 4:
                        # 一半被堵住
                        if (i == 0 and state[i + 4][j] == 0) or (i == 11 and state[i - 1][j] == 0) or (
                                (j >= 1 and j <= 10) and state[i - 1][j] == player and state[i + 4][j] == 0) or (
                                (j >= 1 and j <= 10) and state[i + 4][j] == player and state[i - 1][j] == 0):
                            opponent_score = 800000
                        # 未被堵住
                        elif (j >= 1 and j <= 10) and state[i + 4][j] == 0 and state[i - 1][j] == 0:
                            opponent_score = 800000
                    # 五子连珠
                    elif chain == 5:
                        opponent_score = 1000000
                    # 检测水平
                    chain = 1
                    for k in range(1, 5):
                        if j + k < 15 and state[i][j + k] == 3 - player:
                            chain += 1
                        else:
                            break
                    # 二子连珠
                    if chain == 2:
                        # 一半被堵住
                        if (j == 0 and state[i][j + 2] == 0) or (j == 13 and state[i][j - 1] == 0) or (
                                (j >= 1 and j <= 12) and state[i][j - 1] == player and state[i][j + 2] == 0) or (
                                (j >= 1 and j <= 12) and state[i][j + 2] == player and state[i][j - 1] == 0):
                            opponent_score = opponent_score + 10
                        # 未被堵住
                        elif (j >= 1 and j <= 12) and state[i][j + 2] == 0 and state[i][j - 1] == 0:
                            opponent_score = opponent_score + 30
                    # 三子连珠
                    elif chain == 3:
                        # 一半被堵住
                        if (j == 0 and state[i][j + 3] == 0) or (j == 12 and state[i][j - 1] == 0) or (
                                (j >= 1 and j <= 11) and state[i][j - 1] == player and state[i][j + 3] == 0) or (
                                (j >= 1 and j <= 11) and state[i][j + 3] == player and state[i][j - 1] == 0):
                            opponent_score = opponent_score + 30
                        # 未被堵住
                        elif (j >= 1 and j <= 11) and state[i][j + 3] == 0 and state[i][j - 1] == 0:
                            opponent_score = opponent_score + 120000
                    # 四子连珠
                    elif chain == 4:
                        # 一半被堵住
                        if (j == 0 and state[i][j + 4] == 0) or (i == 11 and state[i][j - 1] == 0) or (
                                (j >= 1 and j <= 10) and state[i][j - 1] == player and state[i][j + 4] == 0) or (
                                (j >= 1 and j <= 10) and state[i][j + 4] == player and state[i][j - 1] == 0):
                            opponent_score = 800000
                        # 未被堵住
                        elif (j >= 1 and j <= 10) and state[i][j + 4] == 0 and state[i][j - 1] == 0:
                            opponent_score = 800000
                    # 五子连珠
                    elif chain == 5:
                        opponent_score = 1000000

                    # 左上到右下
                    chain = 1
                    for k in range(1, 5):
                        if i + k < 15 and j + k < 15 and state[i + k][j + k] == 3 - player:
                            chain += 1
                        else:
                            break
                    # 二子连珠
                    if chain == 2:
                        # 一半被堵住
                        if (((j == 0 and i <= 12) or (i == 0 and j <= 12)) and state[i + 2][j + 2] == 0) or (
                                ((j == 13 and i >= 1) or (i == 13 and j >= 1)) and state[i - 1][j - 1] == 0) or (
                                (1 <= i <= 12 and 1 <= j <= 12) and state[i - 1][j - 1] == player and state[i + 2][
                            j + 2] == 0) or (
                                (1 <= i <= 12 and 1 <= j <= 12) and state[i + 2][j + 2] == player and state[i - 1][
                            j - 1] == 0):
                            opponent_score = opponent_score + 10
                        # 未被堵住
                        elif (1 <= i <= 12 and 1 <= j <= 12) and state[i + 2][j + 2] == 0 and state[i - 1][j - 1] == 0:
                            opponent_score = opponent_score + 30
                    # 三子连珠
                    elif chain == 3:
                        # 一半被堵住
                        if ((j == 0 or i == 0) and state[i + 3][j + 3] == 0) or (
                                (j == 12 or i == 12) and state[i - 1][j - 1] == 0) or (
                                (1 <= i <= 11 and 1 <= j <= 11) and state[i - 1][j - 1] == player and state[i + 3][
                            j + 3] == 0) or (
                                (1 <= i <= 11 and 1 <= j <= 11) and state[i + 3][j + 3] == player and state[i - 1][
                            j - 1] == 0):
                            opponent_score = opponent_score + 30
                        # 未被堵住
                        elif (1 <= i <= 11 and 1 <= j <= 11) and state[i + 3][j + 3] == 0 and state[i - 1][j - 1] == 0:
                            opponent_score = 120000
                    # 四子连珠
                    elif chain == 4:
                        # 一半被堵住
                        if ((j == 0 or i == 0) and state[i + 4][j + 4] == 0) or (
                                (j == 11 or i == 11) and state[i - 1][j - 1] == 0) or (
                                (1 <= i <= 10 and 1 <= j <= 10) and state[i - 1][j - 1] == player and state[i + 4][
                            j + 4] == 0) or (
                                (1 <= i <= 10 and 1 <= j <= 10) and state[i + 4][j + 4] == player and state[i - 1][
                            j - 1] == 0):
                            opponent_score = 800000
                        # 未被堵住
                        elif (1 <= i <= 10 and 1 <= j <= 10) and state[i + 4][j + 4] == 0 and state[i - 1][j - 1] == 0:
                            opponent_score = 800000
                    # 五子连珠
                    elif chain == 5:
                        opponent_score = 1000000

                    # 左下到右上
                    chain = 1
                    for k in range(1, 5):
                        if i - k >= 0 and j + k < 15 and state[i - k][j + k] == 3 - player:
                            chain += 1
                        else:
                            break
                    # 二子连珠
                    if chain == 2:
                        # 一半被堵住
                        if (((j == 0 and i >= 2) or (i == 14 and j <= 13)) and state[i - 2][j + 2] == 0) or (
                                ((j == 13 and i <= 13) or (i == 1 and j >= 1)) and state[i - 1][j + 1] == 0) or (
                                (2 <= i <= 13 and 1 <= j <= 12) and state[i - 2][j + 2] == player and state[i + 1][
                            j - 1] == 0) or (
                                (2 <= i <= 13 and 1 <= j <= 12) and state[i + 1][j - 1] == player and state[i - 2][
                            j + 2] == 0):
                            opponent_score = opponent_score + 10
                        # 未被堵住
                        elif (2 <= i <= 13 and 1 <= j <= 12) and state[i - 2][j + 2] == 0 and state[i + 1][j - 1] == 0:
                            opponent_score = opponent_score + 30
                    # 三子连珠
                    elif chain == 3:
                        # 一半被堵住
                        if ((j == 0 or i == 14) and state[i - 3][j + 3] == 0) or (
                                (j == 12 or i == 0) and state[i - 1][j + 1] == 0) or (
                                (3 <= i <= 13 and 1 <= j <= 11) and state[i - 3][j + 3] == player and state[i + 1][
                            j - 1] == 0) or (
                                (3 <= i <= 13 and 1 <= j <= 11) and state[i + 1][j - 1] == player and state[i - 3][
                            j + 3] == 0):
                            opponent_score = opponent_score + 30
                        # 未被堵住
                        elif (3 <= i <= 13 and 1 <= j <= 11) and state[i - 3][j + 3] == 0 and state[i + 1][j - 1] == 0:
                            opponent_score = 120000
                    # 四子连珠
                    elif chain == 4:
                        # 一半被堵住
                        if ((j == 0 or i == 14) and state[i - 4][j + 4] == 0) or (
                                (j == 11 or i == 0) and state[i - 1][j - 1] == 0) or (
                                (4 <= i <= 13 and 1 <= j <= 10) and state[i - 4][j + 4] == player and state[i + 1][
                            j - 1] == 0) or (
                                (4 <= i <= 13 and 1 <= j <= 10) and state[i + 1][j - 1] == player and state[i - 4][
                            j + 4] == 0):
                            opponent_score = 800000
                        # 未被堵住
                        elif (4 <= i <= 13 and 1 <= j <= 10) and state[i - 4][j + 4] == 0 and state[i + 1][j - 1] == 0:
                            opponent_score = 800000
                    # 五子连珠
                    elif chain == 5:
                        opponent_score = 1000000
        return (240 - (player_score - opponent_score)) / 240 * 10

    # 检测player是否赢了
    def is_goal(self, state, player):
        for i in range(15):
            for j in range(15):
                if state[i][j] == player:
                    # Check horizontally
                    if j + 4 < 15 and state[i][j + 1] == player and state[i][j + 2] == player and state[i][
                        j + 3] == player and state[i][j + 4] == player:
                        return True
                    # Check vertically
                    if i + 4 < 15 and state[i + 1][j] == player and state[i + 2][j] == player and state[i + 3][
                        j] == player and state[i + 4][j] == player:
                        return True
                    # Check diagonally (top-left to bottom-right)
                    if i + 4 < 15 and j + 4 < 15 and state[i + 1][j + 1] == player and state[i + 2][j + 2] == player and \
                            state[i + 3][j + 3] == player and state[i + 4][j + 4] == player:
                        return True
                    # Check diagonally (bottom-left to top-right)
                    if i - 4 >= 0 and j + 4 < 15 and state[i - 1][j + 1] == player and state[i - 2][j + 2] == player and \
                            state[i - 3][j + 3] == player and state[i - 4][j + 4] == player:
                        return True
        return False

    def next_move(self, depth):
        state = self.chessboard
        # initial为初始状态
        initial = state
        # 下一个是白色
        player = 2
        # 求出下一步
        result = self.a_star(depth)

        # 得到下一步坐标
        row = -1
        col = -1
        # 找出不一样的点
        for i in range(15):
            for j in range(15):
                if initial[i][j] != result[i][j] and result[i][j] == 2:
                    row = i
                    col = j
                    break
            if row != -1:
                break
        # Return the next move as a tuple of (row, col)
        return [row, col]

    # 该棋子周围有没有其他棋子
    def ifSurrond(self, states, row, col):
        where = [(-1, 1), (0, 1), (1, 1), (-1, 0), (1, 0), (-1, -1), (0, -1), (1, -1)]
        for i in where:
            if row + i[0] >= 0 and col + i[1] >= 0 and row + i[0] < 15 and col + i[1] < 15:
                if states[row + i[0]][col + i[1]] != 0:
                    return True
        return False

    # 生成子节点
    def get_successors(self, state):
        successors = []
        # 遍历，将白子下到对应位置
        for i in range(15):
            for j in range(15):
                if state[i][j] == 0 and self.ifSurrond(state, i, j):
                    new_state = copy.deepcopy(state)
                    # 白子下到该位置
                    new_state[i][j] = 2
                    # 遍历，寻找这个时候黑子下的位置
                    temp = self.getBestBlack(new_state)
                    # 如果黑子赢了，取消白子的这种下子方式
                    # if self.is_goal(temp, 1):
                    # self.close_list[self.three2one(temp)] = 10000
                    # continue
                    # else:
                    successors.append(self.three2one(temp))
        return successors

    def getBestBlack(self, state):
        # 记录黑子下的最佳位置
        temp = [state, 0]
        for i in range(15):
            for j in range(15):
                if state[i][j] == 0 and self.ifSurrond(state, i, j):
                    new_state = copy.deepcopy(state)
                    # 黑子下到该位置
                    new_state[i][j] = 1
                    x = self.heuristic(new_state, 1)
                    if temp[1] > x:
                        temp[0] = new_state
                        temp[1] = x
        return temp[0]

    # 计算player方的最长分
    def score(self, state, player):
        # 双方玩家最长的链
        max_chain_player = 0
        for i in range(15):
            for j in range(15):
                # 遍历到该种子
                if state[i][j] == player:
                    # 检测水平，初始chain=1
                    chain = 1
                    for k in range(1, 5):
                        if j + k < 15 and state[i][j + k] == player:
                            chain += 1
                        else:
                            break
                    max_chain_player = max(max_chain_player, chain)

                    # 检测垂直
                    chain = 1
                    for k in range(1, 5):
                        if i + k < 15 and state[i + k][j] == player:
                            chain += 1
                        else:
                            break
                    max_chain_player = max(max_chain_player, chain)

                    # 左上到右下
                    chain = 1
                    for k in range(1, 5):
                        if i + k < 15 and j + k < 15 and state[i + k][j + k] == player:
                            chain += 1
                        else:
                            break
                    max_chain_player = max(max_chain_player, chain)

                    # 左下到右上
                    chain = 1
                    for k in range(1, 5):
                        if i - k >= 0 and j + k < 15 and state[i - k][j + k] == player:
                            chain += 1
                        else:
                            break
                    max_chain_player = max(max_chain_player, chain)
        return max_chain_player

    def getSource(self, start, source):
        # 指向当前
        temp = start
        # 指向temp的父节点
        temp1 = start
        while (True):
            temp1 = self.dict_link[temp]
            if temp1 == source:
                return self.one2three(temp)
            temp = temp1
