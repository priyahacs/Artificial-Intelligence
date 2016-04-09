__author__ = 'Preethi'
import sys
from copy import deepcopy
def preparation(kay,kay_goal,jay,jay_goal):
    mixed = []
    for i in range(len(kay)):
        mixed.append(kay[i])
    mixed.append(kay_goal)
    jay.reverse()
    for j in range(len(jay)):
        mixed.append(jay[j])
    mixed.append(jay_goal)
    return mixed

def preparation_name(player_1,play1_m,player_2,play2_m):
    prep = []
    prep1 = []
    k = 2
    for i in range(len(player_1)+1):
        prep.append("B"+str(k))
        k += 1
    j = 2
    for i in range(len(player_2)):
        prep1.append("A"+str(j))
        j +=1
    prep1.reverse()
    for i in range(len(prep1)):
        prep.append(prep1[i])
    prep.append("A"+ str(1))
    return prep


def getAvailableMoves(o1,player_turn):
    retVal = []
    playerPots = o1
    if(player_turn == 1):
        for i in range(p1_goal):
            a = playerPots[i]
            if int(a) > 0:
                retVal.append(i)
    elif(player_turn == 2):
        for i in range(p1_goal+1, p2_goal):
            a = playerPots[i]
            if int(a) > 0:
                retVal.append(i)
    #print(retVal)
    return retVal

def getAvailableMoves_MiniMax(o1,player_turn):
    retVal = []
    playerPots = o1
    if(player_turn == 1):
        for i in range(p1_goal):
            a = playerPots[i]
            if int(a) > 0:
                retVal.append(i)
    elif(player_turn == 2):
        #print("inside 2",p1_goal+1 )
        for i in range(p1_goal+1, p2_goal):
            a = playerPots[i]
            if int(a) > 0:
                retVal.append(i)
        retVal.reverse()

    #print("avail moves for o1",o1,retVal)
    return retVal


def end_game(board1):
    retVal = []
    retVal1 = []
    end = False

    for i in range(p1_goal):
        a = board1[i]
        if int(a) > 0:
            retVal.append(i)
    if len(retVal) == 0:
        end = True

    for i in range(p1_goal+1, p2_goal):
        a = board1[i]
        if int(a) > 0:
            retVal1.append(i)
    if len(retVal1) == 0:
        end = True
    return end


def calculate_end_game(board1):
    retVal = []
    retVal1 = []
    for i in range(p1_goal):
        a = board1[i]
        if int(a) > 0:
            retVal.append(i)

    for i in range(p1_goal+1, p2_goal):
        a = board1[i]
        if int(a) > 0:
            retVal1.append(i)
    if len(retVal) == 0:
        for app in range(p1_goal+1, p2_goal):
            temp = int(board1[app])
            board1[p2_goal] = int(board1[p2_goal]) + temp
            board1[app] = 0
    elif len(retVal1) == 0:
        for app in range(p1_goal):
            temp = int(board1[app])
            board1[p1_goal] = int(board1[p1_goal]) + temp
            board1[app] = 0

    return board1


