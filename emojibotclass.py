import heapq

class EmojiClass():
    def __init__(self):
        # self.animatedEmotes = {}
        # self.regularEmotes = {}
        self.emotesList = {}
        self.embedList = []
        self.top5AnimatedEmotes = {}
        self.top5RegularEmotes = {}
        self.pg_num = 0

    # def resetEmotes(self):
    #     self.animatedEmotes.clear()
    #     self.regularEmotes.clear()

    # def getTop5(self, animatedList, regularList):
    #     self.top5AnimatedEmotes.clear()
    #     self.top5RegularEmotes.clear()
    #     self.top5AnimatedEmotes = heapq.nlargest(5, animatedList, key=animatedList.get)
    #     self.top5RegularEmotes = heapq.nlargest(5, regularList, key=regularList.get)