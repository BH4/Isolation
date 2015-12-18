from copy import deepcopy

def enemyid(pid):
    if pid==1:
        return 2
    return 1

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

def find(board,pid):
    for i,row in enumerate(board):
        for j,n in enumerate(row):
            if n==pid:
                return (i,j)

def change(board,pos,num):
    board[pos[0]][pos[1]]=num

def turn(board,move,remove,oldSpot,pid):
    #board=deepcopy(board)
    #oldSpot=find(board,pid)
    change(board,oldSpot,0)
    change(board,move,pid)
    change(board,remove,-1)

def undoTurn(board,oldSpot,remove,newSpot,pid):
    #newSpot=find(board,pid)
    change(board,remove,0)
    change(board,newSpot,0)
    change(board,oldSpot,pid)

def evaluation(board,pos):#heristic to calculate utility of pid's position
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

def utility(board,myPos,badGuyPos):
    myScore=evaluation(board,myPos)
    eScore=evaluation(board,badGuyPos)

    return myScore-eScore

def children(node):#a child is a set of two positions. first is the move second is the remove
    board=node[0]
    ppos=node[1]
    epos=node[2]
    pneigh=neighbors(board,ppos)
    eneigh=neighbors(board,epos)

    c=[]
    for p in pneigh:
        for e in eneigh:
            if not(p==e):
                c.append((p,e))

    return c
    

def minimax(node,depth,isMe):#node=(board,Ppos,Epos)
    #board=deepcopy(board)
    board=node[0]
    Ppos=node[1]
    Epos=node[2]

    if len(neighbors(board,Ppos))==0:
        if isMe:
            return -1
        return 100
    if depth==0:
        if isMe:
            return utility(board,Ppos,Epos)
        return utility(board,Epos,Ppos)

    kids=children(node)
    if isMe:
        bestValue=-1*(10**4)
        for c in kids:
            turn(board,c[0],c[1],Ppos,pid)
            val=minimax((board,Epos,c[0]),depth-1,False)
            bestValue=max(bestValue,val)
            undoTurn(board,Ppos,c[1],c[0],pid)
        return bestValue
    else:
        bestValue=10**4
        for c in kids:
            turn(board,c[0],c[1],Ppos,enemyid(pid))
            val=minimax((board,Epos,c[0]),depth-1,True)
            bestValue=min(bestValue,val)
            undoTurn(board,Ppos,c[1],c[0],enemyid(pid))
        return bestValue



def minimaxW(board,Ppos,Epos,depth):
    node=(board,Ppos,Epos)
    
    kids=children(node)
    bestValue=-1*(10**4)
    bestKid=None
    for c in kids:
        turn(board,c[0],c[1],Ppos,pid)
        val=minimax((board,Epos,c[0]),depth-1,False)
        undoTurn(board,Ppos,c[1],c[0],pid)

        if val>bestValue:
            bestValue=val
            bestKid=c

    return c



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
else:
    enemy,player=temp

ans=minimaxW(board,player,enemy,2)
print str(ans[0][0])+' '+str(ans[0][1])
print str(ans[1][0])+' '+str(ans[1][1])







    
