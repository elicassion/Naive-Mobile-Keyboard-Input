import os,sys
import math as m
import random
import string

#Key Width equal to 1 key
keyWidth = 1.0
#Key coordinate for a 6 rows by 5 column keyboard
cord = [[(x + keyWidth/2.0,y + keyWidth/2.0) for x in range(5)] for y in range(6)]


def get_random_layout():
    # Call this function to a a randomized layout.
    # A layout is dictionary of key symbols(a to z) to it's (row, column) index
    cord_shuffle = [(x ,y) for x in range(6) for y in range(5)]
    random.shuffle(cord_shuffle)

    layout={}
    i=0
    for lt in string.ascii_lowercase:
        layout[lt]=cord_shuffle[i]
        i+=1
    # Since there are 30 slots for a 6*5 keyboard, 
    # we use dummy keys to stuff remaining keys
    layout['1']=cord_shuffle[-1]
    layout['2']=cord_shuffle[-2]
    layout['3']=cord_shuffle[-3]
    layout['4']=cord_shuffle[-4]

    return layout


def makeDigramTable(data_path):
    # Make a Digram Table , which is a dictionary with key format (letter_i,letter_j) to it's Pij
    # You could safely ignore words that have only 1 character when constructing this dictionary
    
#    fp = open(data_path)
#    content=fp.read()
#    fp.close()

    tbl={}

    return tbl

def FittsLaw(W,D):
    #implement the Fitt's Law based on the given arguments and constant
    a = 0.083
    b = 0.127
    return 


def computeAMT(layout, digram_table):
    # Compute the average movement time
    MT=0

    return MT

def SA(num_iter, num_random_start, tbl):
    # Do the SA with num_iter iterations, you can random start by num_random_start times
    # the tbl arguments were the digram table

    final_result= ({},0.0)
#    while r < num_random_start:
#        starting_state = get_random_layout()
#        k=0

#        cost = computeAMT(starting_state,tbl)
#        while k<num_iter:
            #Do something


    #--------you should return a tuple of (optimal_layout,optimal_MT)----
    return final_result

def printLayout(layout):
    # use this function to print the layout
    keyboard= [[[] for x in range(5)] for y in range(6)]
    for k in layout:
        r=layout[k][0]
        c=layout[k][1]
        keyboard[r][c].append(k)
    for r in range(6):
        row=''
        for c in range(5):
            row+=keyboard[r][c][0]+'  '
        print row

if __name__ == '__main__':

    if len(sys.argv)!=4:
        print "usage: hw1.py [num_SA_iteration] [num_SA_random_start] [dataset_path]"
        exit(0)
    
    k=int(sys.argv[1])
    rs=int(sys.argv[2])
    data_path=sys.argv[3]

    # Test Fitt's Law
    print FittsLaw(10,10)
    print FittsLaw(20,5)
    print FittsLaw(10.5,1)

    #Construct Digram Table
    tbl = makeDigramTable(data_path)

    #Run SA
    result, cost = SA(k,rs,tbl)
    print "Optimal MT:", cost
    printLayout(result)

    

