#!/usr/bin/env python
# coding: utf-8

# In[ ]:


## START: GENERATOR AND PRINTER FOR FUBINI RANKINGS AND PARKING FUNCTIONS


# In[18]:


# Prints everything on a separate line
def tidy_printer(arr):
    for i in range(len(arr)):
        print(arr[i])
    return


# In[19]:


# Checks if tuple is a parking function
def is_pf(pf):
    pf = sorted(pf)
    for i in range(len(pf)):
        if i+1 < pf[i]:
            return False
    return True


# In[34]:


# Checks if tuple is a Fubini ranking
def is_fr(fr):
    ranks = sorted(list(set(fr)))
    count = [fr.count(i) for i in ranks]
    if ranks[0] != 1:
        return False
    pos = 1
    for i in range(len(ranks)):
        if pos != ranks[i]: 
            return False
        pos += count[i]
    return True


# In[ ]:


# MATT
# Check for Unit Fubini ranking
def is_unit_fr(fr):
    if is_fr(fr)==False:
        return False
    for i in range(len(fr)):
        if fr.count(i+1) > 2:
            return False
    return True


# In[21]:


# This checks if any ties exceed more than l
def tiechecker(l,fr):
    if is_fr(fr) == False:
        return False
    for i in range(len(fr)):
        if fr.count(i+1) > l:
            return False
    return True


# In[ ]:


# MATT
# this function takes in a Fubini ranking, and checks if the indices x, x+1, x+2, ..., y  form a tie.
def tie_scanner(fub,x,y):
    if len(set(fub[x-1:y]))==1:
        return True
    return False


# In[ ]:


# MATT
# this function does what tie_scanner does, but also checks if the tie is a certain value
# x,y = starting and ending indices of the tie, i = desired value of the tie
def tie_scanner2(fub,x,y,i):
    if len(set(fub[x-1:y])) == 1 and fub[x]==i:
        return True
    return False


# In[ ]:


# MATT
# This generates all of the Fubini rankings of length n
def Fubini(n): 
    Fubs = [] # this will store the fubini's
    for pf in ParkingFunctions(n):
        if is_fr(pf) == True:
            Fubs.append(pf)
    return Fubs


# In[ ]:


# MATT
# This function generates all of the weakly increasing Fubini's
def weakly_increasing_Fubini(n):
    A = [] # this will store all of the weakly increasing Fubini's
    for fub in Fubini(n):
        if sorted(fub) not in A:
            A.append(sorted(fub))
    return A


# In[ ]:


# MATT
# This computes all of the unit Fubini's of length n
def UnitFubini(n):
    X = list(range(1,n+1))
    S = ParkingFunctions(n) #Tuples(X,len(X))
    A = [] # this will store the unit fubini's
    for s in S:
        if is_unit_fr(s)==True:
            A.append(s)
    return A


# In[ ]:


# MATT
# This computes all of the Fubini's of length n with ties no more than ell
def ell_Fubini(n,k):
    X = list(range(1,n+1))
    S = ParkingFunctions(n) #Tuples(X,len(X))
    A = [] # this will store the unit fubini's
    for s in S:
        if tiechecker(k,s)==True:
            A.append(s)
    return A


# In[ ]:


# MATT
# This computes the weakly increasing ell-Fubini rankings of length n
def weakly_increasing_ell_Fubini(n,ell):
    A = [] # this will store the weakly increasing ell-Fubini's
    for fub in weakly_increasing_Fubini(n):
        if tiechecker(ell,fub) == True:
            A.append(fub)
    return A


# In[ ]:


# MATT
# This function determines all the l-Fubini's that have a tie at a specific consecutive string of indices
# n= length, ell= ell-fubini, x,y = starting / ending indices of the tie, i= desired rank of tie
def Fubini_with_VERY_specific_tie(n, x, y, i):
    A = [] # this will store all the Fubini's that have a tie of rank i at indices x through y
    for fub in ell_Fubini(n,ell):
    #for fub in weakly_increasing_Fubini(n):#ell_Fubini(n,ell):
        if tie_scanner2(fub,x,y,i) == True:
            A.append(fub)
    return A


# In[ ]:


# MATT
# This function determins all of the weakly increasing ell-Fubini rankings with a tie between indices x through y at rank i
# n= length, ell= ell Fubini, x/y = starting/ending index, i= rank of the tie
def weak_inc_ell_Fubini_with_specific_tie(n,ell,x,y,i):
    A = [] # this will store the Fubini's you want
    for fub in weakly_increasing_ell_Fubini(n,ell):
        if tie_scanner2(fub,x,y,i) == True:
            A.append(fub)
    return A


