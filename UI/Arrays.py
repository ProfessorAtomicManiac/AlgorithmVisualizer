import pygame

class ArrayElement(pygame.sprite.Sprite):
    def __init__(self, color, coords, dim):
        super().__init__()
        self.image = pygame.Surface(dim)
        self.color = color
        self.rect = self.image.get_rect(bottomleft = coords)
        self.coords = coords
        self.image.fill(color)
    
    def update(self):
        self.rect = self.image.get_rect(bottomleft = self.coords)

    def change_color(self, color):
        self.color = color

class Array():
    '''The actual array with ArrayElements as its elements
       array_group = Sprite Group containing all the array_elements
       dim = dimenisons of the entire array (rectangle enclosing the array) in (width, height) form
       coords = where the array will be placed in (x, y) form
       end = the maximum possible value of the array (will sort from 1-end)
    '''
    def __init__(self, array_group, dim, coords, end):
        self.array_group = array_group
        self.dim = dim
        self.coords = coords
        self.end = end
        width = dim[0]/self.end
        y = coords[1] + dim[1]
        for i in range(1, self.end+1):
            height = i*dim[1]/self.end
            x = coords[0] + (i-1)*dim[0]/self.end
            self.array_group.add(ArrayElement("#ffffff", (x,y), (width, height)))
            print("{},{}  {},{}".format(x, y, width, height))

    def shuffle(self):
        pass