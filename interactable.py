from abc import ABC, abstractmethod

class Interactable(ABC):
    def __init__(self, x, y, tileset, index):
        self.x = x
        self.y = y
        self.tileset = tileset
        self.index = index

    @abstractmethod
    def interact(self, obj):
        pass

    def render(self, surface, index = -1):
        if index == -1:
            index = self.index
        scale = self.tileset.scale
        tw, th = self.tileset.size

        img = self.tileset.tiles[index]
        surface.blit(img, (self.x * tw * scale, self.y * th * scale))

