from random import randint
from copy import deepcopy

def legal(board,pos):
    if pos[0]<0 or pos[1]<0 or pos[0]>=7 or pos[1]>=7:
        return False
    if board[pos[0]][pos[1]]==0:
        return True
    return False

def neighbors(board,pos):
    """
    n=[]
    #print 'hi'
    for i in xrange(-1*depth,depth+1):
        for j in xrange(-1*depth,depth+1):
            test=(pos[0]+i,pos[1]+j)
            #print test
            if legal(board,test):
                n.append(test)
    return n
    """
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
    while not done and curr[0]<10:
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

def neighborFind(node):#find the neighbor whose score is max
    kids=children(node)
    #if len(kids)==0:
    #    print node
    scores=[]
    for child in kids:
        c=getChild(node,child)
        myScore=bfsScore(c[0],c[node[3]])
        bScore=bfsScore(c[0],child[1])
        s=myScore+bScore
        scores.append(s)
    
    ind=argmax(scores)
    return kids[ind]


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

def children(node):#a child is a set of two positions. first is the move second is the remove
    board=node[0]
    currentPlayerPos=node[node[3]]
    otherPlayerPos=node[enemyid(node[3])]
    
    currentPlayerNeigh=neighbors(board,currentPlayerPos)
    otherPlayerNeigh=neighbors(board,otherPlayerPos)
    #otherPlayerNeigh.append(currentPlayerPos)
    #print len(currentPlayerNeigh)
    #print len(otherPlayerNeigh)

    #randBlock=findRandomBlock(board,otherPlayerNeigh,currentPlayerNeigh)

    c=[]
    for n in currentPlayerNeigh:
        for o in otherPlayerNeigh:
            if not(n==o):
                c.append((n,o))

    return c

def getChild(node,child):
    board=deepcopy(node[0])
    currPos=node[node[3]]
    
    board[currPos[0]][currPos[1]]=0
    board[child[0][0]][child[0][1]]=node[3]
    board[child[1][0]][child[1][1]]=-1

    if node[3]==1:
        newNode=(board,child[0],node[2],2)
    else:
        newNode=(board,node[1],child[0],1)
    return newNode

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

    if pid==1:
        node=(board,player,enemy,1)
    else:
        node=(board,enemy,player,2)

    move,remove=neighborFind(node)
    
    #move=neighborFind(board,player,argmax)
    #board[move[0]][move[1]]=pid
    #board[player[0]][player[1]]=0
    #remove=neighborFind(board,enemy,argmax)

    return [move,remove]
    #print str(move[0])+' '+str(move[1])
    #print str(remove[0])+' '+str(remove[1])
