def selection_sort(arr, event):
    for i in range(0, arr.length()):
        min = i
        for j in range(i+1, arr.length()):
            if arr.get(j) < arr.get(min):
                min = j
                if (event.is_set()):
                    return
        arr.swap(i, min)

def quick_sort(arr, event, begin, end):
    if (begin < end):
        pivot = end-1
        low = begin

        for i in range(begin, end):
            if arr.get(i) < arr.get(pivot):
                arr.swap(i, low)
                low += 1
                if (event.is_set()):
                    return

        arr.swap(low, pivot)
        quick_sort(arr, event, begin, low)
        quick_sort(arr, event, low+1, end)

def merge_sort(arr, event, begin, end):
    if (begin+1 < end):
        mid = begin + ((end-begin)+1)//2
        merge_sort(arr, event, begin, mid)
        merge_sort(arr, event, mid, end)
        arrL = arr.list[begin:mid]
        arrR = arr.list[mid:end]
        i = j = 0
        k = begin
        while (i < len(arrL) and j < len(arrR)):
            if arrL[i] < arrR[j]:
                arr.replace(k, arrL[i])
                i += 1
            else:
                arr.replace(k, arrR[j])
                j += 1
            k += 1

        while i < len(arrL):
            arr.replace(k, arrL[i])
            i += 1
            k += 1
        while j < len(arrR):
            arr.replace(k, arrR[j])
            j += 1
            k += 1

class Heap():

    def __init__(self, arr, event):
        self.heap = []
        self.arr = arr
        self.event = event

    def size(self):
        return len(self.heap)

    def isEmpty(self):
        return self.size() == 0

    def insert(self, val):
        # Upheap
        self.heap.append(val)

        self.arr.replace(self.size()-1, val)
        n = self.size()-1
        while (n != 0 and val > self.heap[(n-1)//2]):

            self.arr.get((n-1)//2)
            self.swap((n-1)//2, n)
            n = (n-1)//2

            if (self.event.is_set()):
                return
        
    def removeMax(self):
        if (self.isEmpty()):
            return None

        self.swap(0, self.size()-1)
        val = self.heap.pop(self.size()-1)
        self.arr.get(self.size()-1)

        # Downheap
        n = 0
        while (self.size() != 0):
            temp = n
            # If there exists two children
            if (2*n+2 < self.size()):
                # If left child is smaller than right child
                self.arr.get(2 * n + 1)
                self.arr.get(2 * n + 2)
                self.arr.get(n)
                if (self.heap[2 * n + 1] > self.heap[2 * n + 2]):
                    if (self.heap[n] < self.heap[2 * n + 1]):
                        self.swap(n, (2 * n + 1))
                        n = 2 * n + 1
                # If left child is equal to or greater than right child
                else:
                    if (2*n+2 < self.size()):
                        if (self.heap[n] < self.heap[2*n+2]):
                            self.swap(n, (2 * n + 2))
                            n = 2 * n + 2
            # If there only exists a left child
            elif (2*n+1 < self.size()):
                # If left child is smaller than parent
                self.arr.get(2 * n + 1)
                self.arr.get(n)
                if (self.heap[n] < self.heap[2 * n + 1]):
                    self.swap(n, (2 * n + 1))
                    n = 2 * n + 1
            # If all its children are bigger
            if (temp == n):
                break

            if (self.event.is_set()):
                return
        return val

    def swap(self, a, b):
        temp = self.heap[a]
        self.heap[a] = self.heap[b]
        self.heap[b] = temp
        self.arr.swap(a, b)

def heap_sort(arr, event):
    heap = Heap(arr, event)
    for i in range(0, arr.length()):
        heap.insert(arr.get(i))
        if (event.is_set()):
            return
    
    i = arr.length() - 1
    while (not heap.isEmpty()):
        arr.replace(i, heap.removeMax())
        i -= 1
        if (event.is_set()):
            return
