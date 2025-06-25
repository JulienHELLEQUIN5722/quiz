class PossibleAnswer:
    def __init__(self, text: str, is_correct: bool, id=None):
        self.id = id
        self.text = text
        self.is_correct = is_correct

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
            is_correct=data['isCorrect']
        )

class Question:
    def __init__(self, position: int, title: str, text: str, image: str, possible_answers=None, id=None):
        self.id = id
        self.position = position
        self.title = title
        self.text = text
        self.image = image
        self.possible_answers = possible_answers if possible_answers is not None else []

    def to_dict(self):
        return {
            "id": self.id,
            "position": self.position,
            "title": self.title,
            "text": self.text,
            "image": self.image,
            "possibleAnswers": [answer.to_dict() for answer in self.possible_answers]
        }

    @classmethod
    def from_dict(cls, data):
        possible_answers = [PossibleAnswer.from_dict(ans) for ans in data['possibleAnswers']]
        return cls(
            position=data['position'],
            title=data['title'],
            text=data['text'],
            image=data['image'],
            possible_answers=possible_answers
        )
