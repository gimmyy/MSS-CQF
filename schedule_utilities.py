import networkx as nx
import numpy as np
import random
import copy

from FlowClass import Flow
#Functions for Schedule


def gcd(x, y):
   
   if x > y:
       smaller = y
   else:
       smaller = x
   if smaller is 0:
        return 0
   for i in range(1,smaller + 1):
       if((x % i == 0) and (y % i == 0)):
           hcf = i
   return hcf


def cm(param):
    L = list(sorted(param))
    k = 0
    while 1:
        k += 1
        g = L[ -1 ] * k
        for i in L:
            if g % i:
                break
            elif i == L[ -1 ]:
                return g

#Create topology
def networkGraph(swNum,topology):

    hostArray=np.random.randint(1,4,size=swNum)
    
    print(hostArray)
    hostNum=np.sum(hostArray)
    print(hostNum)

    nodeNum=swNum+hostNum
    #Create graph
    G = nx.Graph()
    if(topology is 'mix'):
        #add switch
        for i in range(7):
            G.add_edge(i,i+1)
        G.add_edge(7,0)
        G.add_edge(8,0)
        G.add_edge(8,9)
        G.add_edge(4,10)
        G.add_edge(4,11)
        G.add_edge(4,12)
        G.add_edge(6,13)
        G.add_edge(6,14)
        G.add_edge(14,13)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
        #add host
        prenum=swNum
        for i in range(swNum):
            for j in range(hostArray[i]):
                G.add_edge(i,prenum+j)
            prenum=prenum+hostArray[i]
    else:
        if(topology is 'ring'):
            for i in range(swNum):
                if(i!=swNum-1):
                    G.add_edge(i,i+1)
                else:
                    G.add_edge(i,0)
        elif topology is 'linear':
            for i in range(swNum-1):
                G.add_edge(i,i+1)
        elif topology is 'star15':
            # for i in range(6):
            #     G.add_edge(12,i+6)
            #     G.add_edge(i,6+i)
            # G.add_edge(5,14)
            # G.add_edge(2,13)
            for i in range(7):
                G.add_edge(14,i+7)
                G.add_edge(i,i+7)
        else:
            for i in range(swNum-1):
                G.add_edge(0,i+1)
        prenum=swNum
        for i in range(swNum):
            for j in range(hostArray[i]):
                G.add_edge(i,prenum+j)
            prenum=prenum+hostArray[i]
    return G,nodeNum

#given graph, src and dst, generate path
def srcDst_flowPath(G,src,dst):
    path=nx.shortest_path(G, source=src, target=dst)
    flowpath=[]
    pathLen=len(path)
    for i in range(pathLen-1):
        if i == 0:
            continue
        else:
            curNode=path[i]
            nextNode=path[i+1]
            prePortNum=0
            if curNode>0:
                for j in range(curNode):
                    prePortNum=prePortNum+G.degree(j)
            neiborCurNode=list(G[curNode])
            neiborCurNode.sort()
            portAB=neiborCurNode.index(nextNode)+1
            port=prePortNum+portAB
        flowpath.append(port)
    return flowpath

#generate flowset
def generateFlow(G,nodeNum,swNum,flownum,ddl):
    src=[]
    dst=[]
    size=[]
    period=[]
    deadline=[]
    path=[]
    #periodSet=[7,8,9,10,11,]
    
    for n in range(flownum):
        srcDst=random.sample(range(1,nodeNum-swNum),2)
        srcDst=[i+swNum-1 for i in srcDst]
        src.append(srcDst[0])
        dst.append(srcDst[1])
        size.append(random.randint(64,1500))
        period.append(random.randint(2,9))      #(5,11)&(2,9)
        #period.append(random.choice(periodSet))
        deadline.append(ddl)
        path.append(srcDst_flowPath(G,srcDst[0],srcDst[1]))
    # flownum=10
    # queueLength=1500
    
    # src=[17,17,18,16,16,17,20,16,14,11]
    # dst=[14,10,16,17,11,20,18,18,10,15]
    # size=[1196,761,1271,1253,78,1422,379,1484,680,249]
    # period=[2,3,3,4,4,4,2,2,2,3]
    # path=[[19,16,15],[19,16,12,9],[21],[22],[19,16,12,10],[20,27],[25,23],[23],[12,9],[8,13,18]]
    # deadline=[9,9,9,4,12,10,12,5,8,9]
    flowSet=[]
    for i in range(flownum):
        flowNew=Flow(src[i],dst[i],size[i],period[i],path[i],deadline[i])
        flowSet.append(flowNew)
    T=cm(period)
    return flowSet,T