def playGreedy(boards,play_turn):
    result = []
    temp_result = []
    p1 = []
    p2 = []
    avail = getAvailableMoves(boards,play_turn)
    if(play_turn == 1):

        max = []
        for i in range(len(avail)):
            alpha = boards[p1_goal] - boards[p2_goal]
            man = play_for_one(avail[i],boards,alpha,boards)
            max.append([man[1],avail[i],man[2]])
        #print("sort",max)
        max.sort(reverse = True)
        big  = max[0][0]
        sort = []
        for loop in range(len(max)):
            if(max[loop][0] == big):
                sort.append(max[0])

        sort.sort()
        temp_result.append(sort[0])
        whole_array = temp_result[0][2]
        p1_m = temp_result[0][0]
        for i in range(p1_goal):
            p1.append(whole_array[i])
        for i in range(int(p1_goal)+1,p2_goal):
            p2.append(whole_array[i])
        p2.reverse()
        #print(p1,p2)
        p2_m = whole_array[p2_goal]

        #print(whole_array)
        result.append(p2)
        result.append(p1)
        result.append(p2_m)
        result.append(p1_m)
        #print(max[0][0])
    if(play_turn == 2):
        max = []
        for i in range(len(avail)):
            alpha = boards[p2_goal]- boards[p1_goal]
            man = play_for_two(avail[i],boards,alpha,boards,play_turn)
            max.append([man[1],avail[i],man[2]])
        #print("hayoooo",max)
        max.sort(reverse = True)
        big  = max[0][0]
        sort = []
        for loop in range(len(max)):
            if(max[loop][0] == big):
                sort.append(max[0])
        #print(sort)
        sort.sort()
        temp_result.append(sort[0])
        whole_array = temp_result[0][2]
        p2_m = temp_result[0][0]
        for i in range(p1_goal):
            p1.append(whole_array[i])
        for i in range(int(p1_goal)+1,p2_goal):
            p2.append(whole_array[i])
        p2.reverse()
        #print(p1,p2)
        p1_m = whole_array[p1_goal]

        #print(whole_array)
        result.append(p2)
        result.append(p1)
        result.append(p2_m)
        result.append(p1_m)

    return result

def play_for_one(index,moved_config,old_max,max_config):
    new_max = int(old_max)
    config = deepcopy(max_config)
    board1 = deepcopy(moved_config)
    #for id in range(len(k)):
     #   board1.append(k[id])
    #print("board1,",board1,moved_config,max_config)
    a = []
    ik = 0
    seeds_count = int(board1[index])
    board1[index] = 0
    round = 1
    while (seeds_count > 0):
        if(round ==1 ):
            s = index+1
        else:
            s = 0
        for ik in range(s,int(len(board1))-1):
            if(seeds_count > 0):
                board1[ik] = int(board1[ik])+1
                seeds_count -=1
            else:
                break
        round +=1
    last = ik-1

    """if end_game(board1):
        for app in range(p1_goal+1, p2_goal):
            temp = int(board1[app])
            board1[p2_goal] = int(board1[p2_goal]) + temp
            board1[app] = 0
        a.append(board1[p1_goal])
        print("board value",board1)"""


    if (last) < p1_goal:
        if int(board1[last]) == 1:
            aj = board1[last] + board1[p1_goal + (p1_goal-last)] + board1[p1_goal]
            a.append(aj)
            board1[last] = 0
            board1[p1_goal+(p1_goal-last)] = 0
            board1[p1_goal] = aj
        else:
            a.append(board1[p1_goal])
    else:
        a.append(board1[p1_goal])

    """if(int (a[0]) > new_max):
        new_max = int(a[0])
        config = board1"""
    if end_game(board1):
        """for app in range(p1_goal+1, p2_goal):
            temp = int(board1[app])
            board1[p2_goal] = int(board1[p2_goal]) + temp
            board1[app] = 0"""
        calc = calculate_end_game(board1)
        board1 = calc

        #print("board value",board1)

    utility  = int(board1[p1_goal]) - int(board1[p2_goal])
    if(utility > new_max):
        new_max = utility
        config = deepcopy(board1)


    if end_game(board1) == False:
        if last == p1_goal:
            avail = getAvailableMoves(board1,player_turn)
            #print(avail)
            maxi = []
            #print("outside loop---------",new_max)
            for i in range(len(avail)):
                jk  = play_for_one(avail[i],board1,new_max,config)
                #print("jk", avail[i],jk)
                maxi.append([jk[1],avail[i],jk[2]])
            maxi.sort(reverse=True)
            #print(maxi)
            big = []
            big_num = int(maxi[0][0])
            for h in range(len(maxi)):
                if(big_num == maxi[h][0]):
                    big.append(maxi[h])
            #print("big",big)
            big.sort()
            #print("big",big)
            m1 = int(big[0][0])
            #print("before m1, new_max,config",m1,new_max,config,)
            if(m1 > new_max):
                new_max = m1
                config = big[0][2]
                #print("after m1, new_max,config",m1,new_max,config)
            a.append(new_max)
            a.append(config)
            return a
        else:
            a.append(new_max)
            a.append(config)
            return a

    else:
        a.append(new_max)
        a.append(config)
        return a



