from event import Event
from interactable import Interactable
from objects.player import Player


class Spike(Interactable):
    def __init__(self, x, y, tileset):
        super().__init__(x, y, tileset, 208)

    def interact(self, obj):
        if type(obj) is Player:
            return Event.PLAYER_DIE