#determine the resource blocks which the combination （f,offset）effects, determine the combinations (f,offset)
#each resource block Q[][] effects

def f_offset_occupyRes(T,flowTempOffset,resource_pool):
    for i in range(len(flowTempOffset.flow.path)):#i表示第几跳-1
        port=flowTempOffset.flow.path[i]
        
        packetNum=int(T/flowTempOffset.flow.period)
       
        time=flowTempOffset.temp_offset+i+1
        for j in range(packetNum):
            if time>T:
                time=time-T
            flowTempOffset.occupyRes.append(resource_pool[port-1][time-1])
            resource_pool[port-1][time-1]['related_tuple_not_scheduled'].append((flowTempOffset.flow,flowTempOffset.temp_offset))
            time=time+flowTempOffset.flow.period

def findMaxScoreTuple(total_flow_dict):
    maxscore=0
    maxscoreTuple=()
    for item in total_flow_dict.items():
        if(item[1].score>=maxscore):
            maxscore=item[1].score
            maxscoreTuple=item[0]
    return maxscoreTuple

def updateFlowDict(resBlock,maxScoreTuple,total_flow_dict):
    for tuple in resBlock['related_tuple_not_scheduled']:
        
        if tuple == maxScoreTuple:
            
            continue
        
        elif resBlock['capacity']<tuple[0].size:
            
            if tuple in total_flow_dict.keys():
                total_flow_dict[tuple].minRes=-1
                del total_flow_dict[tuple]
        else:
            if tuple in total_flow_dict.keys() and total_flow_dict[tuple].minRes>resBlock['capacity']:
                
                total_flow_dict[tuple].computeMinRes()
                total_flow_dict[tuple].computeScore()

def updateRes_and_flowDict(total_flow_dict,maxScoreTuple):
    curFlow=maxScoreTuple[0]
    for resBlock in total_flow_dict[maxScoreTuple].occupyRes:
        #update resource capacity
        resBlock['capacity']=resBlock['capacity']-curFlow.size
        
        updateFlowDict(resBlock,maxScoreTuple,total_flow_dict)
        
        resBlock['related_tuple_not_scheduled'].remove(maxScoreTuple)


########################################naiveGreedy########################################
def minSizeFlow(flowSet):
    minSize=1501
    for i in range(len(flowSet)):
        
        if (flowSet[i].size < minSize) and (flowSet[i].schedFlag==0):
            minSize=flowSet[i].size
            minFlowInd=i
   
    return minFlowInd

def findOverflow(T,flow,offset,resource_pool):
    for i in range(len(flow.path)):
        port=flow.path[i]
        
        packetNum=int(T/flow.period)
       
        time=offset+i+1
        for j in range(packetNum):
            if time>T:
                time=time-T
            if resource_pool[port-1][time-1]['capacity']<flow.size:
                return True
            else:
                time=time+flow.period
    return False

def updateResPool(T,flow,offset,resource_pool):
    for i in range(len(flow.path)):
        port=flow.path[i]
       
        packetNum=int(T/flow.period)
       
        time=offset+i+1
        for j in range(packetNum):
            if time>T:
                time=time-T
            resource_pool[port-1][time-1]['capacity']=resource_pool[port-1][time-1]['capacity']-flow.size
           
            time=time+flow.period


########################################tabuSearch中的函数########################################
def updateResPoolReverse(T,flow,resource_pool):
    offset=flow.offset
    for i in range(len(flow.path)):
        port=flow.path[i]
       
        packetNum=int(T/flow.period)
       
        time=offset+i+1
        for j in range(packetNum):
            if time>T:
                time=time-T
            resource_pool[port-1][time-1]['capacity']+=flow.size
          
            time=time+flow.period



