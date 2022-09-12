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
            # TODO: Sometimes crashes due to null pointer, seems to happen when you are sorting then you press "advanced"
            dim[1] = self.list[self.index] * self.height_unit
            assert self.list[self.index] >= 0

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
       beg = the minimum possible value of the array 
       end = the maximum possible value of the array
    '''
    default_delay = 0.001
    default_size = 256
    def __init__(self, array_group, dim, coords, beg, end, midi, delay = default_delay, size = default_size):
        self.array_group = array_group
        self.list = []
        self.visited = []
        for i in range(1, size+1):
            self.list.append(i)
            self.visited.append(False)
        self.dim = dim
        self.coords = coords
        self.beg = beg
        self.end = end
        self.delay = delay
        self.midi = midi
        self.size = size
        self.createList()
        
    def change_delay(self, delay):
        try:
            self.delay = float(delay)
        # TODO: figure out how to get rid of magic numbers using static constants idk python weird
        except ValueError:
            self.delay = 0.001
        return self.delay

    def change_size(self, size):
        try:
            self.size = int(size)
            self.beg = 1
            self.end = int(size)
        # TODO: figure out how to get rid of magic numbers using static constants idk python weird
        except ValueError:
            self.size = 256
            self.beg = 1
            self.end = 256
        self.reset()
        return self.size

    def createList(self):
        width = self.dim[0]/len(self.list)
        y = self.coords[1] + self.dim[1]
        height_unit = self.dim[1] / (self.end - self.beg + 1)

        for i in range(1, len(self.list)+1):
            height = (self.list[i-1] - self.beg + 1) * self.dim[1] / (self.end - self.beg + 1)
            x = self.coords[0] + (i-1)*self.dim[0]/len(self.list)
            self.array_group.add(ArrayElement((x,y), (width, height), self.visited, self.list, height_unit, i-1))
            #print("{},{}  {},{}".format(x, y, width, height))

    # TODO: Get rid of size parameter
    def setList(self, size, beg, end):
        self.list = []
        self.visited = []
        self.array_group.empty()
        self.beg = beg
        self.end = end
        for i in range(0, size):
            self.visited.append(False)
            self.list.append(0)
        self.createList()

    def getList(self):
        return self.list

    # TODO: As part of the challenge, code ur own shuffle method
    def shuffle(self):
        random.shuffle(self.list)

    def generate(self):
        self.array_group.empty()
        self.list = []
        self.visited = []
        for i in range(self.size):
            self.list.append(random.randint(self.beg, self.end))
            self.visited.append(False)
        self.createList()

    def play(self, index):
        self.midi.play(int((self.list[index] - self.beg + 1)/(self.end - self.beg + 1)*127))


    def get(self, index):
        self.visited[index] = True
        self.play(index)
        time.sleep(self.delay)
        return self.list[index]

    def replace(self, index, val):
        self.visited[index] = True
        self.play(index)
        time.sleep(self.delay)
        self.list[index] = val
    
    def insert(self, index, val):
        self.list.insert(index, val)
        self.visited.insert(index, True)
        self.array_group.empty()
        self.createList()
        self.play(index)
        time.sleep(self.delay)

    def remove(self, index):
        self.visited[index] = True
        self.play(index)
        time.sleep(self.delay)
        self.array_group.empty()
        del self.list[index]
        self.createList()

    def swap(self, ind1, ind2):
        if (ind1 == ind2):
            return
        self.visited[ind1] = True
        self.visited[ind2] = True
        self.play(ind1)
        self.play(ind2)
        time.sleep(self.delay)
        temp = self.list[ind1]
        self.list[ind1] = self.list[ind2]
        self.list[ind2] = temp

    def length(self):
        return len(self.list)

    def reset(self):
        self.list = []
        self.visited = []
        cnt = 0
        while (cnt < self.size):
            for i in range(self.beg, self.end+1):
                self.list.append(i)
                self.visited.append(False)
                cnt += 1
                if (cnt == self.size):
                    break

        self.array_group.empty()
        self.createList()
    '''
    def reverse(self):
        self.list = []
        self.visited = []
        for i in range(1, self.size+1):
            self.list.append(self.end - i + 1)
            self.visited.append(False)
        self.array_group.empty()
        self.createList()
    '''
    def change(self, dim, coords):
        self.array_group.empty()
        self.dim = dim
        self.coords = coords
        self.list = []
        self.visited = []
        for i in range(1, self.end+1):
            self.list.append(i)
            self.visited.append(False)
        self.createList()

    def kill(self):
        self.array_group.empty()
        del self
