import random
import time
import copy

from FlowClass import Flow
from naiveFunc import naiveFunc_tabu
from naiveGreedyFunc import naiveGreedyFunc_tabu


from schedule_utilities import dsk_remove_flows, updateResPool
from schedule_utilities import dsk_insert_flows
from schedule_utilities import random_remove_flows
from schedule_utilities import random_insert_flows
from schedule_utilities import tabu_update

def tabuFunc(G,flowSet,n_port,T,flownum,queueLength,hostNum,swNum):
    start=time.time()

    #init tabu parameter
    tabu_size=50
    tabu_max_iter=300
    max_num=10
    max_repeat=10
    tabuOk=False
    canSet=[]

    
    resource_pool = []
    for i in range(n_port):             
        port_list = []                 
        for j in range(T):     
            vertex_dict = {
                            'port': i+1,
                            'time': j+1,
                            'capacity': queueLength
                        }  
            port_list.append(vertex_dict)
        resource_pool.append(port_list)
    
    
    time_init,sucRate_init=naiveGreedyFunc_tabu(flowSet,T,flownum,resource_pool)
    offsetList=[]
    for flow in flowSet:
        offsetList.append(flow.offset)

    
    flowSet_cur=flowSet
    resource_pool_cur=resource_pool
    bestResult={'schedSolu':offsetList,'sucRate':sucRate_init}
    curResult=bestResult
    bestList=[]
    
    tabu_list=[]
    for cur_iter in range(tabu_max_iter):
        cur_num=0
        neighbor=[]

        
        while cur_num<max_num:
            resource_pool=copy.deepcopy(resource_pool_cur)
            flowSet_can=copy.deepcopy(flowSet_cur)
            curSoluList=[]
            sigma=random.uniform(0,1)
            
            if sigma>=0.7:
                dsk_remove_flows(flowSet_can,resource_pool,T)
               
                dsk_insert_flows(flowSet_can,resource_pool,T)
              
            else:
                random_remove_flows(flowSet_can,resource_pool,T)
                random_insert_flows(flowSet_can,resource_pool,T)

            sucNum=0
            for flow in flowSet_can:
                curSoluList.append(flow.offset)
                if flow.offset!=100:
                    sucNum+=1
            sucRate=sucNum/flownum
            schedDict={'schedSolu':curSoluList,'sucRate':sucRate}
            neighbor.append(schedDict)
            cur_num+=1
        canSet.extend(neighbor)
       
        curResult=tabu_update(neighbor,tabu_list,tabu_size,bestResult)
       
        for i in range(flownum):
            flowSet_cur[i].offset=curResult['schedSolu'][i]
            if flowSet_cur[i].offset==100:
                flowSet_cur[i].schedFlag=0
            else:
                flowSet_cur[i].schedFlag=1
                updateResPool(T,flowSet_cur[i],flowSet_cur[i].offset,resource_pool_cur)
        bestDict={'result':bestResult['schedSolu'],'repeatNum':1}
      
        isrepeat=False
        for dict in bestList:
            if dict['result']==bestDict['result']:
                dict['repeatNum']+=1
                isrepeat=True
                if(dict['repeatNum']==max_repeat):
                    tabuOk=True
                break
        if isrepeat==False:
            bestList.append(bestDict)
        if tabuOk:
            print("Repeat Too many times")
            break
        cur_iter+=1
    
    end=time.time()
    excTime=end-start

    
    resource_pool_best = []
    for i in range(n_port):             
        port_list = []                  
        for j in range(T):     
            vertex_dict = {
                            'port': i+1,
                            'time': j+1,
                            'capacity': queueLength
                        }  
            port_list.append(vertex_dict)
        resource_pool_best.append(port_list)
    

    for i in range(flownum):
        
        flowSet[i].offset=bestResult['schedSolu'][i]
        if(flowSet[i].offset!=100):
            updateResPool(T,flowSet[i],flowSet[i].offset,resource_pool_best)

    
    allQueue=T*(n_port-hostNum)*queueLength
    allocatedQueue=0

  
    preNum=0
    for sw in range(swNum):
        neiborsw=list(G[sw])
        neiborsw.sort()
        for neighbor in neiborsw:
            if neighbor<swNum:
                port=preNum+neiborsw.index(neighbor)+1
                for j in range(T):
                    allocatedQueue=allocatedQueue+queueLength-resource_pool_best[port-1][j]['capacity']
   
    resUtiRate=allocatedQueue/allQueue
    allocatedQueue=0
    
    variance=0
    for i in range(n_port):
        for j in range(T):
            allocatedQueue=allocatedQueue+queueLength-resource_pool_best[i][j]['capacity']
    aveQueue=allocatedQueue/T/n_port

    for i in range(n_port):
        for j in range(T):
            variance=variance+(queueLength-resource_pool_best[i][j]['capacity']-aveQueue)*(queueLength-resource_pool_best[i][j]['capacity']-aveQueue)
            
    variance=variance/T/n_port

    return excTime,bestResult['sucRate'],bestResult['schedSolu'],resUtiRate,variance
    