class EmojiClass():
    def __init__(self):
        self.animatedEmotes = {}
        self.regularEmotes = {}
        self.animatedEmotesMessage = f'__***ANIMATED EMOTES:***__\n'
        self.regularEmotesMessage = f'\u200b\n__***EMOTES:***__\n'

    def resetBot(self):
        self.animatedEmotes.clear()
        self.regularEmotes.clear()
        self.animatedEmotesMessage = f'__***ANIMATED EMOTES:***__\n'
        self.regularEmotesMessage = f'\u200b\n__***EMOTES:***__\n'

