class ResultModel:
    def __init__(self):
        super().__init__()
        self.code = 0
        self.message = None
        self.model = None

    def success(self):
        return self.code == 0

    def fail(self):
        return self.code != 0

    @staticmethod
    def ok(model=None):
        return ResultModel.res(0, model=model)

    @staticmethod
    def err(message, model=None):
        return ResultModel.res(1, message, model)

    @staticmethod
    def res(code, message=None, model=None):
        result = ResultModel()
        result.code = code
        result.message = message
        result.model = model
        return result
