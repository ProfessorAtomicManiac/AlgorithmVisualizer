''' Will do a "glissando" up the array indexes when the array is done sorting
'''
def finish(arr):
    for i in range(0, arr.length()):
        arr.get(i)

''' Selection Sort - O(n^2)
    The algorithm will iterate through the entire array to find the minimum, then replace the lowest unsorted index with that element
    This repeats until the entire array is sorted
'''
def selection_sort(arr, event):
    for i in range(0, arr.length()):
        min = i
        for j in range(i+1, arr.length()):
            if arr.get(j) < arr.get(min):
                min = j
            if (event.is_set()):
                return
        arr.swap(i, min)
    finish(arr)

''' Inerstion Sort - O(n^2)
    For every index i from 1 to arr.length(), it will iterate backwards in the indexes of the already previously sorted array
    When it finds an element that is less than the element at index i, it will replace it
    As it iterates to find that element, it will shift all elements greater than it to the right
'''
def insertion_sort(arr, event):
    for i in range(1, arr.length()):
        key = arr.get(i)
        j = i-1
        while j >= 0 and key < arr.get(j):
            arr.replace(j+1, arr.get(j))
            j -= 1
            if (event.is_set()):
                return
        arr.replace(j+1, key)
    finish(arr)

''' Quick Sort - O(nlogn), O(n^2) if the array is sorted
    All elements in the array will be set to the left of the rightmost element if its less than the rightmost element
    Same with the right side
    This repeats until the array is sorted
'''
def quick_sort(arr, event, begin, end, isFinished = False):
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
    if isFinished:
        finish(arr)

''' Merge Sort - O(nlogn)
    The array will be split into two even parts (not exactly even if the array has an odd number of elements)
    This continues until the splitted array is of length 1
    The splitted arrays will be merged together, where the smallest elements to the biggest elements of each splitted array will be compared to each other
    and merged into a single array
    This continues until the entire array is sorted
'''
def merge_sort(arr, event, begin, end, isFinished = False):
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
            if (event.is_set()):
                return
            k += 1

        while i < len(arrL):
            arr.replace(k, arrL[i])
            i += 1
            k += 1
            if (event.is_set()):
                return
        while j < len(arrR):
            arr.replace(k, arrR[j])
            j += 1
            k += 1
            if (event.is_set()):
                return
    if (isFinished):
        finish(arr)

''' Heap Sort (nlogn) - Also the implementation of the Priority Queue using the Heap Data Structure
    All elements of the array will be inserted into what is known as a "Heap".
    A Heap is a data structure that is a special form of a binary tree that satisfies the condition that
    each node's children must be smaller than the node itself

    When an element is inserted into the heap, it will be added as the last element of the tree, in other words, it is the last leaf
    Then the algorithm will perform an "upheap" operation, where the inserted node will be compared to its parent
    If the parent is smaller than the node, the two nodes will swap.
    This process will continue until either it finds a parent that is bigger than the node, or the node becomes the root
    This operation takes O(log n) time, since we only iterate up to the root in the worst possible case, whose height is log n

    After all elements are inserted, we will remove the maximum element, which should be the root of the binary tree
    The root will be swapped with the outermost leaf of the tree, and then it will be removed.
    In order to satisfy the heap property, we must perform a "downheap" on the root, as the root is no longer tha maximum
    If either the left or right child is bigger than the node, than it will be swapped (the bigger of the children)
    This will keep going until either the node has no more children, or its children are smaller than the node
    This operation takes O(log n) time, since we only iterate down to the leaf in the worse possible case, whose height is log n

    tl;dr think of this as a more efficient "selection sort"
'''
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
    finish(arr)
    
''' Radix Sort O(d*(n+b)) - where d is the number of digits in base b, n is the number of elements, and b is the base/bucket size
    I don't feel like typing an explanation just know it has to do with sorting each digit
    If you want something cool, make the array size big
    you can do that on line 126 in UI.py. I will eventually add it to the UI don't worry
'''
def radix_sort(arr, event):
    maxValue = 0
    for i in range(arr.length()):
        if (arr.get(i) > maxValue):
            maxValue = arr.get(i)

    # We assume that the digits are > 0 for doubles
    maxDigit = 1
    digitValue = 10
    while (maxValue // digitValue > 0):
        digitValue*=10
        maxDigit += 1
        if (event.is_set()):
            return

    for i in range(maxDigit):
        bucketSort(arr, event, i)
        if (event.is_set()):
            return
    finish(arr)

# Does consider negative numbers
def bucketSort(arr, event, digit):
    # Range is [-9, 9]
    length = 19
    buckets = []
    for i in range(length):
        buckets.append([])
        
    
    for i in range(arr.length()):
        buckets[int(getDigit(arr.get(i), digit) + 9)].append(arr.get(i))
        if (event.is_set()):
            return

    index = 0
    for bucket in buckets:
        for num in bucket:
            arr.replace(index, num)
            index += 1
            if (event.is_set()):
                return

    return arr

def getDigit(num, digit):
    # 0 is units digit, 1 is tens digit, etc
    if (digit == 0):
        return num % (10*(digit+1))
    else:
        digitValue = 1
        for i in range(digit):
            digitValue *= 10
        return (num/(digitValue))%(10)

''' Counting Sort - O(n + k)
    min = smallest element in arr
    max = biggest element in arr
'''
def counting_sort(arr, event, min, max):
    count = []
    ans = []
    for i in range(min, max + 1):
        count.append(0)
        if (event.is_set()):
            return
    
    for i in range(arr.length()):
        count[arr.get(i) - min] += 1
        ans.append(0)
        if (event.is_set()):
            return

    for i in range(arr.length()):
        count[i] += count[i-1]
        if (event.is_set()):
            return
    count.insert(0, 0)
    count.pop(len(count) - 1)

    for i in range(arr.length()-1, -1, -1):
        ans[count[arr.get(i)] - 1] = arr.get(i)
        count[arr.get(i)] -= 1
        if (event.is_set()):
            return

    for i in range(arr.length()):
        arr.replace(i, ans[i])
        if (event.is_set()):
            return

    finish(arr)