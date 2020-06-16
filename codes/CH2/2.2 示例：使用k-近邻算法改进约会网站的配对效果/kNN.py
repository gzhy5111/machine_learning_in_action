#-*- coding: utf-8 -*-
# 2.2 示例：使用k-近邻算法改进约会网站的配对效果
import numpy
import operator
# 2.2.2 分析数据：使用Matplotilb创建散点图
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import matplotlib.lines as mlines

# 2.2.1 准备数据：从文本中解析数据 得到矩阵的形式
# datingTestSet.txt 是海伦约会的数据
def file2matrix(filename):
    # 打开文件
    fr = open(filename)
    # readlines()方法读取整个文件所有行，保存在一个列表arrayOLines中
    arrayOLines = fr.readlines()
    # 得到文件行数 1000行
    numberOfLines = len(arrayOLines)
    # print(numberOfLines)

    # numpy.zeros()可以创建0矩阵
    returnMat = numpy.zeros((numberOfLines, 3))

    # 解析txt文件，存入矩阵 returnMat 和标签 classLabelVector 列表中
    classLabelVector = []
    index = 0
    for line in arrayOLines:
        # 移除字符串头尾的字符（默认为空格或换行符），注意：中间的空格什么的不会删除
        line = line.strip()
        # 以制表符分割
        # 重要！这里是一行一行解析的，我们对每一行进行分析都需要用到lineFromLine变量
        lineFromLine = line.split('\t')
        # 放入到矩阵returnMat中
        returnMat[index:] = lineFromLine[0:3]

        # 根据datingTestSet.txt最后一列的字符串，对其转换为数字标签形式
        if (lineFromLine[-1] == "largeDoses"):
            classLabelVector.append(3)
        elif (lineFromLine[-1] == "smallDoses"):
            classLabelVector.append(2)
        elif (lineFromLine[-1] == "didntLike"):
            classLabelVector.append(1)
        index = index + 1
    return returnMat, classLabelVector

