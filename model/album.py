from dataclasses import dataclass


@dataclass
class Album:
    id:int
    title:str
    artist_id:int
    duration: float

    def __str__(self):
        return self.title

    def __repr__(self):
        return self.title

    def __hash__(self):
        return hash(self.id)