# trees.py功能：
# 计算给定数据集的信息熵
# 创建数据集
# 划分数据集
# 将每种划分方式得到的数据集都计算一次信息增益，最后选择信息增益最大的划分方式。——即最好的划分方式

# 因为刚学，我需要理清思路，所以讲后续的决策树函数另起一个新文件，这样更清晰一些。
# 上面的trees.py，我们已经选择出来了最好的数据集划分方式。下面我们要构造决策树。
import operator

from trees import *
def createTree(dataSet, labels, featLabels):
    classList = [example[-1] for example in dataSet]    # 取dataSet每行中的yes或no标签。
    # 递归结束条件之一：所有的标签都相同，已经不需要更多的指标就可以确定结果。则返回该标签
    # Python count() 方法用于统计字符串里某个字符出现的次数。
    if classList.count(classList[0]) == len(classList):
        return classList[0]
    # 递归结束条件二：用完了所有的标签，还无法做出结果。则返回出现次数最多的标签
    if len(classList) == 0:
        return majorityCnt(classList)
    bestFeat = chooseBestFeatureToSplit(dataSet)        # 选择数据集中的最优特征
    bestFeatLabel = labels[bestFeat]                    # 最优特征对应的标签名字
    # 需要存起来，后面还要绘图
    featLabels.append(bestFeatLabel)
    myTree = {bestFeatLabel: {}}
    del(labels[bestFeat])
    featValues = [example[bestFeat] for example in dataSet] # 把选出来的那一列中所有的属性值取出
    uniqueVals = set(featValues)                        # set() 函数创建一个无序不重复元素集，用于去掉重复的属性值
    for value in uniqueVals:
        # 原来的数据集会变成两个数据集
        subLabels = labels[:]
        myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet, bestFeat, value), subLabels, featLabels)

    return myTree

"""
功能：计算
"""
def majorityCnt(classList):
    # 用名为classCount的字典存储出现的概率，即统计yes和no的个数
    classCount = {}
    for vote in classList:
        if vote not in classCount.keys():    # .keys()方法用于返回一个字典所有的键。
            classCount[vote] = 0
        else:
            classCount[vote] += 1
    # 排序，看yes和no谁个数多，返回谁
    sortClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)
    return sortClassCount[0][0]