def play_for_two(index,moved_config,old_max,max_config,play_turn):
    new_max = int(old_max)
    config = deepcopy(max_config)
    board1 = deepcopy(moved_config)
    #for id in range(len(k)):
     #   board1.append(k[id])
    #print("board1,",board1,moved_config,max_config)
    a = []
    pos = 0
    seeds_count = int(board1[index])
    board1[index] = 0
    round = 1
    last = p2_goal
    while (seeds_count > 0):
        if(round ==1 ):
            s = index+1
        else:
            s = 0
        for pos in range(s,p2_goal+1):
            if(seeds_count > 0):
                if(pos != p1_goal):
                    board1[pos] = int(board1[pos])+1
                    seeds_count -=1
            else:
                last = pos-1
                break
        round +=1

    if(last > p1_goal) and (last < p2_goal):
        if int(board1[last]) == 1:
            diff = last - p1_goal
            value = board1[last] + board1[p1_goal - diff] + board1[p2_goal]
            board1[last] = 0
            board1[p1_goal - diff] = 0
            board1[p2_goal] = value
            a.append(value)
        else:
            a.append(board1[p2_goal])
    else:
        a.append(board1[p2_goal])


    if end_game(board1):
        """for app in range(p1_goal):
            temp = int(board1[app])
            board1[p1_goal] = int(board1[p1_goal]) + temp
            board1[app] = 0"""
        calc = calculate_end_game(board1)
        board1 = calc
        #print("board value",board1)


    utility  = int(board1[p2_goal]) - int(board1[p1_goal])
    if(utility > new_max):
        new_max = utility
        config = board1

    """if(int (a[0]) > new_max):
        new_max = int(a[0])
        config = board1"""
    #print("outside loop---------",last,pos)
    if end_game(board1) == False:
        if last == p2_goal:

            avail = getAvailableMoves(board1,play_turn)
            maxi = []

            for i in range(len(avail)):
                #print("enna ma ipdi pandringalae ma",board1)
                jk  = play_for_two(avail[i],board1,new_max,config,play_turn)
                #print("man for index****** ",jk[1],new_max,jk[0])
                maxi.append([jk[1],avail[i],jk[2]])
            maxi.sort(reverse=True)
            m1 = int(maxi[0][0])

            if(m1 > new_max):
                new_max = m1
                config = maxi[0][2]
            a.append(new_max)
            a.append(config)
            return a
        else:
            a.append(new_max)
            a.append(config)
            return a
    else:
        a.append(new_max)
        a.append(config)
        return a


def terminal_Test(depth):
    if(depth > cutoff_depth):
        return True
    else:
        return False


def legal_move_player1(board_config,index_move):
    hybrid_array = board_config
    seeds_count = int(hybrid_array[index_move])

    result = []
    free_play = False
    game_over = False
    #print("position",index_move,seeds_count,hybrid_array)
    pos = 0
    round = 1
    hybrid_array = [int(j) for j in hybrid_array]
    hybrid_array[index_move] = 0
    #print("hi",hybrid_array)
    #print("entering",name[index_move],hybrid_array,index_move)
    while (seeds_count > 0):
        if(round == 1 ):
            s = index_move + 1
        else:
            s = 0
        for pos in range(s,p2_goal):
            if(seeds_count > 0):
                hybrid_array[pos] = int(hybrid_array[pos])+1
                seeds_count -=1
                    #print("k1[ik]",hybrid_array[pos],pos)
            else:
                break
        round +=1
    last = pos-1

    if end_game(hybrid_array):
        calc = calculate_end_game(hybrid_array)
        hybrid_array = calc
        result.append(hybrid_array[p1_goal])
        game_over = True
    elif last < p1_goal:
        if int(hybrid_array[last]) == 1:
            value = hybrid_array[last] + hybrid_array[p1_goal + (p1_goal-last)] + hybrid_array[p1_goal]
            hybrid_array[last] = 0
            hybrid_array[p1_goal+(p1_goal-last)] = 0
            hybrid_array[p1_goal] = value
            result.append(value)
        else:
            result.append(hybrid_array[p1_goal])
    else:
        result.append(hybrid_array[p1_goal])




    """if (last < p1_goal) and int(hybrid_array[last]) == 1:
        value = hybrid_array[last] + hybrid_array[p1_goal + (p1_goal-last)] + hybrid_array[p1_goal]
        hybrid_array[last] = 0
        hybrid_array[p1_goal+(p1_goal-last)] = 0
        hybrid_array[p1_goal] = value

    if end_game(hybrid_array):
        calc = calculate_end_game(hybrid_array)
        hybrid_array = calc
        #result.append(hybrid_array[p1_goal])
        game_over = True

           result.append(value)
        else:
            result.append(hybrid_array[p1_goal])
    else:
        result.append(hybrid_array[p1_goal])   """

    if(last) == p1_goal:
        free_play = True
    result.append(free_play)
    result.append(hybrid_array)
    result.append(game_over)
    return result

