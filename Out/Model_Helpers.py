import pandas as pd
import math
import random
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import numpy as np

c2u_rate = 30  #@param {type: "slider", min: 0, max: 40}
depurination_rate = 20  #@param {type: "slider", min: 0, max: 30}
enzyme_type = "proof_reading"  #@param ['proof_reading', 'non_proof_reading']
ref_half_time = 2000 
#@markdown ---
#@markdown **PCR**:
primer_length = 5 #@param {type:"number"}
amplification_base_rate = 1.8 #@param {type: "number"}
ref_target_num = 100000  #@param {type: "number"}
#@markdown ---
#@markdown **error within molecules**
error_A = 0.75 #@param {type: "slider",min:0, max:2, step:0.01}
error_A2C = 0.2 #@param {type: "slider",min:0, max:1, step:0.01}
error_A2G = 0.3 #@param {type: "slider",min:0, max:1, step:0.01}
error_A2T = 0.5 #@param {type: "slider",min:0, max:1, step:0.01}
#@markdown ---
error_C = 1 #@param {type: "slider",min:0, max:2, step:0.01}
error_C2A = 0.2 #@param {type: "slider",min:0, max:1, step:0.01}
error_C2T = 0.3 #@param {type: "slider",min:0, max:1, step:0.01}
error_C2G = 0.5 #@param {type: "slider",min:0, max:1, step:0.01}
#@markdown ---
error_T = 1 #@param {type: "slider",min:0, max:2, step:0.01}
error_T2A = 0.2 #@param {type: "slider",min:0, max:1, step:0.01}
error_T2C = 0.3 #@param {type: "slider",min:0, max:1, step:0.01}
error_T2G = 0.5 #@param {type: "slider",min:0, max:1, step:0.01}
#@markdown ---
error_G = 1 #@param {type: "slider",min:0, max:2, step:0.01}
error_G2A = 0.2 #@param {type: "slider",min:0, max:1, step:0.01}
error_G2T = 0.3 #@param {type: "slider",min:0, max:1, step:0.01}
error_G2C = 0.5 #@param {type: "slider",min:0, max:1, step:0.01}

def fake_DNA_generator(length):
    DNA = []
    for i in range(length):
        DNA.append(random.randint(0,3))
    return DNA

dna = fake_DNA_generator(100)

def print_dna(DNA):
    length  = len(DNA)
    dna_trans = "ACGT"
    dna_string = ""
    for base in DNA:
        dna_string += dna_trans[base]
    print(dna_string)

def gc(DNA):
    gc = 0 
    length = len(DNA)
    for base in DNA:
        if base == 1 or base == 2:
            gc += 1
    gc = gc/length
    return gc

def PCR_para(DNA):
    key_sequence = DNA[-(4+primer_length):][0:4]
    PCR_para = 1.8
    for b in key_sequence:
        if b == 2 or b == 1:
            PCR_para += 0.018 * (1+ random.uniform(0,0.015))
        else:
            PCR_para -= 0.018* (1+ random.uniform(0,0.015))
    return PCR_para

def ks_dna(DNA):
    ks = DNA[-(4+primer_length):][0:4]
    return ks


def happen(prob):
    i = random.uniform(0,1)
    if i<=prob:
        return 1
    else:
        return 0

def who_in_3(prob1,prob2):
    i = random.uniform(0,1)
    if i<= prob1:
        return 0
    elif i<= (prob1 + prob2):
        return 1
    else:
        return 2
    
def sequencing_result(dna):
    rs = []
    l = len(dna)
    for i in range(l):
        # judge wether to insert, but we skip this this time 
        # judge wether to delete
        #if(happen(0.01)):
         #   continue
        if dna[i] == '0' :#A
            if(happen(0.01)):
                base_to = who_in_3(0.3,0.4)
                rs.append(base_to+1)
            else:
                rs.append(dna[i])
                
        if dna[i] == '2' :#G
            if(happen(0.01)):
                base_to = who_in_3(0.3,0.4)
                if base_to != 2:
                    rs.append(base_to+1)
                else :
                    rs.append(base_to)
            else:
                rs.append(dna[i])
       
        if dna[i] == '3' :#T
                if(happen(0.01)):
                    base_to = who_in_3(0.3,0.4)
                    rs.append(base_to)
                else:
                    rs.append(dna[i])
        
        if dna[i] == '1' :#C
            if(happen(0.01)):
                base_to = who_in_3(0.3,0.4)
                if base_to == 0:                
                    rs.append(base_to)
                else:
                    rs.append(base_to+1)
            else:
                rs.append(dna[i])
    return rs 

def diff(dna,s_dna):
    l1 = len(dna)
    l2 = len(s_dna)
    l = min(l1,l2)
    dif = 0
    for i in range(l):
        if dna[i] != s_dna[i]:
            dif += 1
    print(dif)
   
#@title helper functions
#@markdown * random_pick
#@markdown * get_index in random_pick
#@markdown * random_pick_test
def get_index(list,value):
    lo = 0
    hi = len(list)
    if(value < list[0]):
        return 0
    while lo < hi:
        mid = int((lo + hi)/2)
        if(list[mid] < value):
            lo = mid 
        else:
            hi = mid
        if hi - lo == 1:
            return hi
    return hi

# random_pick test

def random_pick(pick_num, cumu_probs, out):
    for i in range(0,pick_num): #repeat pick_num times
        x = random.uniform(0,1)
        sequence_index = get_index(cumu_probs,x)
        out[sequence_index] += 1
    return        
