from copy import deepcopy
from time import time
from random import randint

maxTime=4
startTime=0

def getOtherId(pid):
    if pid==1:
        return 2
    return 1

def find(board,pid):
    for i,row in enumerate(board):
        for j,n in enumerate(row):
            if n==pid:
                return (i,j)

def legal(board,pos):
    if pos[0]<0 or pos[1]<0 or pos[0]>=7 or pos[1]>=7:
        return False
    if board[pos[0]][pos[1]]==0:
        return True
    return False

def neighbors(board,pos):
    n=[]
    moves=[(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,1),(-1,-1),(1,-1)]
    for m in moves:
        test=(pos[0]+m[0],pos[1]+m[1])
        if legal(board,test):
            n.append(test)
    return n

def isTerminal(node):
    return len(neighbors(node[0],node[1]))==0 or len(neighbors(node[0],node[2]))==0

def terminalIsMe(node,maxPlayer):#assumes node is a terminal state
    if maxPlayer:
        playerId=node[3]
    else:
        playerId=getOtherId(node[3])

    if len(neighbors(node[0],node[playerId]))==0:
        return True
    return False

def numFilledSpaces(board):
    tot=0
    for row in board:
        for n in row:
            if n==-1:
                tot+=1

    return tot


def heuristic(node,maxPlayer,numFilled):
    #t=time()
    
    currId=node[3]
    otherId=getOtherId(currId)
        
    if maxPlayer:
        myId=currId
        oId=otherId
    else:
        myId=otherId
        oId=currId
    
    myMoves=len(neighbors(node[0],node[myId]))
    eMoves=len(neighbors(node[0],node[oId]))
    #filledSpaces=numFilledSpaces(node[0])

    #print time()-t
    
    return (myMoves-3*eMoves)*numFilled

"""
def bfsScore(board,pos):
    board=deepcopy(board)
    score=0
    q=[]
    curr=(0,pos)
    done=False
    while not done and curr[0]<5:
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

def heuristic(node,maxPlayer):
    #t=time()
    currId=node[3]
    otherId=getOtherId(currId)
        
    if maxPlayer:
        myId=currId
        oId=otherId
    else:
        myId=otherId
        oId=currId

    myPos=node[myId]
    oPos=node[oId]
    
    myScore=bfsScore(node[0],myPos)
    oScore=bfsScore(node[0],oPos)
    filledSpaces=numFilledSpaces(node[0])
    #print time()-t
    return (myScore-3*oScore)*filledSpaces
"""
#def findRandomBlock(board,oNeigh,cNeigh):
#    r=(-1,-1)
#    while not legal(board,r) or r in oNeigh,:
#        r=(randInt(0,6),randInt(0,6))
        

def children(node):#a child is a set of two positions. first is the move second is the remove
    board=node[0]
    currentPlayerPos=node[node[3]]
    otherPlayerPos=node[getOtherId(node[3])]
    
    currentPlayerNeigh=neighbors(board,currentPlayerPos)
    otherPlayerNeigh=neighbors(board,otherPlayerPos)

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
    

def alphabeta(node,depth,alpha,beta,maxPlayer,numFilled):
    if time()-startTime>maxTime:
        return None
    if isTerminal(node):
        t=terminalIsMe(node,maxPlayer)
        if t:
            return -10**5
        else:
            return 10**5
        
    if depth==0:
        return heuristic(node,maxPlayer,numFilled)
    
    if maxPlayer:
        val=-10**7
        kids=children(node)
        for child in kids:
            c=getChild(node,child)#gets child node
            #print c[0]
            #raw_input()
            ab=alphabeta(c,depth-1,alpha,beta,False,numFilled+1)
            if ab==None:
                return None

            val=max(val,ab)
            alpha=max(alpha,val)
            if beta<=alpha:
                break

    else:
        val=10**7
        kids=children(node)
        for child in kids:
            c=getChild(node,child)#turns node into the child node
            #print c[0]
            #raw_input()
            ab=alphabeta(c,depth-1,alpha,beta,True,numFilled+1)
            if ab==None:
                return None

            val=min(val,ab)
            beta=min(beta,val)
            if beta<=alpha:
                break


    return val

def minimax(node,depth,numFilled):#always the first call
    alpha=-10**7
    beta=10**7
    
    val=-10**7
    bestChild=None
    kids=children(node)
    for child in kids:
        c=getChild(node,child)#gets child node
        #print c[0]
        #raw_input()

        ab=alphabeta(c,depth-1,alpha,beta,False,numFilled+1)
        if ab==None:
            return None
        if ab>val:
            val=ab
            bestChild=child
        
        alpha=max(alpha,val)
        if beta<=alpha:
            break

    return bestChild

#specific to neighbor evaluation-----------------------------------------
def argmax(l):
    m=max(l)
    return l.index(m)

def neighborFind(node):#find the neighbor whose score is max
    kids=children(node)
    scores=[]
    for child in kids:
        c=getChild(node,child)
        myScore=bfsScore(c[0],c[node[3]])
        bScore=bfsScore(c[0],child[1])
        s=myScore+bScore
        scores.append(s)
    
    ind=argmax(scores)
    return kids[ind]

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
#---------------------------------------------------------------------

def play(board,pid):
    global startTime
    startTime=time()
    player=find(board,pid)
    enemy=find(board,getOtherId(pid))

    if pid==1:
        node=(board,player,enemy,1)
    else:
        node=(board,enemy,player,2)

    numFilled=numFilledSpaces(board)
    ans=minimax(node,6,numFilled)
    if ans==None:
        ans=neighborFind(node)
    return [ans[0],ans[1]]