def dsk_remove_flows(flowSet_can,resource_pool,T):
  
    flowSuc=[]
    for flow in flowSet_can:
        if flow.offset != 100:
            flowSuc.append(flow)
    
    flowSuc.sort(key=lambda x:x.size,reverse=True)
   
    if(len(flowSuc)<5):
        removeNum=len(flowSuc)
    else:
        removeNum=5
   
    for i in range(removeNum):
        updateResPoolReverse(T,flowSuc[i],resource_pool)
        flowSuc[i].offset=100
        flowSuc[i].schedFlag=0
    
    return 



def dsk_insert_flows(flowSet_can,resource_pool,T):
   
    flowFail=[]
    for flow in flowSet_can:
        if flow.offset==100:
            flowFail.append(flow)
   
    flowFail.sort(key=lambda x:x.size,reverse=False)
    for flow in flowFail:
        offsetList=range(flow.period)
        offsetList=sorted(offsetList,reverse=True)
        for offset in offsetList:
            isOverflow=findOverflow(T,flow,offset,resource_pool)
         
            if isOverflow==False:
                
                flow.schedFlag=1
                flow.offset=offset
               
                updateResPool(T,flow,offset,resource_pool)
               
                break
    return 

def random_remove_flows(flowSet_can,resource_pool,T):
    
    flowSuc=[]
    for flow in flowSet_can:
        if flow.offset !=100:
            flowSuc.append(flow)
   
    if(len(flowSuc)<5):
        randlist=range(len(flowSuc))
    else:
        randlist=random.sample(range(0,len(flowSuc)),5)
    for num in randlist:
        updateResPoolReverse(T,flowSuc[num],resource_pool)
        flowSuc[num].offset=100
        flowSuc[num].schedFlag=0
    return

def random_insert_flows(flowSet_can,resource_pool,T):
    
    flowFail=[]
    for flow in flowSet_can:
         if flow.offset==100:
             flowFail.append(flow)
    
    while flowFail:
        randFlowInd=random.sample(range(0,len(flowFail)),1)[0]
       
        randSlot=random.sample(range(0,flowFail[randFlowInd].period),1)[0]
        isOverflow=findOverflow(T,flowFail[randFlowInd],randSlot,resource_pool)
        if isOverflow==False:
            
            flowFail[randFlowInd].schedFlag=1
            flowFail[randFlowInd].offset=randSlot
            
            updateResPool(T,flowFail[randFlowInd],randSlot,resource_pool)
        flowFail.pop(randFlowInd)
    return

def ifInTabu(tabu_list,item):
    for solu in tabu_list:
        if solu==item:
            return True
    return False



def tabu_update(neighbor,tabu_list,tabu_size,bestResult):
    
    neighbor_sort=sorted(neighbor,key=lambda e:e.__getitem__('sucRate'),reverse=True)
   
    canSolu=neighbor_sort[0]
    
    inTabu=ifInTabu(tabu_list,canSolu['schedSolu'])
    if(inTabu):
        
        if(canSolu['sucRate']>bestResult['sucRate']):
            
            bestResult['schedSolu']=canSolu['schedSolu']
            bestResult['sucRate']=canSolu['sucRate']
            
            curResult=copy.deepcopy(bestResult)
            
            tabu_list.remove(canSolu['schedSolu'])
            
            tabu_list.append(canSolu['schedSolu'])
        else:
           
            allInTabu=True
            for soluDict in neighbor_sort[1:]:
                
                if not ifInTabu(tabu_list,soluDict['schedSolu']):
                    
                    curResult=copy.deepcopy(soluDict)
                   
                    if len(tabu_list)==tabu_size:
                        tabu_list.pop(0)
                    tabu_list.append(soluDict['schedSolu'])
                    allInTabu=False
                    break
            if(allInTabu):
                
                curResult=copy.deepcopy(canSolu)
                
                tabu_list.remove(canSolu['schedSolu'])
               
                tabu_list.append(canSolu['schedSolu'])
    
    else:
        if canSolu['sucRate']>bestResult['sucRate']:
            
            bestResult['schedSolu']=canSolu['schedSolu']
            bestResult['sucRate']=canSolu['sucRate']
        
        curResult=copy.deepcopy(canSolu)
        
        if len(tabu_list)==tabu_size:
            tabu_list.pop(0)
        tabu_list.append(canSolu['schedSolu'])
    return curResult

