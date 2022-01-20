import csv_reader


class Package:
    def __init__(self, package_id):
        self.info = csv_reader.get_package_info(package_id)
        self.vertex = int(self.info['vertex'])
        self.at_hub = None
        self.en_route = None
        self.delivered = None

    def __str__(self):
        return str('Package: ' + self.info['package ID number'])
