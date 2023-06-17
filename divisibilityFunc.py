import time
from schedule_utilities import *
from portGraphClass import portGraph
from divisibility_utility import *

def divisibilityFunc(G,flowSet,n_port,T,flownum,queueLength,hostNum,swNum):
    start=time.time()
    #create and init the graph of each graph
    portGraphSet=[]
    for i in range(n_port):
        port_to_Graph=portGraph(i+1)
        portGraphSet.append(port_to_Graph)
    #Schedule flows
    
    flowSetSort=Sort(flowSet)
    
    for flow in flowSetSort:
        #print("current flow size ",flow.size)
        bestResCurflow=queueLength
        
        offsetUpperBound=findoffsetUpperBound(flowSetSort,flow)
        if offsetUpperBound==0:
            offsetUpperBound=1
        
        bestOffset=100
        
        for offset in range(offsetUpperBound):
            
            maxResCuroff=maxResourceOccupancy(flowSetSort,flow,portGraphSet,offset)
            #print("current flow: ",flow.size,"with the offset", offset, "max res occupancy", maxResCuroff)
            if maxResCuroff<=queueLength:
                if maxResCuroff<bestResCurflow:
                    bestOffset=offset
                    bestResCurflow=maxResCuroff
        if bestOffset !=100:#flow successfully scheduled
            
            flow.offset=bestOffset
            
            for port in flow.path:
                port_to_graph=portGraphSet[port-1].graph
                nodeList=port_to_graph.nodes()
                port_to_graph.add_node(flow,weight=flow.size)
                for existflow in nodeList:
                    if (existflow==flow):
                        continue
                    q1=existflow.offset+existflow.path.index(port)
                    q2=flow.offset+flow.path.index(port)
                    if (q1-q2)%gcd(flow.period,existflow.period)==0:
                        port_to_graph.add_edge(flow,existflow)
                #draw the graph of port

                # node_labels=nx.get_node_attributes(port_to_graph,'weight')
                # pos=nx.spring_layout(port_to_graph)
                # nx.draw_networkx(port_to_graph,pos,labels=node_labels)
                # plt.title('port {} to graph'.format(port))
                # plt.tight_layout()
                # plt.show()
    end=time.time()
    excTime=end-start

    # Create resource pool
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
        
        if(flowSetSort[i].offset!=100):
            updateResPool(T,flowSetSort[i],flowSetSort[i].offset,resource_pool_best)

    #Success Rate
    sucnum=0
    for flow in flowSetSort:
       
        if flow.offset!=100:
            sucnum+=1
    sucRate=sucnum/flownum
   

    #Resource Utilizatioin and Resource Variety
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
                    allocatedQueue=allocatedQueue+queueLength-resource_pool_best[port-1][j]['capacity']
    
    resUtiRate=allocatedQueue/allQueue

    
    allocatedQueue=0
    for i in range(n_port):
        for j in range(T):
            allocatedQueue=allocatedQueue+queueLength-resource_pool_best[i][j]['capacity']
    variance=0
    aveQueue=allocatedQueue/T/n_port

    for i in range(n_port):
        for j in range(T):
            variance=variance+(queueLength-resource_pool_best[i][j]['capacity']-aveQueue)*(queueLength-resource_pool_best[i][j]['capacity']-aveQueue)
            
    variance=variance/T/n_port
    return sucRate,excTime,resUtiRate,variance