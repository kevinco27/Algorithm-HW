
class Node():
    def __init__(self, value, parent, color, left=None, right=None):
        self.parent = parent
        self.left = left
        self.right = right
        self.value = value
        self.color = color

    def __iter__(self):
        if self.left.color != "nil":
            yield from self.left.__iter__()

        yield self.value

        if self.right.color != "nil":
            yield from self.right.__iter__()


class BRTree():
    def __init__(self):
        self.NIL = Node(None, None, 'nil')
        self.root = self.NIL

    def __iter__(self):
        if self.root.color == self.NIL:
            return list()
        yield from self.root.__iter__()

    def insert(self, value):
        new_node = Node(value, None, 'red', left=self.NIL, right=self.NIL)
        y = self.NIL
        x = self.root
        while x != self.NIL:
            y = x
            if new_node.value < x.value:
                x = x.left
            else:
                x = x.right
        new_node.parent = y
        if y == self.NIL:
            self.root = new_node
        elif new_node.value < y.value:
            y.left = new_node
        else:
            y.right = new_node
        self._INSERT_FIXUP(new_node)

    def delete(self, value):
        pass

    def _INSERT_FIXUP(self, z):
        while z.parent.color == "red":
            if z.parent == z.parent.parent.left:
                y = z.parent.parent.right
                if y.color == "red":
                    z.parent.color = "black"
                    y.color = "black"
                    z.parent.parent.color = "red"
                    z = z.parent.parent
                else:
                    if z == z.parent.right:
                        z = z.parent                      # case2
                        self._LEFT_ROTATE(z)              # case2 -> case3
                    z.parent.color = "black"              # case3
                    z.parent.parent.color = "red"         # case3
                    self._RIGHT_ROTATE(z.parent.parent)   # case3
            elif z.parent == z.parent.parent.right:
                y = z.parent.parent.right
                if y.color == "red":
                    z.parent.color = "black"
                    y.color = "black"
                    z.parent.parent.color = "red"
                    z = z.parent.parent
                else:
                    if z == z.parent.right:
                        z = z.parent                      # case2
                        self._LEFT_ROTATE(z)              # case2 -> case3
                    z.parent.color = "black"              # case3
                    z.parent.parent.color = "red"         # case3
                    self._RIGHT_ROTATE(z.parent.parent)   # case3
        self.root.color = "black"

    def _LEFT_ROTATE(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.NIL:
            y.left.parent = x
        y.parent = x.parent
        if x.parent == self.NIL:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def _RIGHT_ROTATE(self, y):
        x = y.left
        y.left = x.right
        if x.right != self.NIL:
            x.right.parent = y
        x.parent = y.parent
        if y.parent == self.NIL:
            self.root = x
        elif y == y.parent.left:
            y.parent.left = x
        else:
            y.parent.right = x
        x.right = y
        y.parent = x
