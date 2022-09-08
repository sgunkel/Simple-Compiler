#
# Seth Gunkel
#

import sys

def error(msg):
    print("\n" + msg, file = sys.stderr)

def report(expected, result, code = None, func = None):
    msg = ""
    if code != None:
        msg = "{}\n{}\n".format(func, code)
    msg = """Expected:
  {0}
Result:
  {1}
""".format(expected, result)
    error(msg)

