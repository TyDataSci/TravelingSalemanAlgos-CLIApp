def nearest_neighbor(curr_vertex, adj_matrix, _list_):
    insert_index = 0
    while True:
        if insert_index == len(_list_)-1:
            return _list_
        nearest_dist = 2**32
        for i in _list_[insert_index:]:
            if adj_matrix.loc[i, curr_vertex] < nearest_dist:
                nearest_dist = adj_matrix.loc[i,curr_vertex]
                nearest_vertex = i
        _list_.insert(insert_index,_list_.pop(_list_.index(nearest_vertex)))
        curr_vertex = nearest_vertex
        insert_index +=1
        #print(curr_vertex,'\n',insert_index)