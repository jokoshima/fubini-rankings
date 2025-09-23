#!/usr/bin/env python
# coding: utf-8

# In[ ]:


## START: GENERATOR AND PRINTER FOR FUBINI RANKINGS AND PARKING FUNCTIONS


# In[2]:


# Prints everything on a separate line
def tidy_printer(arr):
    for i in range(len(arr)):
        print(arr[i])
    return


# In[3]:


# Checks if tuple is a parking function
def is_pf(pf):
    pf = sorted(pf)
    for i in range(len(pf)):
        if i+1 < pf[i]:
            return False
    return True


# In[4]:


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


# In[5]:


# Determine the outcome of a (valid!) Fubini ranking
def fubini_outcome(fr):
    named = [(fr[i],i+1) for i in range(len(fr))]
    named.sort()
    outcome = tuple([named[i][1] for i in range(len(fr))])
    return outcome


# In[6]:


def shifted_nondec_fubini(frs, k):
    nondec = []
    for i in range(len(frs)):
        if frs[i] == sorted(frs[i]):
            nondec.append([frs[i][j] + k for j in range(len(frs[i]))])
    return nondec


# In[7]:


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
    


# In[8]:


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


# In[9]:


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


# In[10]:


# Generate PF_n and FR_n AND the outcome map for the Fubini rankings (to be tidied up)
def all_rankings_per_outcome(n):
    #n = int(input("Length? "))
    frs = all_tuples_of_length(n)["FRs"]
    prs = Permutations(n)
    outcome_map = {tuple(prs[i]):[] for i in range(len(prs))}
    for i in range(len(frs)):
        outcome_map[fubini_outcome(frs[i])].append(frs[i])
    return outcome_map


# In[11]:


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

