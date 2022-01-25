from csv_reader import get_package_info


# All package information stored in a hash table in self.info of the class --> O(n)
# Additional class variables Vertex and status times: at_hub,en_route,delivered
class Package:
    def __init__(self, package_id):
        self.info = get_package_info(package_id)
        self.vertex = int(self.info['vertex'])
        self.at_hub = None
        self.en_route = None
        self.delivered = None

    # return package as string example 'Package: 1' --> O(1)
    def __str__(self):
        return str('Package: ' + self.info['package ID number'])
