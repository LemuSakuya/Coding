# 引入numpy库
import numpy as np
# 定义opeadd函数
def opeadd(m,b,n):
	'''
	参数：
	m:是一个数组
	b:是一个列表
	n:是列表中的索引
	你需要做的是 m+b[n]
	返回值:
	ret: 一个numpy数组
	'''
	ret = 0
	# 加法运算
	#********** Begin *********#
	ret = m + b[n]
	#********** End **********#

	return ret
# 定义opemul函数
def opemul(m,b,n):
	'''
	参数：
	m:是一个数组
	b:是一个列表
	n:是列表中的索引
	你需要做的是 m*b[n]
	返回值:
	ret: 一个numpy数组
	'''
	ret = 0
	# 乘法运算
	#********** Begin *********#
	ret = m * b[n]
	#********** End **********#
	return ret

# 定义opesubtract函数
def opesubtract(m,b,n):
	'''
	参数：
	m:是一个数组
	b:是一个列表
	n:是列表中的索引
	你需要做的是 m-b[n]
	返回值:
	ret: 一个numpy数组
	'''
	ret = 0
	# 减法运算
	#********** Begin *********#
	ret = m - b[n]
	#********** End **********#
	return ret

# 定义opedot函数
def opedot(m,b,n):
	'''
	参数：
	m:是一个数组
	b:是一个列表
	n:是列表中的索引
	你需要做的是 np.dot(m,b[n])
	返回值:
	ret: 一个numpy数组
	'''
	ret = 0
	# 点乘运算
	#********** Begin *********#
	ret = np.dot(m, b[n])
	#********** End **********#
	return ret