# 2.2.2 分析数据：使用Matplotlib创建散点图
# datingDataMat - 样本集矩阵
# datingLabels - 标签
# errorDatingDataMat - 错误点矩阵
def show(datingDataMat, datingLabels, errorDatingDataMat):
    # 将fig画布分隔成2行2列,不共享x轴和y轴,fig画布的大小为(14,8)
    # 当nrow=2,nclos=2时,代表fig画布被分为四个区域,axs[0][0]表示第一行第一个区域
    fig, axs = plt.subplots(nrows=2, ncols=2, sharex=False, sharey=False, figsize=(14, 8))
    # 调整子图间距
    plt.subplots_adjust(wspace=0.2, hspace=0.3)
    # 设置文字格式 需要 from matplotlib.font_manager import FontProperties
    font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=12)

    # 第一张图：
    # 生成画布
    # fig = plt.figure()
    # # 添加坐标和刻度尺
    # ax = fig.add_subplot(111)
    # X[:, 0]是numpy中数组的一种写法，表示对一个二维数组，取该二维数组第一维中的所有数据，第二维中取第0个数据，直观来说，X[:, 0]就是取所有行的第1个数据。
    axs[0][0].scatter(datingDataMat[:, 1], datingDataMat[:, 2], s=15, alpha=.5)
    # 设置标题,x轴label,y轴label
    axs0_title_text = axs[0][0].set_title(u'没有样本类别的约会数据散点图', FontProperties=font)
    axs0_xlabel_text = axs[0][0].set_xlabel(u'玩视频游戏所消耗时间占比', FontProperties=font)
    axs0_ylabel_text = axs[0][0].set_ylabel(u'每周消费的冰淇淋公升数', FontProperties=font)
    plt.setp(axs0_title_text, size=12, weight='bold', color='red')
    plt.setp(axs0_xlabel_text, size=10, weight='bold', color='black')
    plt.setp(axs0_ylabel_text, size=10, weight='bold', color='black')

    # 第二张图
    # 画出散点图,以datingDataMat矩阵的第二(玩游戏)、第三列(冰激凌)数据画散点数据,散点大小为15,透明度为0.5
    labelsColors = []
    for i in datingLabels:
        if i == 1:
            labelsColors.append('red')
        elif i == 2:
            labelsColors.append('green')
        elif i == 3:
            labelsColors.append('blue')

    axs[0][1].scatter(x=datingDataMat[:, 1], y=datingDataMat[:, 2], color=labelsColors, s=15, alpha=.5)
    # 设置标题,x轴label,y轴label
    axs1_title_text = axs[0][1].set_title(u'含有样本类别的约会数据散点图', FontProperties=font)
    axs1_xlabel_text = axs[0][1].set_xlabel(u'玩视频游戏所消耗时间占比', FontProperties=font)
    axs1_ylabel_text = axs[0][1].set_ylabel(u'每周消费的冰激淋公升数', FontProperties=font)
    plt.setp(axs1_title_text, size=12, weight='bold', color='red')
    plt.setp(axs1_xlabel_text, size=10, weight='bold', color='black')
    plt.setp(axs1_ylabel_text, size=10, weight='bold', color='black')

    # 第三张图：
    # 彩色绘图 x轴是玩视频游戏所占时间比；y轴是每年获取的飞行常客里程数
    # 颜色标注 分为三个类别
    # 类别区分
    labelsColors = []
    for i in datingLabels:
        if (i == 1):                # didntLike
            labelsColors.append('red')
        elif (i == 2):              # smallDoses
            labelsColors.append('green')
        elif (i == 3):              # largeDoses
            labelsColors.append('blue')
    axs[1][0].scatter(x=datingDataMat[:, 0], y=datingDataMat[:, 1], color=labelsColors, s=15, alpha=.5)
    # 设置标题,x轴label,y轴label
    axs2_title_text = axs[1][0].set_title(u'每年获得的飞行常客里程数与玩视频游戏所消耗时间占比', FontProperties=font)
    axs2_xlabel_text = axs[1][0].set_xlabel(u'每年获得的飞行常客里程数', FontProperties=font)
    axs2_ylabel_text = axs[1][0].set_ylabel(u'玩视频游戏所消耗时间占比', FontProperties=font)
    plt.setp(axs2_title_text, size=12, weight='bold', color='red')
    plt.setp(axs2_xlabel_text, size=10, weight='bold', color='black')
    plt.setp(axs2_ylabel_text, size=10, weight='bold', color='black')

    # 第四张图：标记错误点
    # 颜色标注 分为三个类别
    # 类别区分
    labelsColors = []
    for i in datingLabels:
        if (i == 1):  # didntLike
            labelsColors.append('red')
        elif (i == 2):  # smallDoses
            labelsColors.append('green')
        elif (i == 3):  # largeDoses
            labelsColors.append('blue')
    axs[1][1].scatter(x=datingDataMat[:, 0], y=datingDataMat[:, 1], color=labelsColors, s=15, alpha=.5)
    # 显示分类错误的点 黑色标注
    axs[1][1].scatter(x=errorDatingDataMat[:, 0], y=errorDatingDataMat[:, 1], color='black', s=15, alpha=.5)
    # 设置标题,x轴label,y轴label
    axs3_title_text = axs[1][1].set_title(u'每年获得的飞行常客里程数与玩视频游戏所消耗时间占比', FontProperties=font)
    axs3_xlabel_text = axs[1][1].set_xlabel(u'每年获得的飞行常客里程数', FontProperties=font)
    axs3_ylabel_text = axs[1][1].set_ylabel(u'玩视频游戏所消耗时间占比', FontProperties=font)
    plt.setp(axs3_title_text, size=12, weight='bold', color='red')
    plt.setp(axs3_xlabel_text, size=10, weight='bold', color='black')
    plt.setp(axs3_ylabel_text, size=10, weight='bold', color='black')

    # 设置图例
    didntLike = mlines.Line2D([], [], color='red', marker='.', markersize=6, label='讨厌')
    smallDoses = mlines.Line2D([], [], color='green', marker='.', markersize=6, label='有点喜欢')
    largeDoses = mlines.Line2D([], [], color='blue', marker='.', markersize=6, label='非常喜欢')
    error = mlines.Line2D([], [], color='black', marker='.', markersize=6, label='错误数据')

    # 添加图例
    axs[0][1].legend(handles=[didntLike, smallDoses, largeDoses], prop=font)
    axs[1][0].legend(handles=[didntLike, smallDoses, largeDoses], prop=font)
    axs[1][1].legend(handles=[didntLike, smallDoses, largeDoses, error], prop=font)
    plt.show()

