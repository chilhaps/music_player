class PlayerStateBase():
    def __init__(self, _ctx, ID_str):
        self._ctx = _ctx
        self.ID_str = ID_str

    def get_ID(self):
        return self.ID_str

    def execute(self):
        pass