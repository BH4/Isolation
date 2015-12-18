from copy import deepcopy

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

def heuristic(node,maxPlayer):
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
    return (myScore-3*oScore)*filledSpaces

def children(node):#a child is a set of two positions. first is the move second is the remove
    board=node[0]
    currentPlayerPos=node[node[3]]
    otherPlayerPos=node[getOtherId(node[3])]
    
    currentPlayerNeigh=neighbors(board,currentPlayerPos)
    otherPlayerNeigh=neighbors(board,otherPlayerPos)

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
    

def alphabeta(node,depth,alpha,beta,maxPlayer):
    if isTerminal(node):
        t=terminalIsMe(node,maxPlayer)
        if t:
            return -10**5
        else:
            return 10**5
        
    if depth==0:
        return heuristic(node,maxPlayer)
    
    if maxPlayer:
        val=-10**7
        kids=children(node)
        for child in kids:
            c=getChild(node,child)#gets child node
            ab=alphabeta(c,depth-1,alpha,beta,False)

            val=max(val,ab)
            alpha=max(alpha,val)
            if beta<=alpha:
                break

    else:
        val=10**7
        kids=children(node)
        for child in kids:
            c=getChild(node,child)#turns node into the child node
            ab=alphabeta(c,depth-1,alpha,beta,True)

            val=min(val,ab)
            beta=min(beta,val)
            if beta<=alpha:
                break


    return val

def minimax(node,depth):#always the first call
    alpha=-10**7
    beta=10**7
    
    val=-10**7
    bestChild=None
    kids=children(node)
    for child in kids:
        c=getChild(node,child)#gets child node
        #print c[0]
        #raw_input()

        ab=alphabeta(c,depth-1,alpha,beta,False)
        if ab>val:
            val=ab
            bestChild=child
        
        alpha=max(alpha,val)
        if beta<=alpha:
            break

    return bestChild


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

ans=minimax(node,3)
print str(ans[0][0])+' '+str(ans[0][1])
print str(ans[1][0])+' '+str(ans[1][1])

