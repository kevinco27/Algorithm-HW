from BlackRed_Tree import BRTree

input_path = "./input.txt"


def main():
    brtree = BRTree()
    with open(input_path) as f:
        num_oper = int(f.readline())
        for i in range(num_oper):
            oper = f.readline().strip('\n')
            values = [int(v) for v in f.readline().split(' ')]
            if oper == '1':
                for val in values:
                    brtree.insert(int(val))
            elif oper == '2':
                for val in values:
                    brtree.delete(int(val))
            
            for node in brtree:
                print(node)
                

if __name__ == '__main__':
    main()
