"""指纹神经网络模块(FPN)
将分子指纹转换为神经网络可处理的表示
"""
from argparse import Namespace
import torch
import torch.nn as nn
import numpy as np
from rdkit import Chem
from rdkit.Chem import AllChem, MACCSkeys
from fpgnn.data import GetPubChemFPs, create_graph, get_atom_features_dim
import csv

# 全局变量，用于存储注意力权重
atts_out = []

class FPN(nn.Module):
    """指纹神经网络模块
    将分子指纹转换为神经网络可处理的表示
    
    Args:
        args: 配置参数，包含:
            fp_2_dim: 指纹转换维度
            dropout: dropout概率
            cuda: 是否使用GPU
            hidden_size: 隐藏层维度
            fp_type: 指纹类型('mixed'或其它)
            fp_changebit: 要修改的指纹位(用于解释性分析)
    """
    def __init__(self,args):
        super(FPN, self).__init__()
        self.fp_2_dim=args.fp_2_dim  # 指纹转换维度
        self.dropout_fpn = args.dropout  # dropout概率
        self.cuda = args.cuda  # 是否使用GPU
        self.hidden_dim = args.hidden_size  # 隐藏层维度
        self.args = args
        
        # 设置指纹类型和维度
        if hasattr(args,'fp_type'):
            self.fp_type = args.fp_type
        else:
            self.fp_type = 'mixed'  # 默认使用混合指纹
        
        if self.fp_type == 'mixed':
            self.fp_dim = 1489  # 混合指纹维度
        else:
            self.fp_dim = 1024  # 普通指纹维度
        
        # 设置要修改的指纹位(用于解释性分析)
        if hasattr(args,'fp_changebit'):
            self.fp_changebit = args.fp_changebit
        else:
            self.fp_changebit = None
        
        # 定义网络层
        self.fc1=nn.Linear(self.fp_dim, self.fp_2_dim)  # 第一全连接层
        self.act_func = nn.ReLU()  # 激活函数
        self.fc2 = nn.Linear(self.fp_2_dim, self.hidden_dim)  # 第二全连接层
        self.dropout = nn.Dropout(p=self.dropout_fpn)  # dropout层
    
    def forward(self, smile):
        """前向传播
        
        Args:
            smile: 分子SMILES字符串列表
            
        Returns:
            torch.Tensor: 指纹神经网络输出，形状为[batch_size, hidden_dim]
        """
        fp_list=[]
        # 为每个分子生成指纹
        for i, one in enumerate(smile):
            fp=[]
            mol = Chem.MolFromSmiles(one)
            
            if self.fp_type == 'mixed':
                fp_maccs = AllChem.GetMACCSKeysFingerprint(mol)
                fp_phaErGfp = AllChem.GetErGFingerprint(mol,fuzzIncrement=0.3,maxPath=21,minPath=1)
                fp_pubcfp = GetPubChemFPs(mol)
                fp.extend(fp_maccs)
                fp.extend(fp_phaErGfp)
                fp.extend(fp_pubcfp)
            else:
                fp_morgan = AllChem.GetMorganFingerprintAsBitVect(mol, 2, nBits=1024)
                fp.extend(fp_morgan)
            fp_list.append(fp)
                
        # 处理指纹修改位(用于解释性分析)
        if self.fp_changebit is not None and self.fp_changebit != 0:
            fp_list = np.array(fp_list)
            fp_list[:,self.fp_changebit-1] = np.ones(fp_list[:,self.fp_changebit-1].shape)
            fp_list.tolist()
        
        # 转换为张量
        fp_list = torch.Tensor(fp_list)

        # 转移到GPU(如果可用)
        if self.cuda:
            fp_list = fp_list.cuda()
        # 前向传播
        fpn_out = self.fc1(fp_list)  # 第一全连接层
        fpn_out = self.dropout(fpn_out)  # dropout
        fpn_out = self.act_func(fpn_out)  # 激活函数
        fpn_out = self.fc2(fpn_out)  # 第二全连接层
        return fpn_out

