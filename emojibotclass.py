class EmojiClass():
    def __init__(self):
        self.animatedEmotes = {}
        self.regularEmotes = {}
        self.emotesSize = 0
        self.animatedEmotesMessage = f'__***ANIMATED EMOTES:***__\n'
        self.regularEmotesMessage = f'__***EMOTES:***__\n'
        self.animatedEmotesCounterMessage = f'__***ANIMATED EMOTES:***__\n'
        self.regularEmotesCounterMessage = f'__***EMOTES:***__\n'

    def resetEmotes(self):
        self.animatedEmotes.clear()
        self.regularEmotes.clear()

    def resetMessage(self):
        self.animatedEmotesMessage = f'__***ANIMATED EMOTES:***__\n'
        self.regularEmotesMessage = f'__***EMOTES:***__\n'
        self.animatedEmotesCounterMessage = f'__***ANIMATED EMOTES:***__\n'
        self.regularEmotesCounterMessage = f'__***EMOTES:***__\n'