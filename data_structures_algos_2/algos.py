from csv_reader import adjacency_matrix
from data_structs import HashTable

'''For every package in the input list:
Check the distance from package’s vertex to the current vertex. If it is less than nearest distance. 
Set package as nearest package.
Once all items in list have been checked, the nearest package will be found.
Pop the nearest package from the input list.
Append the nearest package as the next package in the nearest neighbor list.
Update the current vertex. Repeat process until only one package remains in input list.
If the length of the input list is 1, pop remaining package off input,
 append as next package in the nearest neighbor list and return the nearest neighbor sorted list.-> O(n^2)
'''


def nearest_neighbor(curr_vertex, adj_matrix, _list_):
    nearest_n_list = []
    while _list_:
        if len(_list_) == 1:
            nearest_n_list.append(_list_.pop(0))
            return nearest_n_list
        nearest_dist = 2 ** 32
        nearest_package = None
        for pkg in _list_:
            if adj_matrix[curr_vertex][pkg.vertex] < nearest_dist:
                nearest_dist = adj_matrix[curr_vertex][pkg.vertex]
                nearest_package = pkg
        if nearest_package:
            _next_ = _list_.pop(_list_.index(nearest_package))
            nearest_n_list.append(_next_)
            curr_vertex = nearest_package.vertex
        else:
            break
    return _list_


'''For all distances between vertices, find the two vertices with the greatest distance.
Set the first vertex to North and the other South (Not literal, simplified attribute name).
Find the midpoint (average distance that splits the North and South vertices).
Add North and South to the hash table with their respective classification: ‘North’, ‘South’.
For each vertex (excluding North, South) if the distance between North and Vertex is less than the midpoint,
 classify vertex as ‘North’, Else classify the vertex as ‘South’.
Return the map direction lookup hash table with classified vertices. # -> O(n^2)
'''


def map_direction():
    adj_matrix = adjacency_matrix()
    maximum = -1
    north = None
    south = None
    map_direction_lookup = HashTable()
    for i in adj_matrix.keys():
        for j in adj_matrix.keys():
            if adj_matrix[i][j] > maximum:
                maximum = adj_matrix[i][j]
                north = j
                south = i
    mid = maximum / 2
    skip = [north, south]
    map_direction_lookup.add(north, 'North')
    map_direction_lookup.add(south, 'South')
    if map_direction_lookup:
        for v in adj_matrix.keys():
            if v not in skip:
                if adj_matrix[north][v] <= mid:
                    map_direction_lookup.add(v, 'North')
                else:
                    map_direction_lookup.add(v, 'South')

    return map_direction_lookup