def legal_move_player2(board_config,index_move):
    hybrid_array = deepcopy(board_config)
    seeds_count = int(hybrid_array[index_move])
    result = []
    free_play = False
    game_over = False
    #print("position",index_move,seeds_count,hybrid_array)
    pos = 0
    round = 1
    last = p2_goal
    hybrid_array = [int(j) for j in hybrid_array]
    hybrid_array[index_move] = 0
    #print("entering",name[index_move],hybrid_array,index_move)
    while (seeds_count > 0):
        if(round == 1 ):
            s = index_move + 1
        else:
            s = 0
        for pos in range(s,p2_goal+1):
            if(seeds_count > 0):
                if(pos != p1_goal):
                    hybrid_array[pos] = int(hybrid_array[pos])+1
                    seeds_count -=1
                    #print("k1[ik]",hybrid_array[pos],pos)
            else:
                last = pos-1
                break
        round +=1

    if end_game(hybrid_array):

        calc = calculate_end_game(hybrid_array)
        hybrid_array = calc
        print("hybrid array in end game",hybrid_array)
        result.append(hybrid_array[p2_goal])
        game_over = True
    elif(last > p1_goal) and (last < p2_goal):
        if int(hybrid_array[last]) == 1:
            diff = last - p1_goal
            value = hybrid_array[last] + hybrid_array[p1_goal - diff] + hybrid_array[p2_goal]
            hybrid_array[last] = 0
            hybrid_array[p1_goal - diff] = 0
            hybrid_array[p2_goal] = value
            result.append(value)
        else:
            result.append(hybrid_array[p2_goal])
    else:
        result.append(hybrid_array[p2_goal])


    """if(last > p1_goal) and (last < p2_goal):
        if int(hybrid_array[last]) == 1:
            diff = last - p1_goal
            value = hybrid_array[last] + hybrid_array[p1_goal - diff] + hybrid_array[p2_goal]
            hybrid_array[last] = 0
            hybrid_array[p1_goal - diff] = 0
            hybrid_array[p2_goal] = value

    if end_game(hybrid_array):
        calc = calculate_end_game(hybrid_array)
        hybrid_array = calc
        print("hybrid array in end game",hybrid_array)
        #result.append(hybrid_array[p2_goal])
        game_over = True

        result.append(value)
        else:
            result.append(hybrid_array[p2_goal])
    else:
        result.append(hybrid_array[p2_goal])"""


    if(last) == p2_goal:
        free_play = True

    result.append(free_play)
    result.append(hybrid_array)
    #print("hybrid array:",hybrid_array)
    result.append(game_over)
    return result


def minValue(board_config,index_move,play_turn,depth,value,good_config):

    minvalue1 = value
    res = []
    if(play_turn == 1):
        move = legal_move_player1(board_config,index_move)
        #print("move",move,move[2])
    else:
        move = legal_move_player2(board_config,index_move)
        #print("movesss",move,name[index_move],move[2])

    free_play = move[1]
    config = deepcopy(move[2])
    game_over = move[3]
    #print("enna ma epdipandringae,",free_play,config,name[index_move])
    #print("config:",str(name[index_move]),depth,config)
    if(player_turn == 1):
        ob_value = config[p1_goal] - config[p2_goal]
    else:
        ob_value = config[p2_goal] - config[p1_goal]

    if(game_over):
        if(free_play == True):
            #out1.write(str(name[index_move])+","+str(depth)+","+"-Infinity"+"\n")
            minvalue = ob_value
            out1.write(str(name[index_move])+","+str(depth)+","+str(minvalue)+"\n")
        else:
            #out1.write(str(name[index_move])+","+str(depth)+","+"Infinity"+"\n")
            minvalue = ob_value
            out1.write(str(name[index_move])+","+str(depth)+","+str(minvalue)+"\n")
        res.append(minvalue)
        res.append(config)
        res.append(good_config)
        print("inside",depth,res,name[index_move])
        return res
    elif(depth == cutoff_depth):
        if(free_play == True):
            minvalue = Infinity
            out1.write(str(name[index_move])+","+str(depth)+","+"Infinity"+"\n")
        else:
            minvalue = ob_value
            out1.write(str(name[index_move])+","+str(depth)+","+str(minvalue)+"\n")
    else:
        minvalue = Infinity
        out1.write(str(name[index_move])+","+str(depth)+","+"Infinity"+"\n")


    if(free_play == True):
        avail = getAvailableMoves_MiniMax(config,play_turn)
        for i in range(len(avail)):
            if(play_turn == 1):
                move = legal_move_player1(config,avail[i])
            #print("move",move,move[2])
            else:
                move = legal_move_player2(config,avail[i])
            bonus_play = move[1]
            if(bonus_play):
                v1 = minValue(config,avail[i],play_turn,depth,minvalue,good_config)
                #print("V1 in minValue in min1",v1,str(name[avail[i]]),depth)
                if(v1[0] < minvalue):
                    minvalue = v1[0]
                    if(depth == 1):
                        good_config = v1[1]
                out1.write(str(name[index_move])+","+str(depth)+","+str(minvalue)+"\n")
            else:
                v1 = maxValue(config,avail[i],play_turn,depth,minvalue,good_config)
                #print("V1 in maxValue in min2",v1,str(name[avail[i]]),depth)
                if(v1[0] < minvalue):
                    minvalue = v1[0]
                    if(depth == 1):
                        good_config = v1[1]
                out1.write(str(name[index_move])+","+str(depth)+","+str(minvalue)+"\n")

    elif (terminal_Test(depth+1) == False):
        if play_turn == 1:
            send_turn = 2
        else:
            send_turn = 1
        avail = getAvailableMoves_MiniMax(config,send_turn)
        for i in range(len(avail)):
            if(send_turn == 1):
                move = legal_move_player1(config,avail[i])
            #print("move",move,move[2])
            else:
                move = legal_move_player2(config,avail[i])
            free_play = move[1]
            if(free_play):

                v1 = minValue(config,avail[i],send_turn,depth+1,minvalue,good_config)
                #print("V1 in minValue in min3",v1,str(name[avail[i]]),depth)
                if(v1[0] < minvalue):
                    minvalue = v1[0]
                out1.write(str(name[index_move])+","+str(depth)+","+str(minvalue)+"\n")

            else:
                v1 = maxValue(config,avail[i],send_turn,depth+1,minvalue,good_config)
                #print("V1 in maxValue in max4",v1,str(name[avail[i]]),depth)
                if(v1[0] < minvalue):
                    minvalue = v1[0]
                out1.write(str(name[index_move])+","+str(depth)+","+str(minvalue)+"\n")
    res.append(minvalue)
    res.append(config)
    res.append(good_config)
    #print("result for", res,str(name[index_move]),depth)
    return res

