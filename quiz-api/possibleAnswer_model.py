class PossibleAnswer:
    def __init__(self, text, is_correct, position):
        self.text = text
        self.is_correct = is_correct
        self.position = position

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "is_correct": self.is_correct
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            text=data['text'],
            is_correct=bool(data['isCorrect'])
        )
