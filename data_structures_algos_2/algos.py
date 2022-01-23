from csv_reader import adjacency_matrix
from data_structs import HashTable


# Given a list, this will calculate nearest neighbor of each element in list.
# current vertex is given to begin algorithm, can be in list or not (curr vertex is generally hub) -> n^2)
def nearest_neighbor(curr_vertex, _list_):
    adj_matrix = adjacency_matrix()
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


def map_direction():
    adj_matrix = adjacency_matrix()
    maximum = -1
    north = None
    south = None
    midpoint = None
    map_direction_lookup = HashTable()
    for i in adj_matrix.keys():
        for j in adj_matrix.keys():
            if adj_matrix[i][j] > maximum:
                maximum = adj_matrix[i][j]
                north = j
                south = i
    minimum = 2 ** 32
    mid = maximum / 2
    skip = [north, south]
    if north and south:
        for v in adj_matrix.keys():
            if v not in skip:
                sum_dist = adj_matrix[v][north] + adj_matrix[v][south]
                avg_dist = sum_dist / 2
                dif_dist = abs(avg_dist - mid)
                if dif_dist < minimum:
                    minimum = dif_dist
                    midpoint = v
        skip.append(midpoint)
        map_direction_lookup.add(north, 'North')
        map_direction_lookup.add(south, 'South')
    if map_direction_lookup:
        for v in adj_matrix.keys():
            if v not in skip:
                if adj_matrix[north][v] <= adj_matrix[north][midpoint]:
                    map_direction_lookup.add(v, 'North')
                else:
                    map_direction_lookup.add(v, 'South')
        if adj_matrix[north][midpoint] < adj_matrix[south][midpoint]:
            map_direction_lookup.add(midpoint, 'North')
        else:
            map_direction_lookup.add(midpoint, 'South')

    return map_direction_lookup
