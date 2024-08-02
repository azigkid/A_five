# 基于A*算法的五子棋AI设计

界面使用pyqt5，参考pyqt5（参考[sgsx11](https://github.com/sgsx11/Gobang)项目：Python+PyQt5实现五子棋游戏（人机博弈+深搜+α-β剪枝））

通过对棋盘状态进行分析获取状态分数，通过A*算法求得最佳方式

#### 使用

运行start.py，玩家固定执黑先手

AI落子后，控制台显示AI思考层数

分出胜负后再次单击即可重新开始

#### 注意

设计规则时未考虑禁手

计分方式粗糙。设计仓促，AI难免有不足之处，敬请谅解
