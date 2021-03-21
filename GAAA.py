# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 23:23:02 2019

@author: 蔡佳超
"""
from Ant import AntList
from Ant import AntUnit
from GA import GAList
from GA import GAUnit
import numpy as np
import time
from MyFuncTool import GetData,ResultShow

class TSP(object):
    def __init__(self,Position,Dist,CityNum,alpha=1,beta=2,rho=0.5,Q=100,aCrossRate=0.6,aMutationRage=0.01,aUnitCount=100):
        """ 构造函数 """
        self.citys=Position                            # 城市坐标
        self.dist=Dist                                # 城市距离矩阵
        self.citynum=CityNum                        # 城市数量
        self.ant =AntList(numant=25,                # 蚂蚁个数
                    distfunc=self.distance,         # 计算距离的函数
                    getEtatable=self.defEtatable,   # 定义启发式矩阵函数
                    numcity=self.citynum,           # 城市个数
                    alpha=alpha,                    # 信息素重要程度因子
                    beta=beta,                      # 期望启发式因子
                    rho=rho,                        # 信息素的挥发速度
                    Q=Q)                            # 品质因子

        self.ga =GAList(aCrossRate=aCrossRate,                # 交叉率
                        aMutationRage=aMutationRage,            # 突变概率
                        aUnitCount=aUnitCount,                # 一个种群中的个体数
                        aGeneLenght=self.citynum,    # 基因长度（城市数）
                        aMatchFun=self.matchFun())    # 适配函数
    
    def defEtatable(self):
        return 1.0/(self.dist+np.diag([1e10]*self.citynum))

    def distance(self, path):
        # 计算从初始城市到最后一个城市的路程
        distance = sum([self.dist[city1][city2] for city1,city2 in 
                            zip(path[:self.citynum], path[1:self.citynum+1])])
        # 计算从初始城市到最后一个城市再回到初始城市所经历的总距离
        distance += self.dist[path[-1]][0]

        return distance
    
    def matchFun(self):
        return lambda life: 1.0 / self.distance(life.gene)
    
    def findq0(self):
        qn=3.2/np.power((self.generate_ant_max-1),2)*np.power(self.ant.generation-(self.generate_ant_max-1)/2,2)+0.1
        return qn
    
    def run(self, generate_ant=0, generate_ga=0):
        distance_list = []
        
        self.ant.nextGeneration()
        self.ant.generation-=1
        newPop = []                        # 新种群
        for i in range(self.ant.numant):
            antu=self.ant.population[i]
            lifeu=GAUnit(antu.path)
            newPop.append(lifeu)
        self.ga.best=GAUnit(self.ant.bestantunit.path,1/self.ant.bestantunit.length)
        
        self.ga.population = newPop
        while generate_ga > 0:
            self.ga.nextGeneration()       	
            distance = self.distance(self.ga.best.gene)        
            distance_list.append(distance)
            generate_ga -= 1
             
        self.ga.population.sort(key=lambda GAUnit:GAUnit.value,reverse=True)
        for k in range(2):
            genepath=self.ga.population[k].gene
            for i in range(self.citynum-1):
                self.ant.pheromonetable[genepath[i]][genepath[i+1]] += 0.5
                self.ant.pheromonetable[genepath[self.citynum-1]][genepath[0]] += 0.5
        self.ant.bestantunit=AntUnit(self.ga.best.gene,self.ant.distfunc(self.ga.best.gene))
        self.generate_ant_max=generate_ant
        while generate_ant > 0:            
            self.ant.nextGeneration(self.findq0())
            distance = self.ant.bestantunit.length
            distance_list.append(distance)
            generate_ant -= 1
        

            
        return self.ant.bestantunit.length,self.ant.bestantunit.path,distance_list

