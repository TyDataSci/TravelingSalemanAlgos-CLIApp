from csv_reader import adjacency_matrix


def nearest_neighbor(curr_vertex, _list_):
    dict_of_dict = adjacency_matrix()
    nearest_n_list = []

    while _list_:
        if len(_list_) == 1:
            nearest_n_list.append(_list_.pop(0))
            return nearest_n_list
        nearest_dist = 2 ** 32
        for pkg in _list_:
            if dict_of_dict[curr_vertex][pkg.vertex] < nearest_dist:
                nearest_dist = dict_of_dict[curr_vertex][pkg.vertex]
                nearest_package = pkg
                nearest_vertex = pkg.vertex
        _next_ = _list_.pop(_list_.index(nearest_package))
        nearest_n_list.append(_next_)
        curr_vertex = nearest_vertex


def map_direction():
    dict_dict = adjacency_matrix()
    maximum = -1
    for i in dict_dict.keys():
        for j in dict_dict.keys():
            if dict_dict[i][j] > maximum:
                maximum = dict_dict[i][j]
                north = j
                south = i
    minimum = 2 ** 32
    mid = maximum / 2
    skip = [north, south]
    for v in dict_dict.keys():
        if v not in skip:
            sum_dist = dict_dict[v][north] + dict_dict[v][south]
            avg_dist = sum_dist / 2
            dif_dist = abs(avg_dist - mid)
            if dif_dist < minimum:
                minimum = dif_dist
                midpoint = v
    skip.append(midpoint)
    north_bound = [north]
    south_bound = [south]
    for v in dict_dict.keys():
        if v not in skip:
            if dict_dict[north][v] <= dict_dict[north][midpoint]:
                north_bound.append(v)
            else:
                south_bound.append(v)
    if dict_dict[north][midpoint] < dict_dict[south][midpoint]:
        north_bound.append(midpoint)
    else:
        south_bound.append(midpoint)

    return north_bound, south_bound
