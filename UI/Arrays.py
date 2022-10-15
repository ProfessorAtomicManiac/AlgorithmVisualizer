import random
import time

import pygame
import random
import UI.Wrapper as Wrapper

class ArrayElement(pygame.sprite.Sprite):

    ''' Creates an element of our special array
        @coords = coordinates of where the bottom-left of the element will be placed
        @dim = dimensions of the element
        @visited = needed to check whether some array index is being accessed/swapped (boolean array)
        @list = needed to check if element was swapped and should update the swappage (regular integer array)
        @height_unit = unit to help determine height of the array element
    '''
    def __init__(self, coords, dim, visited, list, height_unit, index, beg):
        super().__init__()
        self.image = pygame.Surface(dim)
        self.color = Wrapper.Colors.WHITE
        self.rect = self.image.get_rect(bottomleft = coords)
        self.coords = coords
        self.dim = dim
        self.image.fill(self.color)
        self.visited = visited
        self.list = list
        self.height_unit = height_unit
        self.index = index
        self.val = list[index]
        self.beg = beg

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
            try:
                dim[1] = (self.list[self.index] - self.beg) * self.height_unit
            except TypeError:
                return
            assert (self.list[self.index] - self.beg) >= 0

            self.val = self.list[self.index]
            self.dim = tuple(dim)
            

    def change_color(self):
        if (self.visited[self.index]):
            #print("index is visited")
            self.still_colored = True
            self.color = Wrapper.Colors.RED
            self.visited[self.index] = False
        
        if (self.still_colored):
            self.timer += 0.1
            if (self.timer > 0.1):
                #print("Index is unvisited")
                self.still_colored = False
                self.color = Wrapper.Colors.WHITE
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
        self.dim = dim
        self.coords = coords
        self.beg = beg
        self.end = end
        self.delay = delay
        self.midi = midi
        self.size = size
        self.reset()

        self.saved_config = [size, beg, end]
        self.saved_list = [i for i in range(1, self.end+1)]

        self.access = 0
        self.swaps = 0
        self.changes = 0
        
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

    def save_config(self, config, arr):
        self.saved_config = config
        self.saved_list = arr

    def change_array(self, beg, end, size, arr = None):
        try:
            self.size = int(size)
            self.beg = int(beg)
            self.end = int(end)
        except ValueError:
            self.size = 256
            self.beg = 1
            self.end = 256
        self.save_config([size, beg, end], arr)
        self.reset(arr)

    def load_config(self):
        self.array_group.empty()

        self.list = self.saved_list
        self.visited = []
        cnt = 0
        #print(self.size, len(self.list))
        while (cnt < self.size):
            # TODO: Unexpected behavior may occur if user puts in invalid array such as not having enough elements or saved_list's size is 0
            for i in range(0, len(self.list)):
                self.visited.append(False)
                cnt += 1
                if (cnt == self.size):
                    break
        self.createList()

    def createList(self):
        self.access = 0
        self.swaps = 0
        self.changes = 0
        width = self.dim[0]/len(self.list)
        y = self.coords[1] + self.dim[1]
        height_unit = self.dim[1] / (self.end - self.beg)
        for i in range(1, len(self.list)+1):
            height = (self.list[i-1] - self.beg) * height_unit
            x = self.coords[0] + (i-1) * width
            self.array_group.add(ArrayElement((x,y), (width, height), self.visited, self.list, height_unit, i-1, self.beg))
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
            self.list.append(beg)
        self.createList()

    def getList(self):
        return self.list

    # TODO: As part of the challenge, code ur own shuffle method
    def shuffle(self):
        random.shuffle(self.list)
        self.access = 0
        self.swaps = 0
        self.changes = 0

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
        self.access += 1
        self.visited[index] = True
        self.play(index)
        time.sleep(self.delay)
        return self.list[index]

    def replace(self, index, val):
        self.access += 1
        self.changes += 1
        self.visited[index] = True
        self.play(index)
        time.sleep(self.delay)
        self.list[index] = val
    
    # No sorting algos actually use these, probably initialization
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
        self.access += 2
        self.changes += 2
        self.swaps += 1
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

    def reset(self, list = None):
        self.array_group.empty()

        self.list = []
        if (list != None):
            self.list = list
        self.visited = []
        cnt = 0
        #print(self.size, len(self.list))
        while (cnt < self.size):
            if (list == None):
                for i in range(self.beg, self.end+1):
                    self.list.append(i)
                    self.visited.append(False)
                    cnt += 1
                    if (cnt == self.size):
                        break
            # TODO: Unexpected behavior may occur if user puts in invalid array such as not having enough elements
            else:
                self.list = list
                for i in range(0, len(self.list)):
                    self.visited.append(False)
                    cnt += 1
                    if (cnt == self.size):
                        break
        self.createList()
    
    def reverse(self, list = None):
        self.array_group.empty()

        self.list = []
        if (list != None):
            self.list = list
        self.visited = []
        cnt = 0
        while (cnt < self.size):
            if (list == None):
                for i in range(self.end, self.beg - 1, -1):
                    self.list.append(i)
                    self.visited.append(False)
                    cnt += 1
                    if (cnt == self.size):
                        break
            # TODO: Unexpected behavior may occur if user puts in invalid array such as not having enough elements
            else:
                self.list = list
                for i in range(0, len(self.list)):
                    self.visited.append(False)
                    cnt += 1
                    if (cnt == self.size):
                        break

        self.createList()
    
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
