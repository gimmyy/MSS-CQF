from __future__ import division
import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms.clique import node_clique_number

from FlowClass import Flow
from FlowOffsetClass import flowTempOffset

from enhancedGreedyFunc import enhancedGreedyFunc
from naiveGreedyFunc import naiveGreedyFunc
from naiveFunc import naiveFunc
from tabuFunc import tabuFunc

from schedule_utilities import *
from divisibility_utility import *
from divisibilityFunc import *


if __name__=='__main__':
    cyclenum=50
    swNum=15#switch number
    flownum=500
    queueLength=8000    #8000for15switch    5000for7switch
    ddl=15

    imp=[]
    Suc1=[]
    Suc2=[]
    Suc3=[]
    Suc4=[]
    Suc5=[]
    Suc6=[]

    Time1=[]
    Time2=[]
    Time3=[]
    Time4=[]
    Time5=[]
    Time6=[]

    resUtiRate1=[]
    resUtiRate2=[]
    resUtiRate3=[]
    resUtiRate4=[]
    resUtiRate5=[]
    resUtiRate6=[]

    variance1=[]
    variance2=[]
    variance3=[]
    variance4=[]
    variance5=[]
    variance6=[]

    for cycle in range(cyclenum):
        #generate topology G and total number of nodes 
        G,nodeNum=networkGraph(swNum,'linear')
        # nx.draw(G,with_labels=True)
        # plt.show()
        n_port=0
        for i in range(swNum):
            n_port=n_port+G.degree(i)

        #generate flows
        flowSet,T=generateFlow(G,nodeNum,swNum,flownum,ddl)
        hostNum=nodeNum-swNum

        #Alg-mss
        time_Enh,sucRate_Enh,resUtiRate_Enh,variance_Enh=enhancedGreedyFunc(G,flowSet,n_port,T,flownum,queueLength,hostNum,swNum)
        
        print("MSS-SucRate",sucRate_Enh)
        print ("MSS-ExecuteTime",time_Enh)
        print("MSS-ResourceUtilization",resUtiRate_Enh)
        print ("MSS-ResourceVariance",variance_Enh)

        for flow in flowSet:
            flow.schedFlag=0
            flow.offset=100

        #Alg-Naive greedy
        time_naive_greedy,sucRate_naive_greedy,resUtiRate_naive_greedy,variance_naive_greedy=naiveGreedyFunc(G,flowSet,n_port,T,flownum,queueLength,hostNum,swNum)

        print("Naive greedy-SucRate",sucRate_naive_greedy)
        print ("Naive greedy-ExecuteTime",time_naive_greedy)
        print("Naive greedy-ResourceUtilization",resUtiRate_naive_greedy)
        print ("Naive greedy-ResourceVariance",variance_naive_greedy)
        
        for flow in flowSet:
            flow.schedFlag=0
            flow.offset=100


        #Alg-----naive
        time_naive,sucRate_naive,resUtiRate_naive,variance_naive=naiveFunc(G,flowSet,n_port,T,flownum,queueLength,hostNum,swNum)
        print("naive-SucRate",sucRate_naive)
        print ("naive-ExecuteTime",time_naive)
        print("naive-ResourceUtilization",resUtiRate_naive)
        print ("naive-ResourceVariance",variance_naive)

        for flow in flowSet:
            flow.schedFlag=0
            flow.offset=100

        #Alg-----tabu
        time_tabu,sucRate_tabu,schedSolu,resUtiRate_tabu,variance_tabu=tabuFunc(G,flowSet,n_port,T,flownum,queueLength,hostNum,swNum)
        print("tabu-SucRate",sucRate_tabu)
        print ("tabu-ExecuteTime",time_tabu)
        print("tabu-ResourceUtilization",resUtiRate_tabu)
        print ("tabu-ResourceVariance",variance_tabu)

        for flow in flowSet:
            flow.schedFlag=0
            flow.offset=100

        #Alg--PD
        sucRate_pd,time_pd,resUtiRate_pd,variance_pd=divisibilityFunc(G,flowSet,n_port,T,flownum,queueLength,hostNum,swNum)
        print("PD-SucRate",sucRate_pd)
        print ("PD-ExecuteTime",time_pd)
        print("PD-ResourceUtilization",resUtiRate_pd)
        print ("PD-ResourceVariance",variance_pd)

        #Avarage Statics
        Suc1.append(sucRate_naive_greedy)
        Suc2.append(sucRate_Enh)
        #Suc3.append(sucRate_half_greedy)
        Suc4.append(sucRate_naive)
        Suc5.append(sucRate_tabu)
        Suc6.append(sucRate_pd)


        Time1.append(time_naive_greedy)
        Time2.append(time_Enh)
        #Time3.append(time_half_greedy)
        Time4.append(time_naive)
        Time5.append(time_tabu)
        Time6.append(time_pd)

        resUtiRate1.append(resUtiRate_naive_greedy)
        resUtiRate2.append(resUtiRate_Enh)
        #resUtiRate3.append(resUtiRate_half_greedy)
        resUtiRate4.append(resUtiRate_naive)
        resUtiRate5.append(resUtiRate_tabu)
        resUtiRate6.append(resUtiRate_pd)

        variance1.append(variance_naive_greedy)
        variance2.append(variance_Enh)
        #variance3.append(variance_half_greedy)
        variance4.append(variance_naive)
        variance5.append(variance_tabu)
        variance6.append(variance_pd)

        improve=sucRate_Enh-sucRate_naive_greedy
        print("Improve",improve)
        imp.append(improve)


    aveImp=sum(imp)/len(imp)
    aveSuc1=sum(Suc1)/len(Suc1)
    aveSuc2=sum(Suc2)/len(Suc2)
    #aveSuc3=sum(Suc3)/len(Suc3)
    aveSuc4=sum(Suc4)/len(Suc4)
    aveSuc5=sum(Suc5)/len(Suc5)
    aveSuc6=sum(Suc6)/len(Suc6)

    aveTime1=sum(Time1)/len(Time1)
    aveTime2=sum(Time2)/len(Time2)
    #aveTime3=sum(Time3)/len(Time3)
    aveTime4=sum(Time4)/len(Time4)
    aveTime5=sum(Time5)/len(Time5)
    aveTime6=sum(Time6)/len(Time6)

    aveResUti1=sum(resUtiRate1)/len(resUtiRate1)
    aveResUti2=sum(resUtiRate2)/len(resUtiRate2)
    #aveResUti3=sum(resUtiRate3)/len(resUtiRate3)
    aveResUti4=sum(resUtiRate4)/len(resUtiRate4)
    aveResUti5=sum(resUtiRate5)/len(resUtiRate5)
    aveResUti6=sum(resUtiRate6)/len(resUtiRate6)

    aveVari1=sum(variance1)/len(variance1)
    aveVari2=sum(variance2)/len(variance2)
    #aveVari3=sum(variance3)/len(variance3)
    aveVari4=sum(variance4)/len(variance4)
    aveVari5=sum(variance5)/len(variance5)
    aveVari6=sum(variance6)/len(variance6)


    print("NaiveGreedyAveSuc",aveSuc1)
    print("MSSAveSuc",aveSuc2)
    #print("alg3",aveSuc3)
    print("NaiveAveSuc",aveSuc4)
    print("tabuAveSuc",aveSuc5)
    print("PDAveSuc",aveSuc6)

    print("NaiveGreedyAveTime",aveTime1)
    print("MSSAveTime",aveTime2)
    #print("alg3",aveTime3)
    print("NaiveAveTime",aveTime4)
    print("tabuAveTime",aveTime5)
    print("PDAveTime",aveTime6)

    print("NaiveGreedyAveResUti",aveResUti1)
    print("MSSAveResUti",aveResUti2)
    #print("alg3",aveResUti3)
    print("NaiveAveResUti",aveResUti4)
    print("tabuAveResUti",aveResUti5)
    print("PDAveResUti",aveResUti6)

    print("NaiveGreedyAveResVar",aveVari1)
    print("MSSAveResVar",aveVari2)
    #print("alg3",aveVari3)
    print("NaiveAveResVar",aveVari4)
    print("tabuAveResVar",aveVari5)
    print("PDAveResVar",aveVari6)


    print("AveImp",aveImp)