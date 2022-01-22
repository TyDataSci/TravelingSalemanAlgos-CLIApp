import csv
from data_structs import HashTable

package_file = 'data/WGU_package_file.csv'
distance_file = 'data/WGUPS_distance_table.csv'


def get_vertices():
    vertices = []
    import csv
    with open(distance_file) as f:
        spam = csv.DictReader(f)
        for row in spam:
            vertices.append(row['vertex'])

    return vertices


def adjacency_matrix():
    vertices = get_vertices()
    dict_of_dict = {}
    for i in range(len(vertices)):
        single_dict = {}
        with open(distance_file) as f:
            spam = csv.DictReader(f)
            for row in spam:
                single_dict[int(row['vertex'])] = float(row[str(i)])
        dict_of_dict[i] = single_dict

    return dict_of_dict


def get_package_ids():
    ids = []
    with open(package_file) as f:
        spam = csv.DictReader(f)
        for row in spam:
            ids.append(row['package ID number'])

    return ids


def get_package_info(package_id):
    package_info = HashTable()
    with open(package_file) as f:
        spam = csv.DictReader(f)
        headers = spam.fieldnames
        for row in spam:
            if row['package ID number'] == package_id:
                for field in headers:
                    package_info.add(field, row[field])
                package_info.add('delivery status', 'at hub')
                package_info.add('trip', None)

    return package_info