class GATLayer(nn.Module):
    """图注意力层(GAT)
    实现图注意力机制
    
    Args:
        in_features: 输入特征维度
        out_features: 输出特征维度
        dropout_gnn: dropout概率
        alpha: LeakyReLU负斜率
        inter_graph: 是否使用交互图
        concat: 是否拼接多头注意力结果
    """
    def __init__(self, in_features, out_features, dropout_gnn, alpha, inter_graph, concat=True):
        super(GATLayer, self).__init__()
        self.dropout_gnn= dropout_gnn  # dropout概率
        self.in_features = in_features  # 输入特征维度
        self.out_features = out_features  # 输出特征维度
        self.alpha = alpha  # LeakyReLU负斜率
        self.concat = concat  # 是否拼接多头注意力结果
        self.dropout = nn.Dropout(p=self.dropout_gnn)  # dropout层
        self.inter_graph = inter_graph  # 交互图

        # 可训练参数
        self.W = nn.Parameter(torch.zeros(size=(in_features, out_features)))  # 权重矩阵
        nn.init.xavier_uniform_(self.W.data, gain=1.414)  # Xavier初始化
        self.a = nn.Parameter(torch.zeros(size=(2*out_features, 1)))  # 注意力系数
        nn.init.xavier_uniform_(self.a.data, gain=1.414)  # Xavier初始化

        self.leakyrelu = nn.LeakyReLU(self.alpha)  # LeakyReLU激活函数
        # 交互图处理
        if self.inter_graph is not None:
            self.atts_out = []
    
    def forward(self,mole_out,adj):
        """前向传播
        
        Args:
            mole_out: 分子特征，形状为[num_atoms, in_features]
            adj: 邻接矩阵，形状为[num_atoms, num_atoms]
            
        Returns:
            torch.Tensor: 图注意力输出，形状为[num_atoms, out_features]
        """
        # 特征变换
        atom_feature = torch.mm(mole_out, self.W) 
        N = atom_feature.size()[0]  # 原子数量

        # 计算注意力系数
        atom_trans = torch.cat([atom_feature.repeat(1, N).view(N * N, -1), atom_feature.repeat(N, 1)], dim=1).view(N, -1, 2 * self.out_features) 
        e = self.leakyrelu(torch.matmul(atom_trans, self.a).squeeze(2)) 

        # 应用邻接矩阵掩码
        zero_vec = -9e15*torch.ones_like(e)
        attention = torch.where(adj > 0, e, zero_vec)
        
        # 交互图处理
        if self.inter_graph is not None:
            att_out = attention
            if att_out.is_cuda:
                att_out = att_out.cpu()
            att_out = np.array(att_out)
            att_out[att_out<-10000] = 0
            att_out = att_out.tolist()
            atts_out.append(att_out)
        
        # 计算注意力权重
        attention = nn.functional.softmax(attention, dim=1)
        attention = self.dropout(attention)
        output = torch.matmul(attention, atom_feature) 

        # 多头注意力拼接
        if self.concat:
            return nn.functional.elu(output)
        else:
            return output 


class GATOne(nn.Module):
    def __init__(self,args):
        super(GATOne, self).__init__()
        self.nfeat = get_atom_features_dim()
        self.nhid = args.nhid
        self.dropout_gnn = args.dropout_gat
        self.atom_dim = args.hidden_size
        self.alpha = 0.2
        self.nheads = args.nheads
        self.args = args
        self.dropout = nn.Dropout(p=self.dropout_gnn)
        
        if hasattr(args,'inter_graph'):
            self.inter_graph = args.inter_graph
        else:
            self.inter_graph = None
        
        self.attentions = [GATLayer(self.nfeat, self.nhid, dropout_gnn=self.dropout_gnn, alpha=self.alpha, inter_graph=self.inter_graph, concat=True) for _ in range(self.nheads)]
        for i, attention in enumerate(self.attentions):
            self.add_module('attention_{}'.format(i), attention)

        self.out_att = GATLayer(self.nhid * self.nheads, self.atom_dim, dropout_gnn=self.dropout_gnn, alpha=self.alpha, inter_graph=self.inter_graph, concat=False)

    def forward(self,mole_out,adj):
        mole_out = self.dropout(mole_out)
        mole_out = torch.cat([att(mole_out, adj) for att in self.attentions], dim=1)
        mole_out = self.dropout(mole_out)
        mole_out = nn.functional.elu(self.out_att(mole_out, adj))
        return nn.functional.log_softmax(mole_out, dim=1)

class GATEncoder(nn.Module):
    def __init__(self,args):
        super(GATEncoder,self).__init__()
        self.cuda = args.cuda
        self.args = args
        self.encoder = GATOne(self.args)
    
    def forward(self,mols,smiles):
        atom_feature, atom_index = mols.get_feature()
        if self.cuda:
            atom_feature = atom_feature.cuda()
        
        gat_outs=[]
        for i,one in enumerate(smiles):
            adj = []
            mol = Chem.MolFromSmiles(one)
            adj = Chem.rdmolops.GetAdjacencyMatrix(mol)
            adj = adj/1
            adj = torch.from_numpy(adj)
            if self.cuda:
                adj = adj.cuda()
            
            atom_start, atom_size = atom_index[i]
            one_feature = atom_feature[atom_start:atom_start+atom_size]
            
            gat_atoms_out = self.encoder(one_feature,adj)
            gat_out = gat_atoms_out.sum(dim=0)/atom_size
            gat_outs.append(gat_out)
        gat_outs = torch.stack(gat_outs, dim=0)
        return gat_outs

