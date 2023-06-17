def existIntersection(list1,list2):
    if list(set(list1)&set(list2)):
        return True
    else:
        return False

from numpy import isin
from schedule_utilities import *
def Sort(flowSet):
    
    for flow in flowSet:
        lcmList=[]
        for tempflow in flowSet:
            if tempflow is flow:
                continue
            else:
                if existIntersection(flow.path,tempflow.path):
                    lcmList.append(tempflow.period)
        lcm=cm(lcmList)
        
        flow.omega=gcd(flow.period,lcm)
   
    flowSetSort=sorted(flowSet,key=lambda x:x.omega,reverse=True)

    return flowSetSort
def findoffsetUpperBound(flowSetSort,flow):
    
    gcdlist=[]
    for port in flow.path:
        lcmlist=[]
        for tempflow in flowSetSort:
            if tempflow.offset !=100 and port in tempflow.path:
                lcmlist.append(tempflow.period)
       
        if lcmlist:
            lcmvalue=cm(lcmlist)
        else:
            lcmvalue=0
        gcdvalue=gcd(flow.period,lcmvalue)
        gcdlist.append(gcdvalue)
    maxgcd=max(gcdlist)
    return maxgcd

def updateM(port,flowPolled,flow,offset,tempM,confFlowSet):
    q1=flowPolled.offset+flowPolled.path.index(port)
    q2=offset+flow.path.index(port)
    if (q1-q2)%gcd(flow.period,flowPolled.period)==0:
        tempM.add_node(flow,weight=flow.size)
        tempM.add_edge(flow,flowPolled)
        confFlowSet.append(flowPolled)
    return tempM

        
def maxResourceOccupancy(flowSetSort,flow,portGraphSet,offset):
    maxOccupancy=flow.size
    flowindex=flowSetSort.index(flow)
    flowPolledSet=flowSetSort[:flowindex]
    for port in flow.path:
        confFlowSet=[]
        
        tempM=portGraphSet[port-1].graph
        tempM.add_node(flow,weight=flow.size)
        
        for flowPolled in flowPolledSet:
            if flowPolled.offset !=100 and port in flowPolled.path:
                
                tempM=updateM(port,flowPolled,flow,offset,tempM,confFlowSet)
        
        cliques=nx.find_cliques(tempM)
        for clique in cliques:
            interSet=[]
            # print("port:",port, "flow",flow.size, "offset:",offset,"maximal clique:",[clique[i].size for i in range(len(clique))])
            # print("port:",port, "flow",flow.size, "offset:",offset,"confFlowSet:",[confFlowSet[i].size for i in range(len(confFlowSet))])
            interSet=list(set(clique).intersection(set(confFlowSet)))
            # print("port:",port, "flow",flow.size, "offset:",offset,"interSet:",[interSet[i].size for i in range(len(interSet))])
            #print("interSet:",interSet,"typeof interSet",type(interSet))
            interSet.append(flow)
            # print("port:",port, "flow",flow.size, "offset:",offset,"interSet:",[interSet[i].size for i in range(len(interSet))])
            #print(interSet)
            curOccupancy=0
            for interflow in interSet:
                curOccupancy=curOccupancy+interflow.size
            if curOccupancy>maxOccupancy:
                maxOccupancy=curOccupancy
        tempM.remove_node(flow)
    return maxOccupancy


if __name__=='__main__':
    Sort(1,2)