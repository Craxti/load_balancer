class VPSList:
    def load_from_file(self, filename):
        vps_list = []

        with open(filename, 'r') as file:
            vps_list = [line.strip() for line in file]

        return vps_list