# In[22]:


# Determine the outcome of a (valid!) Fubini ranking
def fubini_outcome(fr):
    named = [(fr[i],i+1) for i in range(len(fr))]
    named.sort()
    outcome = tuple([named[i][1] for i in range(len(fr))])
    return outcome


# In[23]:


def shifted_nondec_fubini(frs, k):
    nondec = []
    for i in range(len(frs)):
        if frs[i] == sorted(frs[i]):
            nondec.append([frs[i][j] + k for j in range(len(frs[i]))])
    return nondec


# In[24]:


# Determine the FR cause set of a permutation

from sage.combinat.cartesian_product import CartesianProduct_iters

def cause_set(pr):
    pr.append(0)             # so every run can be captured
    runs = []
    run_sizes = []
    shifts = []
    run_start = 0
    for i in range(1,len(pr)):
        if pr[i] < pr[i-1]:
            shifts.append(run_start)
            runs.append([pr[i] for i in range(run_start, i)])
            run_sizes.append(i-run_start)
            run_start = i
            
    run_outcomes = [[] for i in range(len(run_sizes))]
    for i in range(len(run_sizes)):
        shifted_frs = shifted_nondec_fubini(all_tuples_of_length(run_sizes[i])["FRs"], shifts[i])
        run_outcomes[i] = [tuple(el) for el in shifted_frs]
    inv = Permutation(pr[:-1]).inverse()
    cp = cartesian_product(run_outcomes)
    causes = [inv.action([a for b in el for a in b]) for el in cp]
    return causes
    


# In[ ]:


# MATT
# this determines all of the Fubini rankings of length n with outcome pi
# NOTE: pi must be entered as as [list], i.e. pi=[1,2,3,4]
def permutation_outcome(pi):
    X = Fubini(len(pi))
    A = [] # this will store all of the fubini with outcome pi
    for x in X:
        y = ParkingFunction(list(x))
        if y.cars_permutation()==pi:
            A.append(x)
    return A


# In[ ]:


# MATT
# This determines all of the ell-Fubini's of length n with outcome pi
# NOTE: pi must be entered as [list], i.e. pi = [1,2,3,4]
def permutation_outcome2(pi,ell):
    X = UnitFubini(len(pi))
    X = ell_Fubini(len(pi),ell)
    A = [] # this will store all of the unit fubini with outcome pi
    for x in X:
        y = ParkingFunction((list(x)))
        if y.cars_permutation() == pi:
            A.append(x)
    return A


# In[25]:


# Generates PF_n and FR_n
def all_tuples_of_length(n):
    #n = int(input("Length? "))
    nset = range(1, n+1)
    tuples = Tuples(nset, n)
    frs = []
    not_frs = []
    for i in range(len(tuples)):
        if is_pf(tuples[i]):
            if is_fr(tuples[i]): 
                frs.append(tuples[i])
            else:
                not_frs.append(tuples[i])
    return {"FRs":frs, "Not FRs":not_frs}


# In[39]:


# This computes all of the Fubini's of length n with ties no more than ell
def ell_fubini(n,l):
    S = ParkingFunctions(n)
    A = [] # this will store the l-Fubini rankings
    for s in S:
        if tiechecker(l,list(s))==True:
            A.append(s)
    return A


# In[36]:


# This determines all of the ell-Fubini's of length n with outcome p
# NOTE: pi must be entered as [list], i.e. pi = [1,2,3,4]
def permutation_outcome2(n,l,p):
    X = ell_fubini(n,l)
    A = [] # this will store all of the unit fubini with outcome pi
    for x in X:
        y = ParkingFunction((list(x)))
        if y.cars_permutation() == p:
            A.append(x)
    return A


# In[28]:


# Tests if a specific function is a PF and a FR
def evaluate_single_tuple():
    f = list(input("Please separate with commas: ").split(","))
    f = [int(i) for i in f]
    print(f)
    truth_pf = "not "
    truth_fr = "not "
    if is_pf(f):
        truth_pf = ""
    if is_fr(f):
        truth_fr = ""
    print(str(f) + " is " + truth_pf + "a parking function")
    print(str(f) + " is " + truth_fr + "a Fubini ranking")
    return


# In[29]:


# Generate PF_n and FR_n AND the outcome map for the Fubini rankings (to be tidied up)
def all_rankings_per_outcome(n):
    #n = int(input("Length? "))
    frs = all_tuples_of_length(n)["FRs"]
    prs = Permutations(n)
    outcome_map = {tuple(prs[i]):[] for i in range(len(prs))}
    for i in range(len(frs)):
        outcome_map[fubini_outcome(frs[i])].append(frs[i])
    return outcome_map


# In[30]:


# Counts number of Fubini rankings for which a given permutation is an outcome and groups permutations by that number
def permutations_per_outcome_number(n):
    outcome_map = all_rankings_per_outcome(n)
    partition = {2^i:[] for i in range(n)}
    for pr in outcome_map.keys():
        # Just in case...
        if not math.log(len(outcome_map[pr]), 2).is_integer():
            print("Oh my god! Not a power of 2!")
        partition[len(outcome_map[pr])].append(pr)
    return partition


# In[71]:


# Computes l-Pingala numbers by computing all (l-i)-Pingala numbers.
def pingala(n, l):
    numbers = [2^i for i in range(l+1)]
    for i in range(l+1, n):
        newnum = sum(numbers[i-l-1:i])
        numbers.append(newnum)
    return numbers


# In[82]:


# Checks if the inverse outcome of a permutation is enumerated by the product defined in Theorem 5.
def check_pingala_conjecture(p, l):
    runs = Permutation(p).runs()
    small_runs = [len(run) for run in runs if len(run) <= l]
    big_runs = [len(run) for run in runs if len(run) > l]
    pingalas = pingala(max(big_runs), l)
    print(pingalas)
    lfr = permutation_outcome2(len(p),l+1,p)
    product = []
    for el in small_runs:
        product.append(pow(2,el-1))
    for el in big_runs:
        product.append(pingalas[el-1])
    prod = 1
    for el in product:
        prod *= el
    print(prod)
    print(len(lfr))


# In[83]:


# MATT
# Determines the outcome set partition (OSP) and outcome from a Fubini ranking.
def OSP_Outcome_test(fub):
    X = OrderedSetPartition(fub)
    y = ParkingFunction(list(fub))
    outcome = y.cars_permutation()
    return('fub= ',fub, 'OSP(fub)= ', X,'outcome= ', outcome)


# In[ ]:


# MATT
# Determines the OSP for every Fubini ranking of length N. 
def OSP_OUTCOME_DATA(N):
    A = Fubini(N)
    for x in A:
        y = ParkingFunction(list(x))
        outcome = y.cars_permutation()
        print(x, OrderedSetPartition(x), outcome)


# In[14]:


# Dialogue to decide what we want the code to do
def dialogue():
    protocol = input("Input 's' for testing a single tuple, \n'a' to generate all tuples of some length, \n'o' to group all Fubini rankings by outcome, \n'p' to group premutations by number of associated rankings, \n'c' to generate the Fubini cause set of a permutation:\n")
    if protocol == "s":
        evaluate_single_tuple()
    elif protocol == "a":
        n = int(input("Length? "))
        tuples = all_tuples_of_length(n)
        frs = tuples["FRs"]
        not_frs = tuples["Not FRs"]
        print("# of parking functions: " + str(len(frs) + len(not_frs)))
        print("# of Fubini rankings: " + str(len(frs)))
        pr = input("Print all? (Y/N):").lower()
        if pr == "y":
            print("Fubini rankings:")
            tidy_printer(frs)
            print("Parking functions that are not Fubini rankings")
            tidy_printer(not_frs)
    elif protocol == "o":
        n = int(input("Length? "))
        outcome_map = all_rankings_per_outcome(n)
        for pr in outcome_map.keys():
            print(pr, " has ", len(outcome_map[pr]), " Fubini rankings: ")
            tidy_printer(outcome_map[pr])
    elif protocol == "p":
        n = int(input("Length? "))
        part = permutations_per_outcome_number(n)
        for i in sorted(part.keys()):
            print("There are", len(part[i]), "permutations that are the outcome of", i, "Fubini rankings:")
            tidy_printer(part[i])
    elif protocol == 'c':
        pr = list(input("Permutation (please separate with commas): ").split(","))
        pr = [int(el) for el in pr]
        causes = cause_set(pr)
        tidy_printer(causes)
    else:
        print("Shut up!")


# In[17]:


dialogue()


# In[ ]:




