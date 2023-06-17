#create（flow，offset）combination class
class flowTempOffset:
    def __init__(self,flow,temp_offset):
      self.flow = flow
      self.temp_offset = temp_offset
      self.occupyRes=[]
      self.minRes=0
      self.score=0

    #compute the minimimum resource
    def computeMinRes(self):
        resCap=[]
        for hop in self.occupyRes:
            resCap.append(hop['capacity'])
        self.minRes=min(resCap)

    #compute combination score
    def computeScore(self):
        self.score=self.minRes/self.flow.size