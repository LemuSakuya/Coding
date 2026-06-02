import torch
import numpy as np

def a2t():
	np_data = np.array([[1, 2],[3,4]])

    #/********** Begin *********/
    #将np_data转为对应的tensor，赋给变量torch_data
	torch_data = torch.from_numpy(np_data)


    #/********** End *********/
	return(torch_data)