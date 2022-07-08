def selection_sort(arr, event):
    for i in range(0, arr.length()):
        min = i
        for j in range(i+1, arr.length()):
            if arr.get(j) < arr.get(min):
                min = j
                if (event.is_set()):
                    return
        arr.swap(i, min)