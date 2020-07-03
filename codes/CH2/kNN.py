#-*- coding: utf-8 -*-
import numpy

# 2.1.1 准备：使用Python导入数据
# 创建测试数据集
def createDataSet():
    # 二维数据集 就是每个数据的坐标点
    group = numpy.array([[1.0, 1.1], [1.0, 1.0], [0, 0], [0, 0.1]])
    # 数据标签（分类用的）
    labels = ['A', 'B', 'C', 'D']
    return group, labels

# 2.1.2 实施kNN分类算法
# inX：用于分类的 输入向量
# dataSet：训练样本集
# labels：
# k：最近邻居的数目
def classify0(inX, dataSet, labels, k):
    # 1. 计算已知类别中的点到当前未知类别点的欧氏距离
    dataSetSize = dataSet.shape[0]                          # 获取测试集的行数
    deffMat = tile(inX, (dataSetSize, 1)) - dataSet         # inX矩阵在横向重复dateSetSize次，列方向不动（就一次）
                                                            # 减dataSet是求欧氏距离的步骤之一，然后是平方，再然后是开方
    sqdeffMat = deffMat ** 2                                # 平方
    sqDistances = sqdeffMat ** 0.5                          # 开方，乘以1/2次方等于开根号

    # 2. 排序（距离升序）
    sortedDistIndecies = sqDistances.argsort()              # 排序，由小到大

    # 3. 选择距离最小的k个点
    for i in range(k):
        # 取出前k个元素的类别
        voteIlabel = sortedDistIndecies[i]


