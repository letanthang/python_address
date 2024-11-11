from .result import Result
class TestCase:
    def __init__(self, input_text='', output=None):
        self.input = input_text
        self.output = output if output else Result()