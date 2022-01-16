import pandas as pd
from data_structs.hash_table import HashTable

file = 'WGU_package_file.csv'
df = pd.read_csv(file)
file = 'WGUPS_distance_table.csv'
df_dist = pd.read_csv(file)
df_dist['Hubs'] = df_dist['Hubs'].str.split('\\n', expand=True)[0]
df = df.loc[:, 'Package\nID':'Special Notes']
df.loc[df['Address'] == '5383 South 900 East #104', 'Address'] = '5383 S 900 East #104'
map_hubs = HashTable()
for j, hub in enumerate(df_dist['Hubs']):
    map_hubs[hub.strip()] = j
map_address = HashTable()
for i, address in enumerate(df_dist['Address']):
    map_address[i] = address
df['nodes'] = ''
node = df.pop('nodes')
df.insert(0, 'nodes', node)
nodes = []
for i in range(len(df)):
    nodes.append(map_hubs[df.loc[i, 'Address']])
df['nodes'] = nodes

for k, v in map_address:
    df_dist.rename(columns={v: k}, inplace=True)
for i in range(len(df_dist)):
    for j in range(len(df_dist)):
        if pd.isnull(df_dist.loc[i, j]):
            df_dist.loc[i, j] = df_dist.loc[j, i]
adj_matrix = df_dist.drop(columns=['Address', 'Hubs'])
adj = adj_matrix.copy()


def get_adj():
    return adj
