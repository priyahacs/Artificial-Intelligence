__author__ = 'Padma'
import sys
from collections import deque


def findChildren(element, nodes):
    elements = element.strip().split(' ')
    children = []
    for op in range(0, len(nodes)):
        if (str(nodes[op][0]) == str(elements[0])):
            children.append(nodes[op])
    return children


def goal_test(node, destinations):
    if node not in destinations:
        return False
    else:
        return True


def sorting_bfs(arr):
    sortArrayBfs = []
    for k in range(0, len(arr)):
        sortArrayBfs.append(arr[k][1])
    sortArrayBfs.sort()
    return sortArrayBfs


def sorting_dfs(inputArr):
    sortArrayDfs = []
    for ku in range(0, len(inputArr)):
        sortArrayDfs.append(inputArr[ku][1])
    sortArrayDfs.sort()
    sortArrayDfs.reverse()
    return sortArrayDfs


def backtrace(parent, start, end):
    s = start[0]
    path = []
    path.append(end)
    while path[-1] != s:
        path.append(parent[path[-1]])
    path.reverse()
    return path


def findChildren_ucs(element, nodes, cost):
    children = []
    for op in range(0, len(nodes)):
        if (str(nodes[op][0]) == str(element)):
            if (findactive(nodes[op], cost)):
                children.append(nodes[op])
    return children


def findactive(node, cost):
    array1 = []
    si = node[3]
    c = cost
    if int(cost) >= 24:
        c = int(cost) % 24
    if (int(si) != 0):
        for p in range(4, len(node)):
            array1.append(node[p])
        for jk in range(0, len(array1)):
            ai = array1[jk]
            bi = ai.strip().split('-')
            if c in range(int(bi[0]), int(bi[1]) + 1):
                return False
    return True


def update_cost(children, cost):
    for ki in range(0, len(children)):
        children[ki][2] = int(children[ki][2]) + cost
    return children


def separate_child(up):
    ak = []
    for g in range(0, len(up)):
        rk = [up[g][2], up[g][1]]
        ak.append(rk)
    return ak


def ucs(source, destination, links, time):
    try:
        frontier = []
        explored = []
        ww = [time, source[0]]
        frontier.append(ww)

        while (len(frontier) > 0):
            sp = []
            popelement = frontier.pop()
            popelement_cost = popelement[0]
            popelement_item = popelement[1]
            parent_cost = int(popelement_cost)
            if (goal_test(popelement_item, destination)):
                res = popelement_item
                ans = parent_cost
                if (parent_cost >= 24):
                    ans = parent_cost % 24
                return res + " " + str(ans)
            else:
                find = findChildren_ucs(popelement_item, links, parent_cost)
                if (len(find) != 0):

                    up = update_cost(find, parent_cost)
                    if (len(frontier) != 0):

                        child_insert = separate_child(up)

                        for fs in range(0, len(child_insert)):
                            ele = child_insert[fs][1]
                            cos = child_insert[fs][0]
                            for er in range(0, len(frontier)):
                                q = frontier[er][1]
                                w = frontier[er][0]
                                if (str(ele) == (q)):
                                    if (int(cos) < int(w)):
                                        frontier[er][0] = cos

                                    sp.append(ele)

                        for ji in range(0, len(child_insert)):
                            lo = child_insert[ji][1]
                            if lo not in explored:
                                if lo not in sp:
                                    frontier.append(child_insert[ji])
                    else:
                        child_insert = separate_child(up)
                        for j in range(0, len(child_insert)):
                            fi = child_insert[j][1]
                            if fi not in explored:
                                frontier.append(child_insert[j])

                    frontier.sort(reverse=True)
                    explored.append(popelement_item)

                else:
                    if (len(frontier) != 0):
                        frontier.sort(reverse=True)
                    explored.append(popelement_item)

        return "None"
    except Exception as e:
        res = "None"
        return res


def bfs(source, destination, links, time):
    try:
        node = []

        node = source
        pathcost = time

        explored = []
        parent = {}
        frontier = deque(node)

        while (len(frontier) > 0):
            popelement = frontier.popleft()
            if (goal_test(popelement, destination)):
                path_trace = backtrace(parent, source, popelement)
                pathcost = pathcost + (len(path_trace) - 1)
                ans = pathcost
                if (pathcost >= 24):
                    ans = pathcost % 24
                res = popelement + " " + str(ans)
                return (res)

            else:

                find = findChildren(popelement, links)
                sorted_bfs = sorting_bfs(find)
                for p in range(0, len(sorted_bfs)):
                    if sorted_bfs[p] not in explored:
                        if sorted_bfs[p] not in frontier:
                            parent[sorted_bfs[p]] = popelement
                            frontier.append(sorted_bfs[p])
                explored.append(popelement)
        return "None"
    except Exception as e:
        res = "None"
        return res


def dfs(source, destination, links, time):
    try:
        node = []
        ako = []

        node = source
        ako.append(node[0])
        pathcost = time
        explored = []
        parent = {}
        frontier = []
        # frontier = deque(node)
        frontier.append(node[0])

        while (len(frontier) > 0):
            popelement = frontier.pop()
            if (goal_test(popelement, destination)):
                path_trace = backtrace(parent, source, popelement)
                pathcost = pathcost + (len(path_trace) - 1)
                explored.append(popelement)
                ans = pathcost
                if (pathcost >= 24):
                    ans = pathcost % 24
                res = popelement + " " + str(ans)
                return (res)

            else:

                find = findChildren(popelement, links)
                sorted_dfs = sorting_dfs(find)
                for q in range(0, len(sorted_dfs)):
                    if sorted_dfs[q] not in explored:
                        if sorted_dfs[q] not in frontier:
                            parent[sorted_dfs[q]] = popelement
                            frontier.append(sorted_dfs[q])
                explored.append(popelement)
        return "None"
    except Exception as e:
        res = "None"
        return res


inputFile = open(sys.argv[2], 'r')
outputFile = open("output.txt", 'w')
totalCase = int(inputFile.readline())

for i in range(0, int(totalCase)):
    a = inputFile.readline()
    while (len(a.strip()) != 0):

            # Type of Algorithm
            algo = a.rstrip('\n')

            # Source
            sor = []
            source = inputFile.readline()
            sor = source.strip().split(' ')


            # Destination
            des = []
            destination = inputFile.readline()
            des = destination.strip().split(' ')

            mid = []
            # Middle nodes
            middle = inputFile.readline()
            mid = middle.strip().split(' ')

            # No of connections
            link_num = int(inputFile.readline())

            # List of all nodes
            Allnodes = []
            Allnodes = sor + des + mid

            # Each connection
            s = []
            if (int(link_num) != 0):
                k = 0
                for k in range(0, link_num):
                    links = inputFile.readline()
                    sep_link = links.strip().split(' ')
                    s.append(sep_link)

            # Timer start
            time_start = int(inputFile.readline())

            # print(algo)
            if (algo == 'BFS'):
                bfsres = bfs(sor, des, s, time_start)
                out1 = outputFile.write(bfsres + "\n")

            # findchildren("A")

            if (algo == 'DFS'):
                dfsres = dfs(sor, des, s, time_start)
                out1 = outputFile.write(dfsres + "\n")

            if (algo == 'UCS'):
                ucsres = ucs(sor, des, s, time_start)
                out1 = outputFile.write(ucsres + "\n")

            # Read the empty line after the case ends
            a = inputFile.readline()