def maxValue(board_config,index_move,play_turn,depth,value,good_config):

    maxvalue = value
    #good_config = gud_config
    res = []
    if(play_turn == 1):
        move = legal_move_player1(board_config,index_move)
        #print("move",move)
    else:
        move = legal_move_player2(board_config,index_move)

    free_play = move[1]
    config = deepcopy(move[2])
    game_over = move[3]
    if(player_turn == 1):
        ob_value = config[p1_goal] - config[p2_goal]
    else:
        ob_value = config[p2_goal] - config[p1_goal]

    #print("config:",str(name[index_move]),depth,config)
    if(game_over):
        if(free_play == True):
            #out1.write(str(name[index_move])+","+str(depth)+","+"-Infinity"+"\n")
            minvalue = ob_value
            out1.write(str(name[index_move])+","+str(depth)+","+str(minvalue)+"\n")
        else:
            #out1.write(str(name[index_move])+","+str(depth)+","+"Infinity"+"\n")
            minvalue = ob_value
            out1.write(str(name[index_move])+","+str(depth)+","+str(minvalue)+"\n")
        res.append(minvalue)
        res.append(config)
        res.append(good_config)
        print("inside",depth,res,name[index_move],minvalue,config)
        return res
    elif(depth == cutoff_depth):
        if(free_play == True):
            maxvalue = -Infinity
            out1.write(str(name[index_move])+","+str(depth)+","+"-Infinity"+"\n")
        else:
            maxvalue = ob_value
            out1.write(str(name[index_move])+","+str(depth)+","+str(maxvalue)+"\n")
    else:
        maxvalue = -Infinity
        out1.write(str(name[index_move])+","+str(depth)+","+"-Infinity"+"\n")

    if(free_play == True):
        avail = getAvailableMoves_MiniMax(config,play_turn)
        #print("maxvalue",config,avail)

        for i in range(len(avail)):
            if(play_turn == 1):
                move = legal_move_player1(config,avail[i])
                    #print("move",move,move[2])
            else:
                move = legal_move_player2(config,avail[i])
            bonus_play = move[1]
            if(bonus_play):
                v1 = maxValue(config,avail[i],play_turn,depth,maxvalue,good_config)
                #print("V1 in maxValue in max1",v1,str(name[avail[i]]),depth)
                if(v1[0] > maxvalue):
                    maxvalue = v1[0]
                    if(depth == 1):
                        good_config = v1[1]
                out1.write(str(name[index_move])+","+str(depth)+","+str(maxvalue)+"\n")
            else:
                v1 = minValue(config,avail[i],play_turn,depth,maxvalue,good_config)
                #print("V1 in minValue in max2",v1,str(name[avail[i]]),depth)
                if(v1[0] > maxvalue):
                    maxvalue = v1[0]
                    if(depth == 1):
                        good_config = v1[1]
                out1.write(str(name[index_move])+","+str(depth)+","+str(maxvalue)+"\n")
                #print("maxvalue", v1,config)
                #print("v1,avail[i] configgggggggggggggggggg ",v1,name[avail[i]],config,depth,maxvalue)

    elif (terminal_Test(depth+1) == False) :
        if play_turn == 1:
            send_turn = 2
        else:
            send_turn = 1
        avail = getAvailableMoves_MiniMax(config,send_turn)
        for i in range(len(avail)):
            if(send_turn == 1):
                move = legal_move_player1(config,avail[i])
            #print("move",move,move[2])
            else:
                move = legal_move_player2(config,avail[i])
            free_play = move[1]
            if(free_play):
                v1 = maxValue(config,avail[i],send_turn,depth+1,maxvalue,good_config)
                #print("V1 in maxValue in max3",v1,str(name[avail[i]]),depth)
                if(v1[0] > maxvalue):
                    maxvalue = v1[0]
                out1.write(str(name[index_move])+","+str(depth)+","+str(maxvalue)+"\n")
            else:
                v1 = minValue(config,avail[i],send_turn,depth+1,maxvalue,good_config)
                #print("V1 in minValue in max4",v1,str(name[avail[i]]),depth)
                if(v1[0] > maxvalue):
                    maxvalue = v1[0]
                out1.write(str(name[index_move])+","+str(depth)+","+str(maxvalue)+"\n")

            #print("v1,avail[i] config ",v1,name[avail[i]],config,depth,maxvalue)
    res.append(maxvalue)
    res.append(config)
    res.append(good_config)
    #print("result for", res,str(name[index_move]),depth)
    return res


