# -*- encoding: utf-8 -*-
"""
Created on Wed Sat 13 15:22:36 2019

@author: 蔡佳超
"""

from Ant import AntList
import time
from MyFuncTool import GetData,ResultShow
import numpy as np

class TSP(object):
    def __init__(self,Position,Dist,CityNum,alpha=1,beta=2,rho=0.5,Q=100,aCrossRate=0.9,aMutationRage=0.9):
        """ 构造函数 """
        self.citys=Position                         # 城市坐标
        self.dist=Dist                              # 城市距离矩阵
        self.citynum=CityNum                        # 城市数量
        
        self.ant =AntList(numant=25,                # 蚂蚁个数
                    distfunc=self.distance,         # 计算距离的函数
                    getEtatable=self.defEtatable,   # 定义启发式矩阵函数
                    numcity=self.citynum,           # 城市个数
                    alpha=alpha,                    # 信息素重要程度因子
                    beta=beta,                      # 期望启发式因子
                    rho=rho,                        # 信息素的挥发速度
                    Q=Q,                            # 品质因子
                    aCrossRate=aCrossRate,          # 交叉率
                    aMutationRage=aMutationRage     # 突变概率
                        )                           
        
        
        
    def defEtatable(self):
        return 1.0/(self.dist+np.diag([1e10]*self.citynum))

    def distance(self, path):
        # 计算从初始城市到最后一个城市的路程
        distance = sum([self.dist[city1][city2] for city1,city2 in 
                            zip(path[:self.citynum], path[1:self.citynum+1])])
        # 计算从初始城市到最后一个城市再回到初始城市所经历的总距离
        distance += self.dist[path[-1]][0]

        return distance

    def findq0(self):
        qn=3.2/np.power((self.generate_max-1),2)*np.power(self.ant.generation-(self.generate_max-1)/2,2)+0.1
        return qn
    
    def run(self, generate=0):
        distance_list = []
        self.generate_max=generate
        while generate > 0:
            self.ant.nextGeneration_mix(self.findq0())
            distance = self.ant.bestantunit.length
            distance_list.append(distance)
            generate -= 1
		
        return self.ant.bestantunit.length,self.ant.bestantunit.path,distance_list
