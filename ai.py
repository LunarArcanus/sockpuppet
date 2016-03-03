from pyaiml3.aiml import Kernel

class BotFactory(Kernel):
    _bots = 0

    def __init__(self, **predicates):
        super().__init__()
        for (key, value) in predicates.items():
            self.setBotPredicate(key, value)
        BotFactory._bots += 1
        self._bot_id = self._bots

    def get_bot_id(self):
        return self._bot_id

    def set_bot_id(self, bid):
        self._bot_id = bid
