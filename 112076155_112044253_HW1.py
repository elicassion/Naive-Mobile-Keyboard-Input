import os,sys
import math as m
import random
import string
# import time

#Key Width equal to 1 key
keyWidth = 1.0
#Key coordinate for a 6 rows by 5 column keyboard
cord = [[(x + keyWidth/2.0,y + keyWidth/2.0) for x in range(5)] for y in range(6)]
T_INIT = 100
DELTA = 0.98
T_FIN = 1e-8
def copy_layout(layout):
    copied_layout = {}
    for k in layout:
        copied_layout[k] = (layout[k][0], layout[k][1])
    return copied_layout


def get_random_layout():
    # Call this function to a a randomized layout.
    # A layout is dictionary of key symbols(a to z) to it's (row, column) index
    cord_shuffle = [(x, y) for x in range(6) for y in range(5)]
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
    

    fp = open(data_path, 'r')
    content = fp.read()
    fp.close()
    freq_sum = 0
    tbl = {}
    for line in content.split('\n'): 
        word, freq, p = line.strip().split('\t')
        if len(word) == 1:
            continue
        freq = int(freq)        
        for i in range(0, len(word)-1):
            freq_sum += freq
            tbl[(word[i], word[i+1])] = tbl.get((word[i], word[i+1]), 0) + freq
    for k in tbl.keys():
        tbl[k] = tbl[k]*1.0 / freq_sum
    # print tbl
    return tbl

def FittsLaw(W,D):
    #implement the Fitt's Law based on the given arguments and constant
    a = 0.083
    b = 0.127
    return a+b*m.log(D*1.0/W+1, 2)

def computeAMT(layout, digram_table, exchange_pair=None, previous_cost=None):
    # Compute the average movement time
    if exchange_pair is None:
        MT=0
        keys = layout.keys()
        for i in range(len(keys)):
            for j in range(i+1, len(keys)):
                c1 = keys[i]
                c2 = keys[j]
                if c1 in '1234' or c2 in '1234':
                    continue
                x1, y1 = layout[c1]
                x2, y2 = layout[c2]
                d = m.sqrt((x1-x2)**2+(y1-y2)**2)
                MT += digram_table.get((c1, c2), 0)*FittsLaw(keyWidth, d)
                MT += digram_table.get((c2, c1), 0)*FittsLaw(keyWidth, d)
    else:
        MT = previous_cost
        keys = layout.keys()
        c1, c2 = exchange_pair
        # for cc in exchange_pair:
        for c in keys:
            if c in '1234' or c == c1 or c == c2:
                continue
            x1, y1 = layout[c1]
            x2, y2 = layout[c2]
            xc, yc = layout[c]
            d1 = m.sqrt((x1-xc)**2+(y1-yc)**2)
            d2 = m.sqrt((x2-xc)**2+(y2-yc)**2)
            f1 = FittsLaw(keyWidth, d1)
            f2 = FittsLaw(keyWidth, d2)

            MT += digram_table.get((c, c1), 0)*(f2-f1)
            MT += digram_table.get((c1, c), 0)*(f2-f1)
            MT += digram_table.get((c, c2), 0)*(f1-f2)
            MT += digram_table.get((c2, c), 0)*(f1-f2)

            # MT -= digram_table.get((c, c1), 0)*f1
            # MT -= digram_table.get((c1, c), 0)*f1

            # MT += digram_table.get((c, c2), 0)*f1
            # MT += digram_table.get((c2, c), 0)*f1

            # MT -= digram_table.get((c, c2), 0)*f2
            # MT -= digram_table.get((c2, c), 0)*f2

            # MT += digram_table.get((c, c1), 0)*f2
            # MT += digram_table.get((c1, c), 0)*f2
    return MT

def SA(num_iter, num_random_start, tbl):
    # Do the SA with num_iter iterations, you can random start by num_random_start times
    # the tbl arguments were the digram table
    r = 0
    final_result= ({},99999999)
    while r < num_random_start:
        layout = get_random_layout()
        k=0
        cost = computeAMT(layout, tbl)
        # print cost
        T = T_INIT
        # while T>=T_FIN: 
        while k<num_iter:
            keys =  layout.keys()
            c1, c2 = random.sample(string.ascii_lowercase, 2)
            new_cost = computeAMT(layout, tbl, (c1, c2), cost)
            # Accept layout
            if new_cost <= cost:
                layout[c1], layout[c2] = layout[c2], layout[c1]
                cost = new_cost
                # Record best layout
                if cost < final_result[1]:
                    final_result = (copy_layout(layout), cost)
                    print (cost)
            else:
                # print new_cost, cost, (new_cost-cost)/T
                # Accept layout by probability
                if m.exp((cost - new_cost)/T) > random.random():
                    layout[c1], layout[c2] = layout[c2], layout[c1]
                    cost = new_cost
            k += 1
            T *= DELTA
        r += 1
        print 'Random Start Round', r
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
    # st = time.time()
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
    # print (tbl[('t', 'h')])
    # print (tbl[('h', 'e')])
    # print (tbl[('o', 'f')])

    #Run SA
    result, cost = SA(k,rs,tbl)
    print "Optimal MT:", cost
    printLayout(result)
    print computeAMT(result, tbl)
    # print time.time() - st

    

