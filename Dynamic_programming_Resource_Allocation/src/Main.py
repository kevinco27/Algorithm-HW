import numpy as np
import os

input_path = "./input.txt"
output_path = "./output.txt"


class Node():
    def __init__(self, projNbr, cumResource, cumProfit, predecessor):
        self.projNbr = projNbr
        self.cumResource = cumResource
        self.cumProfit = cumProfit
        self.pred = predecessor


class mulStageGraph():
    def __init__(self, profit_table):
        self.sink = None
        self.profit_table = profit_table

    def build_graph(self, max_res):
        numStage = len(self.profit_table)
        numChoices = len(self.profit_table[0])
        rootNode = Node(0, 0, 0, None)

        prevStage = max_res * [None]
        currStage = max_res * [None]
        for stage in range(numStage):
            if stage == 0:
                for i in range(numChoices):
                    curNode = Node(stage + 1, i + 1, self.profit_table[stage][i], rootNode)
                    prevStage[i] = curNode
            elif stage == numStage - 1:
                sink = Node(stage + 1, max_res, 0, None)
                start = 1 if max_res - numChoices < 2 else max_res - numChoices
                end = max_res
                for k in range(start, end):
                    preNode = prevStage[k - 1]
                    if preNode is None:
                        continue
                    profit = self.profit_table[stage][end - k - 1]
                    cumProfit = profit + preNode.cumProfit
                    if cumProfit >= sink.cumProfit:
                        sink.cumProfit = cumProfit
                        sink.pred = preNode
                self.sink = sink
                return sink
            else:
                for res in range(stage + 1, max_res + 1):
                    curNode = Node(stage + 1, res, 0, None)
                    currStage[res - 1] = curNode
                    start = 1 if res - numChoices < 2 else res - numChoices
                    end = res
                    for k in range(start, end):
                        preNode = prevStage[k - 1]
                        if preNode is None:
                            continue
                        profit = self.profit_table[stage][end - k - 1]
                        cumProfit = profit + preNode.cumProfit
                        if cumProfit >= curNode.cumProfit:
                            curNode.cumProfit = cumProfit
                            curNode.pred = preNode
                prevStage = currStage
                currStage = max_res * [None]


def main():
    with open(input_path) as f:
        strings = f.read()
        strings = strings.split('\n')

    split_idx = [-1]
    pre = None
    table = []
    for idx, tmp in enumerate(strings):
        if pre == '' and len(tmp) > 1:
            split_idx.append(idx - 1)
        pre = tmp
    split_idx.append(len(strings))

    pre_idx = None
    for idx in split_idx:
        table = None
        graph = None
        if idx == -1:
            pre_idx = idx
            continue
        pre = None
        for i in range(pre_idx + 1, idx):
            tmp = strings[i]
            if len(tmp) > 1 and table is None:
                table = []
                table.append([int(v) for v in tmp.split(' ')])
            elif len(tmp) > 1:
                table.append([int(v) for v in tmp.split(' ')])
            elif tmp == '' and len(pre) > 1:
                table = np.transpose(np.array(table))
                graph = mulStageGraph(table)
            elif len(tmp) == 1:
                resource = int(tmp)
                sink = graph.build_graph(resource)
                max_profit = sink.cumProfit
                with open(output_path, 'a') as fout:
                    fout.write(str(max_profit) + '\n')
            pre = tmp
        pre_idx = idx


if __name__ == "__main__":
    if os.path.exists(output_path):
        os.remove(output_path)
    main()
