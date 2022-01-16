from data_structs.hash_table import HashTable


class Package:
    def __init__(self):
        info_components = ['package ID number',
                           'delivery address',
                           'delivery deadline',
                           'delivery city',
                           'package weight',
                           'delivery status']
        self.distance = HashTable()
        self.info = HashTable()

        for component in info_components:
            self.info.add(component, None)
