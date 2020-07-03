import operator

import numpy
# 导入了一个模块中的一个函数
# 导入os模块中的listdir函数
from os import listdir


def img2vector(filename):
    fr = open(filename)
    returnMat = numpy.zeros((1, 1024))      # 32 * 32d的矩阵，折合成一行，1024列。

    # 开始录入进矩阵
    for i in range(32):
        # 每一行都存在lineStr中
        lineStr = fr.readline()             # 读一行，而不是全部文件，读全部文件是readlines()方法
        for j in range(32):
            returnMat[0, i * 32 + j] = int(lineStr[j])
    return returnMat

# 训练数据（大数据）
def ClassTraining():
    trainingFileList = listdir('trainingDigits')            # 获取testDigits文件夹下的所有文件名
    trainingMat = numpy.zeros((len(trainingFileList), 1024))

    # 创建标签
    label = []

    # 对每个文件进行操作，需要遍历
    for i in range(len(trainingFileList)):
        # 从文件名（带扩展名）中解析出文件名
        fileName = trainingFileList[i].split('.')[0]    #eg：8_72
        number = fileName.split('_')[0]
        label.append(number)
        # trainingMat[i,:]：取第一行元素
        # 但img2vector的返回值是 1x1024 的数据。所以就是直接转存
        trainingMat[i,:] = img2vector('trainingDigits/%s' % (trainingFileList[i]))

    return trainingMat, label

# 测试数据（新数据）
def Classtest():
    # 获取训练集的大数据矩阵
    trainingMat, label = ClassTraining()            # trainningMat：(1934, 1024)；len(lable)：1934

    # 获取文件夹中的文件名，这是py自带的方法
    testFileList = listdir('testDigits')
    testMat = numpy.zeros((len(testFileList), 1024))    # 测试集testMat大小：(946, 1024)
    # print(testMat.shape)

    # 统计错误率
    errorCount = 0.0

    for i in range(len(testFileList)):
        fileName = testFileList[i].split('.')[0]
        number = fileName.split('_')[0]
        testMat = img2vector('testDigits/%s' % (testFileList[i]))

        # testMat：1*1024   trainingMat：1934*1024
        # 重要！每次只发送一个测试集数据（1*1024）到classify

        class_test = classify0(testMat, trainingMat, label, 3)
        print("系统推断出该数字可能是：%s\t 实际该数字是：%s" % (class_test, number))
        if (class_test != number):
            errorCount += 1.0

    errorRate = float(errorCount / len(testFileList))*100
    accuracy = 100.0 - errorRate
    print("系统正确率：%lf %%" % accuracy)

def classify0(testMat, trainingMat, label, k):
    # 训练集行数
    trainingMatSize = trainingMat.shape[0]
    diffMat = numpy.tile(testMat, (trainingMatSize, 1)) - trainingMat
    sqDiffMat = diffMat ** 2
    sqDistances = sqDiffMat.sum(axis = 1)       # axis = 1：将矩阵的每一行相加
    distances = sqDistances ** 0.5
    # 从小到大排序
    sortedDisIndices = distances.argsort()

    classCount = {}
    for i in range(k):
        type = label[sortedDisIndices[i]]
        classCount[type] = classCount.get(type, 0) + 1
    sortClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)
    return sortClassCount[0][0]

if __name__ == '__main__':
    # returnMat = img2vector('trainingDigits/0_0.txt')
    # print(returnMat)
    # (x, y) = numpy.shape(returnMat)
    # # 打印出矩阵的行和列（调试的时候用的）
    # print("矩阵的行：%d， 矩阵的列：%d" % (x, y))
    Classtest()

    # # 看下训练集的大小
    # (x, y) = numpy.shape(trainingMat)
    # print("%d %d" % (x, y))
    # # 看下测试集的大小
    # (x, y) = numpy.shape(testMat)
    # print("%d %d" % (x, y))