class GAT(nn.Module):
    def __init__(self,args):
        super(GAT,self).__init__()
        self.args = args
        self.encoder = GATEncoder(self.args)
        
    def forward(self,smile):
        mol = create_graph(smile, self.args)
        gat_out = self.encoder.forward(mol,smile)

        return gat_out

class FpgnnModel(nn.Module):
    def __init__(self,is_classif,gat_scale,cuda,dropout_fpn):
        super(FpgnnModel, self).__init__()
        self.gat_scale = gat_scale
        self.is_classif = is_classif
        self.cuda = cuda
        self.dropout_fpn = dropout_fpn
        if self.is_classif:
            self.sigmoid = nn.Sigmoid()

    def create_gat(self,args):
        self.encoder3 = GAT(args)
    
    def create_fpn(self,args):
        self.encoder2 = FPN(args)
    
    def create_scale(self,args):
        linear_dim = int(args.hidden_size)
        if self.gat_scale == 1:
            self.fc_gat = nn.Linear(linear_dim,linear_dim)
        elif self.gat_scale == 0:
            self.fc_fpn = nn.Linear(linear_dim,linear_dim)
        else:
            self.gat_dim = int((linear_dim*2*self.gat_scale)//1)
            self.fc_gat = nn.Linear(linear_dim,self.gat_dim)
            self.fc_fpn = nn.Linear(linear_dim,linear_dim*2-self.gat_dim)
        self.act_func = nn.ReLU()

    def create_ffn(self,args):
        linear_dim = args.hidden_size
        if self.gat_scale == 1:
            self.ffn = nn.Sequential(
                                     nn.Dropout(self.dropout_fpn),
                                     nn.Linear(in_features=linear_dim, out_features=linear_dim, bias=True),
                                     nn.ReLU(),
                                     nn.Dropout(self.dropout_fpn),
                                     nn.Linear(in_features=linear_dim, out_features=args.task_num, bias=True)
                                     )
        elif self.gat_scale == 0:
            self.ffn = nn.Sequential(
                                     nn.Dropout(self.dropout_fpn),
                                     nn.Linear(in_features=linear_dim, out_features=linear_dim, bias=True),
                                     nn.ReLU(),
                                     nn.Dropout(self.dropout_fpn),
                                     nn.Linear(in_features=linear_dim, out_features=args.task_num, bias=True)
                                     )

        else:
            self.ffn = nn.Sequential(
                                     nn.Dropout(self.dropout_fpn),
                                     nn.Linear(in_features=linear_dim*2, out_features=linear_dim, bias=True),
                                     nn.ReLU(),
                                     nn.Dropout(self.dropout_fpn),
                                     nn.Linear(in_features=linear_dim, out_features=args.task_num, bias=True)
                                     )
    
    def forward(self,input):
        if self.gat_scale == 1:
            output = self.encoder3(input)
        elif self.gat_scale == 0:
            output = self.encoder2(input)
        else:
            gat_out = self.encoder3(input)
            fpn_out = self.encoder2(input)
            gat_out = self.fc_gat(gat_out)
            gat_out = self.act_func(gat_out)
            
            fpn_out = self.fc_fpn(fpn_out)
            fpn_out = self.act_func(fpn_out)
            
            output = torch.cat([gat_out,fpn_out],axis=1)
        output = self.ffn(output)
        
        if self.is_classif and not self.training:
            output = self.sigmoid(output)
        
        return output

def get_atts_out():
    return atts_out

def FPGNN(args):
    if args.dataset_type == 'classification':
        is_classif = 1
    else:
        is_classif = 0
    model = FpgnnModel(is_classif,args.gat_scale,args.cuda,args.dropout)
    if args.gat_scale == 1:
        model.create_gat(args)
        model.create_ffn(args)
    elif args.gat_scale == 0:
        model.create_fpn(args)
        model.create_ffn(args)
    else:
        model.create_gat(args)
        model.create_fpn(args)
        model.create_scale(args)
        model.create_ffn(args)
    
    for param in model.parameters():
        if param.dim() == 1:
            nn.init.constant_(param, 0)
        else:
            nn.init.xavier_normal_(param)
    
    return model