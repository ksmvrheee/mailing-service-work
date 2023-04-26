from os.path import dirname as up


file_loc = up(up(__file__))

with open(f'{file_loc}\\secret.txt', 'r') as f:
    SERVER = f.readline().split()[-1]
    PORT = int(f.readline().split()[-1])
    EMAIL = f.readline().split()[-1]
    PASSWORD = f.readline().split()[-1]

    f.close()
