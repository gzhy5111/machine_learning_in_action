# 首先，我们刚开始写这个文件都是边看书边写的，书上程序清单3-1告诉我要先写“计算给定数据集的信息熵”这个函数，也告诉你了需要传进去什么参数，得到什么。我们就一边理解一边完成即可。不要像以前那样从main函数开始写起。因为是刚学，我们不会有很清晰的思路，刚开始我们要做的就是模仿。

from math import log

"""
功能：计算给定数据集的信息熵
参数：数据集合dataSet，是一个矩阵，跟以前的kNN中的测试集、训练集一样都是矩阵形式的参数。
返回：一个数值，表示这个数据集整体的信息熵。
"""
def calculateShannonEntropy(dataSet):
    # 到这，我们是不是要想下。dataSet矩阵怎么去测试？不然我怎么知道这个函数我写完了它对不对呢？看了眼书本，他用的是creatDataSet函数，内部创建dateSet矩阵的。
    # 所以，我们也顺便准备好createDateSet函数。
    count = len(dataSet)                # 数据集dataSet的行数
    # print(count)
    # 接下来，我们要做的事情是统计整个数据集中yes和no的行数。有多少数据是yes，多少是no。——为了后面计算熵
    labelCounts = {}                    # 用字典存储yes和no的个数
    for i in dataSet:
        # print(i)                        # 获取数据集中第一行数据
        # print(i[-1])                    # 获取最后一列的值
        currentLabel = i[-1]
        # 字典中没有这个键，就增加并初始化值为0
        if currentLabel not in labelCounts.keys():
            # 初始化，值为0
            labelCounts[currentLabel] = 0
        # 初始化后，字典中就有这个键了，下面修改字典的值
        labelCounts[currentLabel] += 1
    # print(labelCounts)

    # 开始使用信息熵公式计算熵
    shannonEntropy = 0.0
    for i in labelCounts.keys():
        factor = labelCounts[i] / count
        shannonEntropy += - factor * log(factor, 2)       # 信息熵计算
    return shannonEntropy

"""
功能：手工创建的数据集，用于验证 calculateShannonEntropy() 函数的正确性
"""
def createDataSet():
    # 手工写了个数据集，将来传给calculateShannonEntropy()函数。
    dataSet = [
        # 标签1, 标签2, 决策结果（yes or no）
        [1, 1, "yes"],
        [1, 1, "yes"],
        [1, 0, "no"],
        [0, 1, "no"],
        [0, 1, "no"]
    ]
    # 有数据集，就有标签。针对这个数据集，dateSet前两列表示两个标签：没有浮出水面 和 是否有脚蹼
    labels = ["没有浮出水面", "脚蹼"]
    # print(dataSet, labels)
    return dataSet, labels

"""
功能：划分数据集。选择第axis列的数值为value的行（我怎么感觉这种操作有点像数据库， select 第axis列字段名 where 第axis列值 == value）
参数：
        dataSet：数据集
        axis：标志位：表示去掉第axis列数据
        value：
返回：处理后的矩阵returnDataSet
"""
def splitDataSet(dataSet, axis, value):
    # 选择第axis列等于value的行
    returnDataSet = []
    for i in dataSet:
        # 先做选择
        if i[axis] == value:
            temp = i[:axis]
            temp.extend(i[axis+1:])
            # 处理好了放到returnDataSet中
            returnDataSet.append(temp)
    # print(returnDataSet)
    return returnDataSet

"""
功能：将每种划分方式得到的数据集都计算一次信息增益，最后选择信息增益最大的划分方式。——即最好的划分方式
参数：数据集矩阵
输出：最好的划分方式数据集矩阵的特征下标（也就是第几列）
"""
def chooseBestFeatureToSplit(dataSet):
    # 信息增益 = 集合熵 - 条件熵
    # 我们要计算每个特征的信息增益
    count = len(dataSet[0]) - 1                                                         # dataSet - 1 代表特征数量
    entropy = calculateShannonEntropy(dataSet)                                          # 集合熵 entropy
    MaxInfoGain = 0.0

    # 遍历所有特征
    for i in range(count):
        # 找到一个特征中的所有可能取值
        featList = [example[i] for example in dataSet]                                  # 不理解的话看这个文章：https://blog.csdn.net/jiangsujiangjiang/article/details/84313227
        # print(featList)
        uniqueVals = set(featList)
        # print(uniqueVals)
        newEntropy = 0.0
        for j in uniqueVals:
            currentDataSet = splitDataSet(dataSet, i, j)
            # 条件熵 newEntropy。当然，需要用for循环来计算每个当前数据集的条件熵。
            # 计算系数
            factor = len(currentDataSet)/len(dataSet)
            # print(factor)
            newEntropy += factor * calculateShannonEntropy(currentDataSet)              # 条件熵
            # print(newEntropy)

        # 接下来计算 选择每个特征后的 信息增益
        infoGain = entropy - newEntropy 					                            #信息增益
        # print(infoGain)
        # 选择最大的信息增益，放到MaxInfoGain
        if infoGain > MaxInfoGain:
            MaxInfoGain = infoGain
            flag = i

    return flag

if __name__ == "__main__":
    # 下面都是临时测试函数正确性用的
    dataSet, labels = createDataSet()
    # print("数据集的香农熵为：" , calculateShannonEntropy(dataSet))

    # print(splitDataSet(dataSet, 0, 0))
    # print(splitDataSet(dataSet, 0, 1))
    # print(splitDataSet(dataSet, 1, 0))
    chooseBestFeatureToSplit(dataSet)