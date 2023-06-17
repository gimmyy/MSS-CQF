import time
from schedule_utilities import findOverflow
from schedule_utilities import updateResPool


def naiveFunc(G,flowSet,n_port,T,flownum,queueLength,hostNum,swNum):
    start=time.time()
    # create resource pool
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
        curflow=flowSet[i]
        curOffset=0
        
        isOverflow=findOverflow(T,curflow,curOffset,resource_pool_naive)
        
        if isOverflow==False:
            curflow.schedFlag=1
            curflow.offset=0
            
            updateResPool(T,curflow,curOffset,resource_pool_naive)
    end=time.time()
    excTime=end-start
    sucNum=0
    for flow in flowSet:
        sucNum=sucNum+flow.schedFlag
    sucRate=sucNum/flownum

    
    allQueue=T*(n_port-hostNum)*queueLength#除去和host连接的端口
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
    
def naiveFunc_tabu(flowSet,T,flownum,resource_pool):
    start=time.time()
    for i in range(flownum):
        curflow=flowSet[i]
        curOffset=0
        
        isOverflow=findOverflow(T,curflow,curOffset,resource_pool)
        
        if isOverflow==False:
            curflow.schedFlag=1
            curflow.offset=0
            
            updateResPool(T,curflow,curOffset,resource_pool)
    end=time.time()
    excTime=end-start
    sucNum=0
    for flow in flowSet:
        sucNum=sucNum+flow.schedFlag
    sucRate=sucNum/flownum



    return excTime,sucRate
