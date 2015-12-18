from copy import deepcopy
from time import time
from random import randint



def getOtherId(pid):
    if pid==1:
        return 2
    return 1

def find(board,pid):
    for i,row in enumerate(board):
        for j,n in enumerate(row):
            if n==pid:
                return (i,j)

#def onBoard(board,pos):
#    if pos[0]<0 or pos[1]<0 or pos[0]>=7 or pos[1]>=7:
#        return False

def legal(board,pos):
    if pos[0]<0 or pos[1]<0 or pos[0]>=7 or pos[1]>=7:
        return False
    if board[pos[0]][pos[1]]==0:
        return True
    return False

def legalBlock(board,pos,currPlayer):
    if pos[0]<0 or pos[1]<0 or pos[0]>=7 or pos[1]>=7:
        return False
    if board[pos[0]][pos[1]]==getOtherId(currPlayer) or board[pos[0]][pos[1]]==-1:
        return False
    return True

def neighbors(board,pos):
    n=[]
    moves=[(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,1),(-1,-1),(1,-1)]
    for m in moves:
        test=(pos[0]+m[0],pos[1]+m[1])
        if legal(board,test):
            n.append(test)
    return n

def blockNeighbors(board,pos,currPlayer):
    n=[]
    moves=[(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,1),(-1,-1),(1,-1)]
    for m in moves:
        test=(pos[0]+m[0],pos[1]+m[1])
        if legalBlock(board,test,currPlayer):
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
    otherPlayerNeigh=blockNeighbors(board,otherPlayerPos,node[3])

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
    if not depth in depthsTimed:
        dTime=time()-startTime
        n1=len(neighbors(node[0],node[1]))
        n2=len(neighbors(node[0],node[2]))
        
        mult=(n1*n2)**(9-depth)
        if mult*dTime>maxTime:
            global minDepth
            minDepth=depth
            
    if isTerminal(node):
        t=terminalIsMe(node,maxPlayer)
        if t:
            return -10**5
        else:
            return 10**5
        
    if depth<=minDepth:
        return heuristic(node,maxPlayer,numFilled)
    
    if maxPlayer:
        val=-10**7
        kids=children(node)
        for child in kids:
            c=getChild(node,child)#gets child node
            #print c[0]
            #raw_input()
            ab=alphabeta(c,depth-1,alpha,beta,False,numFilled+1)

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
        if ab>=val:
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

maxTime=5000
minDepth=0
depthsTimed=[]
startTime=time()

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

if pid==1:
    player,enemy=temp
    node=(board,player,enemy,1)
else:
    enemy,player=temp
    node=(board,enemy,player,2)

numFilled=numFilledSpaces(board)
move,remove=minimax(node,9,numFilled)
if minDepth>3:
    move,remove=neighborFind(node)
print str(move[0])+' '+str(move[1])
print str(remove[0])+' '+str(remove[1])
