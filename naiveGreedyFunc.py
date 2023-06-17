import time
from schedule_utilities import minSizeFlow
from schedule_utilities import findOverflow
from schedule_utilities import updateResPool

def naiveGreedyFunc(G,flowSet,n_port,T,flownum,queueLength,hostNum,swNum):
    start=time.time()
   
    resource_pool_naive = []
    for i in range(n_port):            
        port_list = []                  
        for j in range(T):      
            vertex_dict = {
                            'port': i+1,
                            'time': j+1,
                            'capacity': queueLength
                        }  
            port_list.append(vertex_dict)
        resource_pool_naive.append(port_list)

    for i in range(flownum):
       
        curflow=minSizeFlow(flowSet)
        
        offsetList=range(flowSet[curflow].period)
        offsetList=sorted(offsetList,reverse=True)
        for offset in offsetList:
            
            isOverflow=findOverflow(T,flowSet[curflow],offset,resource_pool_naive)
            
            if isOverflow==False:
               
                flowSet[curflow].schedFlag=1
                flowSet[curflow].offset=offset
               
                updateResPool(T,flowSet[curflow],offset,resource_pool_naive)
                break
        if flowSet[curflow].schedFlag==0:
            flowSet[curflow].schedFlag=-1

    end=time.time()
    excTime=end-start
    sucNum=0
    for flow in flowSet:
        #print(flow.offset)
        if flow.schedFlag==1:
            sucNum+=1
    sucRate=sucNum/flownum

  
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
                    allocatedQueue=allocatedQueue+queueLength-resource_pool_naive[port-1][j]['capacity']
   
    resUtiRate=allocatedQueue/allQueue
    allocatedQueue=0
    
    variance=0
    for i in range(n_port):
        for j in range(T):
            allocatedQueue=allocatedQueue+queueLength-resource_pool_naive[i][j]['capacity']
    aveQueue=allocatedQueue/T/n_port

    for i in range(n_port):
        for j in range(T):
            variance=variance+(queueLength-resource_pool_naive[i][j]['capacity']-aveQueue)*(queueLength-resource_pool_naive[i][j]['capacity']-aveQueue)
           
    variance=variance/T/n_port

    return excTime,sucRate,resUtiRate,variance


def naiveGreedyFunc_tabu(flowSet,T,flownum,resource_pool_naive):
    start=time.time()
    for i in range(flownum):
        
        curflow=minSizeFlow(flowSet)
        
        offsetList=range(flowSet[curflow].period)
        offsetList=sorted(offsetList,reverse=True)
        for offset in offsetList:
           
            isOverflow=findOverflow(T,flowSet[curflow],offset,resource_pool_naive)
            
            if isOverflow==False:
               
                flowSet[curflow].schedFlag=1
                flowSet[curflow].offset=offset
                
                updateResPool(T,flowSet[curflow],offset,resource_pool_naive)
                break
        if flowSet[curflow].schedFlag==0:
            flowSet[curflow].schedFlag=-1

    end=time.time()
    excTime=end-start
    sucNum=0
    for flow in flowSet:
        #print(flow.offset)
        if flow.schedFlag==1:
            sucNum+=1
    sucRate=sucNum/flownum
    return excTime,sucRate