#
# Seth Gunkel
#

import os

def printByColor(_str, color):
    code = 0
    if color == "blue":
        code = 96
    else:
        code = 92
    print("\033[{0}m{1}\033[0m".format(code, _str), end="")

def scan(path):
    for fname in os.listdir(path):
        if fname in [ '.', '..', "runTests.py" ]:
            continue
        f = os.path.join(path, fname)
        if os.path.isfile(f):
            if f.endswith("Tests.py"):
                printByColor(fname, "blue")
                printByColor(" [Done]", "green")
                print()
                os.system("python {}".format(fname))
        else:
            scan(f)

scan('./')
