import heapq

class EmojiClass():
    def __init__(self):
        self.animatedEmotes = {}
        self.regularEmotes = {}
        self.top5AnimatedEmotes = {}
        self.top5RegularEmotes = {}
        self.emotesAmt = 0
        # self.animatedEmotesMessage = f'__***ANIMATED EMOTES:***__\n'
        # self.regularEmotesMessage = f'__***EMOTES:***__\n'
        # self.animatedEmotesCounterMessage = f'__***ANIMATED EMOTES:***__\n'
        # self.regularEmotesCounterMessage = f'__***EMOTES:***__\n'

    def resetEmotes(self):
        self.animatedEmotes.clear()
        self.regularEmotes.clear()

    # def resetMessage(self):
    #     self.animatedEmotesMessage = f'__***ANIMATED EMOTES:***__\n'
    #     self.regularEmotesMessage = f'__***EMOTES:***__\n'
    #     self.animatedEmotesCounterMessage = f'__***ANIMATED EMOTES:***__\n'
    #     self.regularEmotesCounterMessage = f'__***EMOTES:***__\n'
    
    def getTop5(self, animatedList, regularList):
        dict1 = {}
        dict2 = {}
        dict1 = heapq.nlargest(5, animatedList)
        dict2 = heapq.nlargest(5, regularList)
        self.top5AnimatedEmotes.clear()
        self.top5RegularEmotes.clear()
        self.top5AnimatedEmotes = dict1
        self.top5RegularEmotes = dict2