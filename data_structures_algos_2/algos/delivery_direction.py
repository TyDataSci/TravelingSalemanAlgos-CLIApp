from data.csv_reader import get_adj


adj = get_adj()

grp1 = []
grp2 = []
grp3 = []


maximum = -1
for node in adj:
    for i in adj:
        if adj.loc[i,node] > maximum:
            maximum = adj.loc[i,node]
            big_dist1 = i
            big_dist2 = node
print(f'MAX {maximum} miles\n {big_dist1} --> {big_dist2}')
mid = maximum /2
group1 = 0
for i,node in enumerate(adj):
    if adj.loc[0,node] > mid:
        group1 +=1
        print(f'Group 1 :{group1}: start ->{node} distance: {adj.loc[0,node]}')
        grp1.append(adj.pop(node))
print(f'MID {mid} miles')
mid2 = mid/2
group2 = 0
for i,node in enumerate(adj):
    if adj.loc[0,node] > mid2:
        group2 +=1
        print(f'Group 2 :{group2}: start ->{node} distance: {adj.loc[0,node]}')
        grp2.append(adj.pop(node))
print(f'MID2 {mid2} miles')
mid3 = mid/4
group3 = 0
for i,node in enumerate(adj):
    if adj.loc[0,node] != 0:
        group3 +=1
        print(f'Group 3 :{group3}: start ->{node} distance: {adj.loc[0,node]}')
        grp3.append(adj.pop(node))
print(f'MID3 {mid3} miles')
maximum = -1
for node in adj:
    for i in adj:
        if adj.loc[i,node] > maximum:
            maximum = adj.loc[i,node]
            north = i
            south = node

print(f'MAX {maximum} miles\n {north} --> {south}')
mid = maximum /2
minimum = 1000
for node in adj:
    for i in adj:
        if node == north or node == south or i == north or i == south:
            pass
        else:
            sum_dist = adj.loc[node,north] + adj.loc[node,south]
            avg_dist = sum_dist/2
            dif_dist = abs(avg_dist - mid)
            if dif_dist < minimum:
                minimum = dif_dist
                midpoint = node
print(f'Midpoint {midpoint} \n {north} --> {midpoint} \n {adj.loc[midpoint,north]}')
print(f'\n {south} --> {midpoint} \n {adj.loc[midpoint,south]}')
y1 = []
y2 = []
for node in adj:
    if node == north or node == south:
        pass
    else:
        if adj.loc[node,north] < adj.loc[midpoint,north]:
            y1.append(node)
        else:
            y2.append(node)
max_x = []
maximum = -1
for node in y1:
    sum_dist = adj.loc[node,midpoint] + adj.loc[node,north]
    if sum_dist > maximum:
        max_x.append(node)
maximum = -1
for node in y2:
    sum_dist = adj.loc[node,midpoint] + adj.loc[node,south]
    if sum_dist > maximum:
        max_x.append(node)
maximum = -1
for i in max_x:
    for j in max_x:
        if i != j:
            if adj.loc[i,j] > maximum:
                maximum = adj.loc[i,j]
                west = i
                east = j
print(west,' ',east)
north_east = []
north_west = []
south_east = []
south_west = []
east_all = []
west_all = []
for i in adj:
    opposite_coor = adj.loc[i,west]
    coor = adj.loc[i,east]
    if coor < opposite_coor:
        east_all.append(i)
    else:
        west_all.append(i)
for i in east_all:
    opposite_coor = adj.loc[i,south]
    coor = adj.loc[i,north]
    if coor < opposite_coor:
        north_east.append(i)
    else:
        south_east.append(i)
for i in west_all:
    opposite_coor = adj.loc[i,south]
    coor = adj.loc[i,north]
    if coor < opposite_coor:
        north_west.append(i)
    else:
        south_west.append(i)