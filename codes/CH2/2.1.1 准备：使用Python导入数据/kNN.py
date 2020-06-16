#-*- coding: utf-8 -*-
# 2.1.1 准备：使用Python导入数据
import numpy
import operator

# 创建测试数据集
def createDataSet():
    # 二维数据集 就是每个数据的坐标点
    group = numpy.array([[1.0, 1.1], [1.0, 1.0], [0, 0], [0, 0.1]])
    # 数据标签（分类用的）
    labels = ['A', 'A', 'B', 'B']
    return group, labels

# 2.1.2 实施kNN分类算法
# inX：用于分类的 输入向量
# dataSet：训练样本集
# labels：
# k：最近邻居的数目
def classify0(inX, dataSet, labels, k):
    # 1. 计算已知类别中的点到当前未知类别点的欧氏距离
    # 获取训练集的行数
    dataSetSize = dataSet.shape[0]
    # inX矩阵在横向重复dateSetSize次，列方向不动（就一次）
    diffMat = numpy.tile(inX, (dataSetSize, 1)) - dataSet
    # 减dataSet是求欧氏距离的步骤之一，然后是平方，再然后是开方
    # 平方
    sqdiffMat = diffMat ** 2
    # 第一列与第二列数值相加合并到第一列
    sqDistances = sqdiffMat.sum(axis=1)
    # 开方，乘以1/2次方等于开根号
    sqDistances = sqDistances ** 0.5

    # 2. 排序（距离升序）
    # 排序，由小到大
    sortedDistIndecies = sqDistances.argsort()

    # 3. 选择距离最小的k个点
    # 记录标签出现次数的字典
    classCount = {}
    for i in range(k):
        # 取出前k个元素的类别
        voteIlabel = labels[sortedDistIndecies[i]]
        # 根据标签查出现次数 然后放在字典中
        classCount[voteIlabel] = classCount.get(voteIlabel, 0) + 1

    # 4. 根据出现的次数 对字典进行排序
    # operator模块提供的itemgetter函数用于获取对象的哪些维的数据（这里是第1维（0维开始）），reverse=True是降序排序
    sortClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)
    return sortClassCount[0][0]
if __name__ == '__main__':
    # 创建数据集
    group, labels = createDataSet()
    # 测试集
    test = [0, 0]
    # kNN分类
    test_class = classify0(test, group, labels, 3)
    # 打印分类结果
    print(test_class)
