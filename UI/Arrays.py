import time
import pygame
import random

class ArrayElement(pygame.sprite.Sprite):

    ''' Creates an element of our special array
        @coords = coordinates of where the bottom-left of the element will be placed
        @dim = dimensions of the element
        @visited = needed to check whether some array index is being accessed/swapped (boolean array)
        @list = needed to check if element was swapped and should update the swappage (regular integer array)
        @height_unit = unit to help determine height of the array element (self.array_dim[1]/self.end)
    '''
    def __init__(self, coords, dim, visited, list, height_unit, index):
        super().__init__()
        self.image = pygame.Surface(dim)
        self.color = "#ffffff"
        self.rect = self.image.get_rect(bottomleft = coords)
        self.coords = coords
        self.dim = dim
        self.image.fill(self.color)
        self.visited = visited
        self.list = list
        self.height_unit = height_unit
        self.index = index
        self.val = list[index]

        # Timing how long the visited array should be red
        self.still_colored = False
        self.timer = 0
    
    def update(self):
        self.image = pygame.Surface(self.dim)
        self.image.fill(self.color)
        self.rect = self.image.get_rect(bottomleft = self.coords)
        self.check_change()
        self.change_color()

    def check_change(self):
        if (self.list[self.index] != self.val):
            #print("index is changed")
            dim = list(self.dim)
            dim[1] = self.list[self.index] * self.height_unit
            self.val = self.list[self.index]
            self.dim = tuple(dim)
            

    def change_color(self):
        if (self.visited[self.index]):
            #print("index is visited")
            self.still_colored = True
            self.color = "#fc0505"
            self.visited[self.index] = False
        
        if (self.still_colored):
            self.timer += 0.1
            if (self.timer > 0.1):
                #print("Index is unvisited")
                self.still_colored = False
                self.color = "#ffffff"
                self.timer = 0
            
class Array():
    '''The actual array with ArrayElements as its elements
       array_group = Sprite Group containing all the array_elements
       dim = dimenisons of the entire array (rectangle enclosing the array) in (width, height) form
       coords = where the array will be placed in (x, y) form
       end = the maximum possible value of the array (will sort from 1-end)
    '''
    def __init__(self, array_group, dim, coords, end, delay = 0.01):
        self.array_group = array_group
        self.list = []
        self.visited = []
        for i in range(1, end+1):
            self.list.append(i)
            self.visited.append(False)
        self.dim = dim
        self.coords = coords
        self.end = end
        self.delay = delay
        self.createList()
        
    def createList(self):
        width = self.dim[0]/self.end
        y = self.coords[1] + self.dim[1]
        for i in range(1, self.end+1):
            height = self.list[i-1] * self.dim[1]/self.end
            height_unit = self.dim[1]/self.end
            x = self.coords[0] + (i-1)*self.dim[0]/self.end
            self.array_group.add(ArrayElement((x,y), (width, height), self.visited, self.list, height_unit, i-1))
            #print("{},{}  {},{}".format(x, y, width, height))

    def getList(self):
        return self.list

    # TODO: As part of the challenge, code ur own shuffle method
    def shuffle(self):
        random.shuffle(self.list)

    def get(self, index):
        self.visited[index] = True
        time.sleep(self.delay)
        return self.list[index]

    def replace(self, index, val):
        self.visited[index] = True
        time.sleep(self.delay)
        self.list[index] = val
    
    def swap(self, ind1, ind2):
        if (ind1 == ind2):
            return
        self.visited[ind1] = True
        self.visited[ind2] = True
        time.sleep(self.delay)
        temp = self.list[ind1]
        self.list[ind1] = self.list[ind2]
        self.list[ind2] = temp

    def length(self):
        return len(self.list)

    def reset(self):
        self.list = []
        self.visited = []
        for i in range(1, self.end+1):
            self.list.append(i)
            self.visited.append(False)
        self.array_group.empty()
        self.createList()