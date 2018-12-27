
class Node():
    def __init__(self, value, parent, color, left=None, right=None, is_nil=False):
        self.parent = parent
        self.left = left
        self.right = right
        self.value = value
        self.color = color
        self.is_nil = is_nil

    def __iter__(self):
        if self.left.is_nil is False:
            yield from self.left.__iter__()

        yield self, self.value

        if self.right.is_nil is False:
            yield from self.right.__iter__()


class BRTree():
    def __init__(self):
        self.BLACK = 'black'
        self.RED = 'red'
        self.NIL = Node(None, None, self.BLACK, is_nil=True)
        self.root = self.NIL

    def __iter__(self):
        if self.root == self.NIL:
            return list()
        yield from self.root.__iter__()

    def insert(self, value):
        new_node = Node(value, None, self.RED, left=self.NIL, right=self.NIL)
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
        z = self._SEARCH(value)
        if z is None:
            print('The value to be deleted not exists in the tree !')
            return
        y = z
        y_origin_color = y.color

        if z.left == self.NIL:
            x = z.right
            self._RB_TRANSPLANT(z, z.right)
        elif z.right == self.NIL:
            x = z.left
            self._RB_TRANSPLANT(z, z.left)
        else:
            y, _ = self._TREE_MINIMUM(z.right)
            y_origin_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self._RB_TRANSPLANT(y, y.right)
                y.right = z.right
                y.right.parent = y
            self._RB_TRANSPLANT(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
        if y_origin_color == self.BLACK:
            self._DELETE_FIXUP(x)

    def _INSERT_FIXUP(self, z):
        while z.parent.color == self.RED:
            if z.parent == z.parent.parent.left:
                y = z.parent.parent.right
                if y.color == self.RED:
                    z.parent.color = self.BLACK
                    y.color = self.BLACK
                    z.parent.parent.color = self.RED
                    z = z.parent.parent
                else:
                    if z == z.parent.right:
                        z = z.parent                      # case2
                        self._LEFT_ROTATE(z)              # case2 -> case3
                    z.parent.color = self.BLACK              # case3
                    z.parent.parent.color = self.RED         # case3
                    self._RIGHT_ROTATE(z.parent.parent)   # case3
            elif z.parent == z.parent.parent.right:
                y = z.parent.parent.left
                if y.color == self.RED:
                    z.parent.color = self.BLACK
                    y.color = self.BLACK
                    z.parent.parent.color = self.RED
                    z = z.parent.parent
                else:
                    if z == z.parent.left:
                        z = z.parent                      # case2
                        self._RIGHT_ROTATE(z)              # case2 -> case3
                    z.parent.color = self.BLACK             # case3
                    z.parent.parent.color = self.RED         # case3
                    self._LEFT_ROTATE(z.parent.parent)   # case3
        self.root.color = self.BLACK

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

    def _RB_TRANSPLANT(self, u, v):
        if u.parent == self.NIL:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def _SEARCH(self, value):
        z = None
        for node, val in self:
            if val == value:
                z = node
        return z

    def _TREE_MINIMUM(self, z):
        while z.left != self.NIL:
            z = z.left
        return z, z.value

    def _DELETE_FIXUP(self, x):
        while x != self.root and x.color == self.BLACK:
            if x == x.parent.left:
                w = x.parent.right
                if w.color == self.RED:
                    w.color = self.BLACK                                   # case 1
                    x.parent.color = self.RED                              # case 1
                    self._LEFT_ROTATE(x.parent)                         # case 1
                    w = x.parent.right                                  # case 1
                else:
                    if w.left.color == self.BLACK and w.right.color == self.BLACK:
                        w.color = self.RED                                 # case 2
                        x = x.parent                                    # case 2
                    else:
                        if w.right.color == self.BLACK:
                            w.left.color = self.BLACK                      # case 3
                            w.color = self.RED                             # case 3
                            self._RIGHT_ROTATE(w)                       # case 3
                            w = x.parent.right                          # case 3
                        w.color = x.parent.color                        # case 4
                        x.parent.color = self.BLACK                        # case 4
                        w.right.color = self.BLACK                         # case 4
                        self._LEFT_ROTATE(x.parent)                     # case 4
                        x = self.root                                   # case 4
            elif x == x.parent.right:
                w = x.parent.left
                if w.color == self.RED:
                    w.color = self.BLACK                                   # case 1
                    x.parent.color = self.RED                              # case 1
                    self._RIGHT_ROTATE(x.parent)                         # case 1
                    w = x.parent.left                                  # case 1
                else:
                    if w.left.color == self.BLACK and w.right.color == self.BLACK:
                        w.color = self.RED                                 # case 2
                        x = x.parent                                    # case 2
                    else:
                        if w.left.color == self.BLACK:
                            w.right.color = self.BLACK                          # case 3
                            w.color = self.RED                                 # case 3
                            self._LEFT_ROTATE(w)                           # case 3
                            w = x.parent.left                              # case 3
                        w.color = x.parent.color                            # case 4
                        x.parent.color = self.BLACK                            # case 4
                        w.left.color = self.BLACK                             # case 4
                        self._RIGHT_ROTATE(x.parent)                         # case 4
                        x = self.root
        x.color = self.BLACK