def play_MiniMax(boards,plays_turn):

    #print(boards,player_turn)
    out1.write("Node,Depth,Value\n")
    out1.write("root,0,-Infinity\n")
    root_value = -Infinity
    depth = 0
    play_turn =  plays_turn
    avail = getAvailableMoves_MiniMax(boards,play_turn)
    for i in range(len(avail)):
    #for i in range(2,len(avail)):
    #for i in range(3,len(avail)):
        if(play_turn == 1):
            move = legal_move_player1(boards,avail[i])
            #print("move",move,move[2])
        else:
            move = legal_move_player2(boards,avail[i])

        free_play = move[1]
        good_config = move[2]
        if(free_play):
            return_value = maxValue(boards,avail[i],play_turn,depth+1,-Infinity,good_config)
        else:
            return_value = minValue(boards,avail[i],play_turn,depth+1,Infinity,good_config)
        #print("minimax over",return_value,str(name[avail[i]]))
        if(return_value[0] > root_value):
            root_value = return_value[0]
            next_state = return_value[2]
        out1.write("root,0,"+str(root_value)+"\n")
    #print("!!!!!!!!!!!!!!!!!!!!!!!!",next_state)
    return next_state


inputFile = open(sys.argv[2],'r')
outputFile = open("next_state.txt","w")
out1 = open("traverse_log.txt","w")
algo = int(inputFile.readline())
#print("algo:",algo)

player_turn = int(inputFile.readline())
#print("player_turn:",player_turn)

cutoff_depth = int(inputFile.readline())
#print("cutoff_depth:",cutoff_depth)

player_2=[]
play2 = inputFile.readline()
play2.strip('\n')
player_2 = play2.strip().split(' ')

player_1=[]
play1 = inputFile.readline().strip('\n')
player_1 = play1.strip().split(' ')

#print("player_1",player_1)

play2_m = inputFile.readline().strip('\n')
play1_m = inputFile.readline().strip('\n')
Infinity = 10000000000000

mix = preparation(player_1, play1_m, player_2, play2_m)
#print(mix)
mix = [int(j) for j in mix]
name = preparation_name(player_1,play1_m,player_2,play2_m)
#print(name[])
p1_goal = len(player_1)
p2_goal = len(mix) - 1

if(algo == 1):

    #print(p1_goal,p2_goal)
    ans = playGreedy(mix,player_turn)
    a1 = ans[0]
    a2 = ', '.join(map(str, a1))
    a3 = a2.replace(',',' ')
    out = outputFile.write(a3+"\n")

    b1 = ans[1]
    b2 = ', '.join(map(str, b1))
    b3 = b2.replace(',',' ')
    out = outputFile.write(b3+"\n")

    c1 = str(ans[2])
    out = outputFile.write(c1+"\n")

    d1 = str(ans[3])
    out = outputFile.write(d1+"\n")

if(algo == 2):
    ans = play_MiniMax(mix,player_turn)
    print(ans)
    a1 = []
    a2 = []

    for j in range(p1_goal+1,p2_goal):
        a1.append(ans[j])
    a1.reverse()
    b1 = ', '.join(map(str, a1))
    c1 = b1.replace(',',' ')


    for j in range(p1_goal):
        a2.append(ans[j])
    b2 = ', '.join(map(str, a2))
    c2 = b2.replace(',',' ')

    a3 = str(ans[p2_goal])
    a4 = str(ans[p1_goal])
    out = outputFile.write(c1+"\n")
    out = outputFile.write(c2+"\n")
    out = outputFile.write(a3+"\n")
    out = outputFile.write(a4+"\n")