# 2.2.3 准备数据：归一化数值
# 因为飞机里程数数值本身相较于其他参数属于大数，但与其他参数重要性同级别。
# dataSet矩阵：1000行3列
def autoNorm(dataSet):
    # min函数从每列中都选取一个最小值
    # minVals、maxVals：一行3列
    minVals = dataSet.min(0)
    maxVals = dataSet.max(0)
    # 最大值与最小值之差 矩阵形式（一行三列）
    rangs = maxVals - minVals
    # 创建新矩阵（这个矩阵也是函数要返回的） 矩阵（1000行3列）
    normDataSet = numpy.zeros(numpy.shape(dataSet))
    # 获取dataSet行数
    lines = dataSet.shape[0]

    # 归一化计算
    normDataSet = dataSet - numpy.tile(minVals, (lines, 1))
    # 除以最大和最小值的差,得到归一化数据
    normDataSet = normDataSet / numpy.tile(rangs, (lines, 1))
    return normDataSet, rangs, minVals

def datingClassTest():
    # 2.2.1 准备数据：从文本中解析数据 得到矩阵的形式
    datingDataMat, datingLabels = file2matrix('datingTestSet.txt')

    # print(datingDataMat)

    # 测试数据集百分比
    hoRatio = 0.1

    # 将所有数据（1000行3列）做归一化
    # 2.2.3 准备数据：归一化数值
    # normMat：1000行3列 归一化后的矩阵
    normMat, ranges, minVals = autoNorm(datingDataMat)
    lines = normMat.shape[0]

    # 测试数据集行数
    numTestVecs = int(lines * hoRatio)

    # 分类结果打印
    # kNN分类
    # 2.1.1是只有一个测试数据，现在我们有10%的测试数据需要被测试

    # 构造errorDatingDataMat矩阵
    errorDatingDataMat = numpy.empty(shape=[0, 3])

    count = 0.0
    for i in range(numTestVecs):
        # normMat[i, :] - 第i行元素
        test_class = classify0(normMat[i, :], normMat[numTestVecs:lines, :], datingLabels[numTestVecs:lines], 4)
        # largeDoses：分类结果3
        # smallDoses：2
        # didntLike：1
        print("分类结果：%s\t真实结果：%s" % (test_class, datingLabels[i]))
        if test_class != datingLabels[i]:
            count = count + 1.0
            errorDatingDataMat = numpy.append(errorDatingDataMat, [normMat[i, :]], axis=0)

    errorRate = float(count / numTestVecs) * 100
    print("错误结果个数：%d\t错误率：%d %%" % (count, errorRate))

    # 2.2.2 分析数据：使用Matplotlib创建散点图
    show(datingDataMat, datingLabels, errorDatingDataMat)

# kNN分类处理函数
# inX - 用于分类的数据(测试集)
# dataSet - 用于训练的数据(训练集)
# labes - 分类标签
# k - 选择距离最小的k个点
def classify0(inX, dataSet, labels, k):
    # 1. 求距离
    dataSetSize = dataSet.shape[0]
    diffMat = numpy.tile(inX, (dataSetSize, 1)) - dataSet
    sqDiffMat = diffMat ** 2
    sqDistances = sqDiffMat.sum(axis=1)
    Distances = sqDistances ** 0.5

    # 2. 排序
    sortedDistIndecies = Distances.argsort()
    # print(sortedDistIndecies)
    # 3. 选择距离最小的k个点
    classCount = {}
    for i in range(k):
        voteIlabel = labels[sortedDistIndecies[i]]
        # 统计标签出现的次数
        classCount[voteIlabel] = classCount.get(voteIlabel, 0) + 1
    sortClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)
    return sortClassCount[0][0]

# 输入数据做预测
def classifyPerson():
    datingDataMat, datingLabels = file2matrix('datingTestSet.txt')
    normMat, ranges, minVals = autoNorm(datingDataMat)
    air = float(input("请输入每年获得的飞行常客里程数："))
    playGameTime = float(input("玩视频游戏所耗时间百分比："))
    iceCream = float(input("每周消费的冰激淋公升数："))
    inArr = numpy.array([air, playGameTime, iceCream])
    normInArr = (inArr - minVals)/ranges
    classifierResult = classify0(normInArr, normMat, datingLabels, 3)
    # largeDoses：分类结果3
    # smallDoses：2
    # didntLike：1
    resultList = ["讨厌", "有点喜欢", "非常喜欢"]
    print("你 %s 这个人" % (resultList[classifierResult-1]))

if __name__ == '__main__':
    # 从数据集中抽取前 hoRatio % 做测试集
    # datingClassTest()
    classifyPerson()