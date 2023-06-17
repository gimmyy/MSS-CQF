#创建流类型
class Flow:
   flowCount = 0
   def __init__(self, src, dst,size,period,path,deadline):
      self.src = src
      self.dst = dst
      self.size = size
      self.period = period
      self.path = path#端口路径
      self.deadline = deadline
      self.schedFlag=0
      self.offset=100
      self.hopnum=0
   
   def displayCount(self):
     print ("Total Flow " , Flow.flowCount)
 
   def displayFlow(self):
      print ("src : ", self.src,  "dst: ", self.dst,"offset: ", self.offset,"path",self.path)