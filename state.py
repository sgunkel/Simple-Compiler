#
# Seth Gunkel
#

class state:
    def __init__(self, prev):
        self.prev = prev
        self.objs = {} # name : obj
    def isParent(self):
        return (self.prev == None)
    def getByName(self, name):
        if name in self.objs:
            return self.objs[name]
        elif self.isParent():
            # error
            return None
        return self.prec.getByName(name)
    def add(self, name, obj):
        self.objs[name] = obj



