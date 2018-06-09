

import time
import sys

UP = (-1,0)
LEFT = (0,-1)
UPLEFT = (-1,-1)


LEFTARROW = '←'
UPARROW = '↑'
LEFTUPARROW = '↖'

DirectionMap = {LEFT:LEFTARROW, UP:UPARROW, UPLEFT:LEFTUPARROW}


class MatrixEntry(object):
    def __init__(self,position,cost,backpointers = []):
        self.position = position
        self.cost = cost
        self.backpointers = backpointers

class Matrix(object):
    '''
    this matrix is implemented by a list of lists
    '''
    def __init__(self,num_rows,num_columns,src,tgt):
        self.matrix = []
        self.num_rows = num_rows
        self.num_columns = num_columns
        self.src = src
        self.tgt = tgt

    def add_row(self,row):
        self.matrix.append(row)

    def add_entry(self,entry):
        if not self.matrix:
            self.matrix.append([entry])
        else:
            last_row_index = len(self.matrix) - 1
            if len(self.matrix[last_row_index]) + 1<= self.num_columns:
                self.matrix[last_row_index].append(entry)
            else:
                self.matrix.append([entry])

    def get_entry(self,i,j):
        return self.matrix[i][j]

    def min_distance(self):
        return self.get_entry(self.num_rows-1,self.num_columns-1).cost

    def pprint(self):
        out = [' ']+(' '.join('#'+self.tgt)).split()
        for c in out:
            print ('%5s' % c+' ' ,end='')
        print ()   

        i = 0
        src = '#' + self.src

        for row in self.matrix:
            out = [str(src[i])]
            for entry in row:
                cost = entry.cost 
                backpointers = ''.join(DirectionMap[p] for p in  entry.backpointers)
                out.append(backpointers+str(cost))

            for c in out:
                print ('%5s' % c+' ' ,end='')
            print ()
            i+=1
        print ('-'*65)

    def backtraces(self):
        backtraces = []
        temp_trace = [] #stack of (position,backpointers)


        current_position = (self.num_rows - 1,self.num_columns - 1)
        current_backpointers = self.get_entry(current_position[0],current_position[1]).backpointers[:] #复制是因为要在原矩阵上保留回指针信息，以备其他路径使用
        temp_trace.append((current_position,current_backpointers)) #push
        
        #while current_backpointers:
        #如果栈底（矩阵的右下角位置）还有回指针
        while temp_trace[0][1]:
            #取回指针链表最后一个作为新的位置所在
            current_position = (current_position[0] + current_backpointers[-1][0], current_position[1] + current_backpointers[-1][1])
            current_backpointers = self.get_entry(current_position[0],current_position[1]).backpointers[:]
            temp_trace.append((current_position,current_backpointers))
            
            #如果当前位置已经达到上边界或左边界或所有回指针已探测完毕
            while not current_backpointers:
                #如果当前位置是起点,添加此路径
                if current_position in [(1,0),(0,1),(0,0)]:
                    pos,bpointer = zip(*temp_trace)
                    backtraces.append(list(pos))
                
                if not temp_trace[0][1] :
                    break
                #回溯一个
                temp_trace.pop()
                #摘掉回溯之后的位置的最后一个回指针
                temp_trace[-1][1].pop()
                #更新当前位置和当前回指针
                current_position,current_backpointers = temp_trace[-1]


        return backtraces      






def construct_matrix(src,tgt,del_cost = 1,sub_cost = 2, ins_cost = 1, sleep_duration = 0.005):
    n = len(src)
    m = len(tgt)
    if src == '': 
        return m*ins_cost
    elif tgt == '':
        return n*del_cost
    else:
        dist_matrix = Matrix(n+1,m+1,src,tgt)
        initial_entry = MatrixEntry((0,0),0)
        dist_matrix.add_entry(initial_entry)
        #when transform from empty src to tgt, all we need is insertions
        #fill in the first line of the distance matrix
        for j in range(1,m+1):
            cost = dist_matrix.get_entry(0,j-1).cost+ins_cost
            new_entry = MatrixEntry((0,j),cost,[])
            dist_matrix.add_entry(new_entry)
        
        for i in range(1,n+1):
            cost = dist_matrix.get_entry(i-1,0).cost+del_cost
            dist_matrix.add_entry(MatrixEntry((i,0),cost,[]))

            for j in range(1,m+1):
                deletion = dist_matrix.get_entry(i-1,j).cost + del_cost
                insertion = dist_matrix.get_entry(i,j-1).cost + ins_cost
                substitution = dist_matrix.get_entry(i-1,j-1).cost +  (0 if src[i-1] == tgt[j-1] else sub_cost)
                
                min_dist = min([deletion,insertion,substitution])
                backpointers = [d for c,d in zip([deletion,insertion,substitution],[UP,LEFT,UPLEFT]) if c == min_dist]

                dist_matrix.add_entry(MatrixEntry((i,j),min_dist,backpointers))

        
    return dist_matrix


if __name__ == '__main__':
    src = 'intention'
    tgt = 'execution'
    dist_matrix = construct_matrix(src,tgt)
    print (dist_matrix.min_distance())
    dist_matrix.pprint()
    backtraces= dist_matrix.backtraces()
    for b in backtraces:
        print (b)