import time
from schedule_utilities import f_offset_occupyRes
from schedule_utilities import findMaxScoreTuple
from schedule_utilities import updateRes_and_flowDict
from FlowOffsetClass import flowTempOffset


def enhancedGreedyFunc(G,flowSet,n_port,T,flownum,queueLength,hostNum,swNum):
    start=time.time()
    
    resource_pool = []
    for i in range(n_port):             
        port_list = []                  
        for j in range(T):      
            vertex_dict = {
                            'port': i+1,
                            'time': j+1,
                            'capacity': queueLength, 
                            'related_tuple_not_scheduled':[],
                        }  
            port_list.append(vertex_dict)
        resource_pool.append(port_list)
   

   #create flow dict
    total_flow_dict={}
    for i in range(flownum):
        for tempOffset in range(flowSet[i].period):
            total_flow_dict[(flowSet[i],tempOffset)]=flowTempOffset(flowSet[i],tempOffset)
            
            f_offset_occupyRes(T,total_flow_dict[(flowSet[i],tempOffset)],resource_pool)
            


    
    for i in range(flownum):
        for tempOffset in range(flowSet[i].period):
            total_flow_dict[(flowSet[i],tempOffset)].computeMinRes()
            total_flow_dict[(flowSet[i],tempOffset)].computeScore()
    

    
    for i in range(flownum):
        
        maxScoreTuple=findMaxScoreTuple(total_flow_dict)
       
        curFlow=maxScoreTuple[0]
        curOffset=maxScoreTuple[1]
        curFlow.offset=curOffset
        curFlow.schedFlag=1
        updateRes_and_flowDict(total_flow_dict,maxScoreTuple)
        
        for j in range (curFlow.period):
            if (maxScoreTuple[0],j) in total_flow_dict.keys():
                
                del total_flow_dict[(maxScoreTuple[0],j)]
        
        if not total_flow_dict:
            break
    end=time.time()
    excTime=end-start
    sucNum=0
    for flow in flowSet:
        #print(flow.offset)
        sucNum=sucNum+flow.schedFlag
    sucRate=sucNum/flownum

   
    allQueue=T*(n_port-hostNum)*queueLength
    allocatedQueue=0

    # for i in range(n_port):
    #     for j in range(T):
    #         allocatedQueue=allocatedQueue+queueLength-resource_pool[i][j]['capacity']

    
    preNum=0
    for sw in range(swNum):
        neiborsw=list(G[sw])
        neiborsw.sort()
        for neighbor in neiborsw:
            if neighbor<swNum:
                port=preNum+neiborsw.index(neighbor)+1
                for j in range(T):
                    allocatedQueue=allocatedQueue+queueLength-resource_pool[port-1][j]['capacity']
    resUtiRate=allocatedQueue/allQueue

    
    allocatedQueue=0
    for i in range(n_port):
        for j in range(T):
            allocatedQueue=allocatedQueue+queueLength-resource_pool[i][j]['capacity']
    variance=0
    aveQueue=allocatedQueue/T/n_port

    for i in range(n_port):
        for j in range(T):
            variance=variance+(queueLength-resource_pool[i][j]['capacity']-aveQueue)*(queueLength-resource_pool[i][j]['capacity']-aveQueue)
            
    variance=variance/T/n_port

    return excTime,sucRate,resUtiRate,variance