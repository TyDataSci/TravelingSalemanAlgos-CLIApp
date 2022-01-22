from csv_reader import adjacency_matrix


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
    north_bound = None
    south_bound = None
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
        north_bound = [north]
        south_bound = [south]
    if north_bound and south_bound:
        for v in adj_matrix.keys():
            if v not in skip:
                if adj_matrix[north][v] <= adj_matrix[north][midpoint]:
                    north_bound.append(v)
                else:
                    south_bound.append(v)
        if adj_matrix[north][midpoint] < adj_matrix[south][midpoint]:
            north_bound.append(midpoint)
        else:
            south_bound.append(midpoint)

    return north_bound, south_bound
