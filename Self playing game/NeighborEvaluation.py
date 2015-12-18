from random import randint
from copy import deepcopy

def legal(board,pos):
    if pos[0]<0 or pos[1]<0 or pos[0]>=7 or pos[1]>=7:
        return False
    if board[pos[0]][pos[1]]==0:
        return True
    return False

def neighbors(board,pos):
    n=[]
    moves=[(0,1),(1,0),(0,-1),(-1,0),(1,1),(-1,1),(-1,-1),(1,-1)]
    for m in moves:
        test=(pos[0]+m[0],pos[1]+m[1])
        if legal(board,test):
            n.append(test)
    return n

def bfsScore(board,pos):
    board=deepcopy(board)
    score=0
    q=[]
    curr=(0,pos)
    done=False
    while not done and curr[0]<7:
        neigh=neighbors(board,curr[1])
        
        for n in neigh:
            board[n[0]][n[1]]=-1
            q.append((curr[0]+1,n))
        
        mod=1./(2**curr[0])
        score+=len(neigh)*mod
        if len(q)==0:
            done=True
        else:
            curr=q.pop(0)
    
    return score

def neighborFind(board,pos,func):#find the neighbor whose score is favored by func
    #func must return the index of the favored score
    neigh=neighbors(board,pos)
    scores=[]
    for n in neigh:
        s=bfsScore(board,n)
        scores.append(s)
    
    ind=func(scores)
    return neigh[ind]


def argmax(l):
    m=max(l)
    return l.index(m)

def argmin(l):
    m=min(l)
    return l.index(m)

def find(board,pid):
    for i,row in enumerate(board):
        for j,n in enumerate(row):
            if n==pid:
                return (i,j)

def enemyid(pid):
    if pid==1:
        return 2
    return 1
            
"""
temp=[None,None]

board=[]
for i in xrange(7):
    row=raw_input()
    row=row.replace('  ',' ')
    row=row.split(' ')
    row=row[:7]
    
    row=[int(x) for x in row]
    
    board.append(row)
    
    if temp[1]==None or temp[0]==None:
        for j,n in enumerate(row):
            if n>0:
                temp[n-1]=(i,j)


pid=int(raw_input())
"""
def play(board,pid):
    player=find(board,pid)
    enemy=find(board,enemyid(pid))
        

    move=neighborFind(board,player,argmax)
    board[move[0]][move[1]]=pid
    board[player[0]][player[1]]=0
    remove=neighborFind(board,enemy,argmax)

    return [move,remove]
    #print str(move[0])+' '+str(move[1])
    #print str(remove[0])+' '+str(remove[1])

