from BlackRed_Tree import BRTree
import os

input_path = "./input.txt"
output_path = "./output.txt"


def main():
    brtree = BRTree()
    with open(input_path) as f:
        num_oper = int(f.readline())
        for i in range(num_oper):
            oper = f.readline().strip('\n')
            values = [int(v) for v in f.readline().split(' ')]
            if oper == '1':
                oper_text = "Insert: " + " ,".join([str(val) for val in values])
                for val in values:
                    brtree.insert(int(val))
            elif oper == '2':
                oper_text = "Delete: " + " ,".join([str(val) for val in values])
                for val in values:
                    brtree.delete(int(val))
            with open(output_path, 'a') as fout:
                fout.write(oper_text + "\n")
                for node, val in brtree:
                    key = val
                    parent = node.parent.value if node.parent.value is not None else " "
                    color = node.color
                    fout.write("key: {} parent: {} color: {} \n".format(key, parent, color))


if __name__ == '__main__':
    if os.path.exists(output_path):
        os.remove(output_path)
    main()
