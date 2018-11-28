import os
import math
import numpy as np


def bubbleUp(table, row, col):
    if row == 0 and col == 0:
        pass
    else:
        lf_ele_row = row
        lf_ele_col = col-1
        above_ele_row = row-1
        above_ele_col = col
        if row == 0:
            # only go leftward
            ele_val = np.array(
                        [table[row][col],
                        table[lf_ele_row][lf_ele_col]
                        ])
            ele_idx = np.array(
                        [[row, col], 
                        [lf_ele_row, lf_ele_col]
                        ])
        elif col == 0:
            # only go upward
            ele_val = np.array(
                        [table[row][col],
                        table[above_ele_row][above_ele_col]
                        ])
            ele_idx = np.array(
                        [[row, col], 
                        [above_ele_row, above_ele_col]
                        ])
        else:
            # either go leftward or upward
            ele_val = np.array(
                        [table[row][col],
                        table[lf_ele_row][lf_ele_col],
                        table[above_ele_row][above_ele_col]
                        ])
            ele_idx = np.array(
                        [[row, col], 
                        [lf_ele_row, lf_ele_col], 
                        [above_ele_row, above_ele_col]
                        ])
        # find max value among three elements
        max_idx = ele_idx[np.argmax(ele_val)]
        max_row = max_idx[0]
        max_col = max_idx[1]
        # swap max element with current element
        if max_row!=row or max_col!=col:
            tmp = table[row][col]
            table[row][col] = table[max_row][max_col]
            table[max_row][max_col] = tmp
            bubbleUp(table, max_row, max_col)


def bubbleDown(table, row, col):
    row_size = table.shape[0]-1
    col_size = table.shape[1]-1

    if row == row_size and col == col_size:
        pass
    else:
        r_ele_row = row
        r_ele_col = col+1
        below_ele_row = row+1
        below_ele_col = col
        if row == row_size:
            # only go rightward
            ele_val = np.array(
                        [table[row][col],
                        table[r_ele_row][r_ele_col]
                        ])
            ele_idx = np.array(
                        [[row, col], 
                        [r_ele_row, r_ele_col]
                        ])

        elif col == col_size:
            # only go downward
            ele_val = np.array(
                        [table[row][col],
                        table[below_ele_row][below_ele_col]
                        ])
            ele_idx = np.array(
                        [[row, col], 
                        [below_ele_row, below_ele_col]
                        ])

        else:
            # either go rightward or downward
            ele_val = np.array(
                        [table[row][col],
                        table[below_ele_row][below_ele_col],
                        table[r_ele_row][r_ele_col]
                        ])
            ele_idx = np.array(
                        [[row, col], 
                        [below_ele_row, below_ele_col],
                        [r_ele_row, r_ele_col]
                        ])
        # find min value among three elements
        min_idx = ele_idx[np.argmin(ele_val)]
        min_row = min_idx[0]
        min_col = min_idx[1]
        # swap max element with current element
        if min_row!=row or min_col!=col:
            tmp = table[row][col]
            table[row][col] = table[min_row][min_col]
            table[min_row][min_col] = tmp
            bubbleDown(table, min_row, min_col)
            

def oper_insert(values, table):
    for val in values:
        inf_idx = np.argwhere(table==np.inf)[0] # the first inf index found in the table
        table[inf_idx[0]][inf_idx[1]] = val
        bubbleUp(table, inf_idx[0], inf_idx[1])
    

def oper_extraMin(table):
    min = table[0][0]
    inf_idx = np.argwhere(table==np.inf)
    for i in range(table.shape[0]-1,-1,-1):
        for j in range(table.shape[1]-1,-1,-1):
            if not np.isinf(table[i][j]):
                table[0][0] = table[i][j]
                table[i][j] = np.inf
                bubbleDown(table, 0, 0)
                return min
    return min

def writeOut(table, outputPath, msg):
    with open(outputPath, 'a') as f:
        f.write(msg)
        f.write('\n')
        for row in table:
            for ele in row:
                if not np.isinf(ele):
                    f.write(str(int(ele)))
                    f.write(' ')
                else:
                    f.write('x')
                    f.write(' ')
            f.write('\n')
        f.write(' ')
        f.write('\n')

def handler(data, outputPath):
    operation = data[0]
    if operation == '1':
        insertValues = [int(ele) for ele in data[1].split(' ')]
        ## 1. build table
        table = [[int(ele) if ele != 'x' else math.inf 
                for ele in row.split(' ')] 
                for row in data[2:]]
        table = np.array(table)
        ## 2. do operation
        oper_insert(insertValues, table)
        ## 3. write out to txt file
        msg = ['Insert']
        for val in insertValues:
            msg.append(str(val))
        writeOut(table, outputPath, ' '.join(msg))
        
    elif operation == '2':
        ## 1. build table
        table = [[int(ele) if ele != 'x' else math.inf 
                for ele in row.split(' ')]
                for row in data[1:]]
        table = np.array(table)
        ## 2. do operation
        min = oper_extraMin(table)
        ## 3. write out to txt file
        writeOut(table, outputPath, f'Extract-min {int(min)}')

def main():
    inputPath = os.path.join('.', 'input.txt')
    outputPath = os.path.join('.', 'output.txt')
    if os.path.exists(outputPath):
        os.remove(outputPath)
    num_tables = 0
    with open(inputPath) as f:
        num_tables = int(f.readline())
        raw_data = f.read().split('\n')
        for _ in range(num_tables):
            data = []
            while True:
                try:
                    e = raw_data.pop(0)
                    if e == '':
                        break
                    else:
                        data.append(e)
                except:
                    break
            handler(data, outputPath)

if __name__ == "__main__":
    main()
            
            
                
            
        

