import alphabetaItDeep as player2
import newalphabetaItDeep as player1
#import NeighborEvaluation as player1
from copy import deepcopy
from time import time

def legal(board,pos):
    if pos[0]<0 or pos[1]<0 or pos[0]>=7 or pos[1]>=7:
        return False
    if board[pos[0]][pos[1]]==0:
        return True
    return False

def change(board,pos,num):
    board[pos[0]][pos[1]]=num

def turn(board,move,remove,oldSpot,pid):#pid=player making move
    change(board,oldSpot,0)
    change(board,move,pid)
    change(board,remove,-1)

def neighbors(board,pos):
    n=[]
    moves=[(0,1),(1,0),(0,-1),(-1,0),(1,1),(-1,1),(-1,-1),(1,-1)]
    for m in moves:
        test=(pos[0]+m[0],pos[1]+m[1])
        if legal(board,test):
            n.append(test)
    return n

def endGame(board,pos1,pos2):
    return len(neighbors(board,pos1))==0 or len(neighbors(board,pos2))==0

def printBoardandId(board,pid):
    colsWithNeg1=[]
    
    for row in board:
        for j,n in enumerate(row):
            if n==-1 and not(j in colsWithNeg1):
                colsWithNeg1.append(j)

    for row in board:
        if 0 in colsWithNeg1 and row[0]!=-1:
            s=' '
        else:
            s=''
        for j,n in enumerate(row):
            s+=str(n)
            if not(j==6):
                if j+1 in colsWithNeg1 and row[j+1]!=-1:
                    s+='  '
                else:
                    s+=' '

        print s

    print pid

board=[]
for i in xrange(7):
    row=[0]*7
    board.append(row)

pos=[(6,3),(0,3)]


change(board,pos[0],1)
change(board,pos[1],2)

curr=0
turns=0
while not endGame(board,pos[0],pos[1]):
    t=time()
    cboard=deepcopy(board)
    if curr==0:
        move,remove=player1.play(cboard,1)
    if curr==1:
        move,remove=player2.play(cboard,2)

    if not (move in neighbors(board,pos[curr])):
        print "cant move there"
        break

    turn(board,move,remove,pos[curr],curr+1)
    pos[curr]=move

    curr=(curr+1)%2
    turns+=1
    
    print '---------------------------------------------------------'
    printBoardandId(board,curr+1)
    print time()-t

print turns
