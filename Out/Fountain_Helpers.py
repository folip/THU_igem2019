import struct
import random
import os
import numpy as np
import argparse
import logging
import sys
import operator
from hashlib import md5
from reedsolo import RSCodec
from math import ceil
from math import log, floor, sqrt
import random
import json
import numpy as np
from numpy.random import RandomState
import scipy.interpolate as inter
import csv
import math

xor_map = {
    'A':{
        'A': 'A',
        'C': 'T',
        'G': 'G',
        'T': 'C'
    },
    'C':{
        'A': 'C',
        'C': 'A',
        'G': 'T',
        'T': 'G'
    },
    'G':{
        'A': 'G',
        'C': 'T',
        'G': 'A',
        'T': 'C'
    },
    'T':{
        'A': 'T',
        'C': 'G',
        'G': 'C',
        'T': 'A'
    }
}
# 96
def xor_dna(d1, d2):
    if(len(d1) != len(d1)):
        logging.error("length not equal")
        return
    dr = ''.join([xor_map[c1][c2] for c1,c2 in zip(d1,d2)])
    return dr

#----------------------------------------------helper functions to calculate the soltion distribution---------------------------------------------------#
class Scanner:
    def __init__(self,max_repeat = 3, gc_interval = [0.45,0.55]):
        self.max_repeat = max_repeat
        self.gc_interval = gc_interval
        
    def scan_repeats(self,dna,record_position = False):
        repeats = []
        prv = dna[0]
        r_num = 1
        for i,c in enumerate(dna[1:]):
            if prv == c:
                r_num += 1
            else:
                if(r_num > self.max_repeat):
                    if(record_position):
                        repeats.append([prv,r_num,i-r_num+1])
                    else:
                        repeats.append([prv,r_num])
                r_num = 1
                prv = c

        if(r_num > self.max_repeat): 
                    if(record_position):
                        repeats.append([prv,r_num,i-r_num+1])
                    else:
                        repeats.append([prv,r_num])
        return repeats
    
    def max_repeats(self,dna):
        rs = self.scan_repeats(dna)
        if rs == []: return 0
        else: return max([r[1] for r in rs])
        
    def repeats_point(self,dna):
        rs = self.scan_repeats(dna)
        if rs == []: return 0
        else:
            return sum([r[1] / (self.max_repeat + 1) for r in rs])

    def Gc(self,dna):
        gc = dna.count('G') + dna.count('C')
        l = len(dna)
        return float(gc) / l
    
    def gc_pass(self,dna):
        if self.gc_interval[0]  < self.Gc(dna) < self.gc_interval[1]:
            return True
        else:
            return False
    
    def Pass(self,dna,with_primer = False):
        if self.gc_pass(dna) and self.repeats_point(dna)  == 0:
            return True
        else:
            return False
    
    def ave_gc(self,dnas):
        return sum([self.Gc(dna) for dna in dnas])/len(dnas)

    def rp_total(self,dnas):
        return(sum([self.repeats_point(dna) for dna in dnas]))

    def Entropy(self,labels, base=4):
        # 计算概率分布
        labels = list(labels)
        probs = pd.Series(labels).value_counts() / len(labels)
        # 计算底数为base的熵
        logging.debug(probs)
        en = stats.entropy(probs, base=base)
        return en
    
    def select_best(self,dnas):
        min_rp = 10000
        best_dna = dnas[0]
        for dna in dnas:
            if(self.gc_pass(dna)):
                if self.repeats_point(dna) < min_rp:
                    min_rp = self.repeats_point(dna)
                    best_dna = dna
        return best_dna,min_rp
                  
        
def gen_tau(S, K, delta):
    """The Robust part of the RSD, we precompute an
    array for speed
    """
    pivot = int(floor(K/S))

    val1 =  [S/K * 1/d for d in range(1, pivot)] 
    val2 =  [S/K * log(S/delta)] 
    val3 =  [0 for d in range(pivot, K)] 
 
    return val1 + val2 + val3

def gen_rho(K):
    """The Ideal Soliton Distribution, we precompute
    an array for speed
    """
    return [1.0/K] + [1.0/(d*(d-1)) for d in range(2, K+1)]



def gen_mu(K, S, delta):
    """The Robust Soliton Distribution on the degree of 
    transmitted blocks
    """

    tau = gen_tau(S, K, delta)
    rho = gen_rho(K)

    Z = sum(rho) + sum(tau)
    mu = [(rho[d] + tau[d])/Z for d in range(K)]
    return (mu, Z)

def gen_rsd_cdf(K, S, delta):
    """The CDF of the RSD on block degree, precomputed for
    sampling speed"""

    mu, Z = gen_mu(K, S, delta)
    cdf = np.cumsum(mu)
    return cdf, Z

class PRNG(object):
    """A Pseudorandom Number Generator that yields samples
    from the set of source blocks using the RSD degree
    distribution described above.
    """

    def __init__(self, K, delta, c, np = None):
        """Provide RSD parameters on construction
        # K is the number of segments
        # delta and c are parameters that determine the distribution
        #np is to use numpy random number generator which is faster
        """

        self.K = float(K)
        self.K_int = int(K)
        self.delta = delta
        self.c = c

        S = self.calc_S()
        cdf, Z = gen_rsd_cdf(K, S, delta)
        self.cdf = cdf
        self.Z = Z

        #self.inter = inter.interp1d(np.concatenate(([0], cdf)), range(0,K+1))
        self.np_rand = RandomState(1)
        self.np = np

        self.state = 1

    def calc_S(self):
        """ A helper function to calculate S, the expected number of degree=1 nodes
        """
  
        K = self.K
        S = self.c * log(self.K/self.delta) * sqrt(self.K) 
        self.S = S
        return S


    def get_S(self):
        return self.S


    def set_seed(self, seed):
        """Reset the state of the PRNG to the 
        given seed
        """

        self.state = seed
    
    def get_state(self):
        """Returns current state of the linear PRNG
        """

        return self.state


    def get_src_blocks_wrap(self, seed=None):
        #a wrapper function to get source blocks.
        #if np flag is on, it will use a numpy-based method.
        #otherwise, it will use the native python random function.
        #np is faster but in compatible with python random which implemented in previous versions.

        if self.np:
            return self.get_src_blocks_np(seed)
        else:
            return self.get_src_blocks(seed)

    def get_src_blocks(self, seed=None):
        """Returns the indices of a set of `d` source blocks
        sampled from indices i = 1, ..., K-1 uniformly, where
        `d` is sampled from the RSD described above.
        """

        if seed:
            self.state = seed

        blockseed = self.state
        random.seed(self.state)
        
        d = self._sample_d()

        nums = random.sample(range(self.K_int), d)
        return blockseed, d, nums


    def get_src_blocks_np(self, seed=None):
        """Returns the indices of a set of `d` source blocks
        sampled from indices i = 1, ..., K-1 uniformly, where
        `d` is sampled from the RSD described above.
        Uses numpy for speed.
        """

        if seed:
            self.state = seed


        blockseed = self.state
        self.np_rand.seed(self.state)
        
        d = self._sample_d_np()
        nums = self.np_rand.randint(0, self.K_int, d)
        return blockseed, d, nums

    def _sample_d_np(self):
        """Samples degree given the precomputed
        distributions above. Uses numpy for speed"""

        p = self.np_rand.rand()
        for ix, v in enumerate(self.cdf):
            if v > p:
                return ix + 1
        return ix + 1        


    def _sample_d_inter(self):
        """Samples degree given the precomputed
        distributions above using interpolation
        """

        p = random.random()
        return int(self.inter(p))+1 #faster than math.ceil albeit can return the wrong value...

    # Samples from the CDF of mu
    def _sample_d(self):
        """Samples degree given the precomputed
        distributions above"""

        p = random.random()

        for ix, v in enumerate(self.cdf):
            if v > p:
                return ix + 1
        return ix + 1

    def debug(self):


        return json.dumps(
            {
               'K': self.K,
               'delta': self.delta,
               'c' : self.c,
               'S' : self.S,
               #'cdf': self.cdf,
               'Z': self.Z ,
               'K_prime': self.K * self.Z
            }
        )
    
def lfsr(state, mask):
    #Galois lfsr:
    result = state
    nbits = mask.bit_length()-1
    while True:
        result = (result << 1)
        xor = result >> nbits
        if xor != 0:
            result ^= mask

        yield result

def lfsr32p():
    #this function returns a hard coded polynomial (0b100000000000000000000000011000101).
    #The polynomial corresponds to 1 + x^25 + x^26 + x^30 + x^32, which is known 
    #to repeat only after 32^2-1 tries. Don't change unless you know what you are doing.
    return 0b100000000000000000000000011000101

def lfsr32s():
    #this function returns a hard coded state for the lfsr (0b001010101)
    #this state is the inital position in the register. You can change it without a major implication.
    return 0b001010101

def test():
    #run the test to see a stream of seed by the polynomial
    for pattern in lfsr(0b001, 0b100000000000000000000000011000101):
        print(pattern)
        
    
#---------------------------------------------------------------screen------------------------------------------------------------#
def prepare(max_repeat):
    global As, Cs, Gs, Ts
    As = '0' * (max_repeat+1)
    Cs = '1' * (max_repeat+1)
    Gs = '2' * (max_repeat+1)
    Ts = '3' * (max_repeat+1)

def screen_repeat(drop, max_repeat, gc_dev):

    dna = drop.toDNA()
    return screen_repeat_dna(dna, max_repeat, gc_dev)
    

def screen_repeat_dna(dna, max_repeat, gc_dev):
    
    if As in dna or Cs in dna or Gs in dna or Ts in dna: 
        #logging.debug('long homo')
        return 0

    gc = dna.count("1") + dna.count("2")  
    gc = gc/(len(dna)+0.0)

    if (gc < 0.5 - gc_dev) or (gc > 0.5 + gc_dev):
        #logging.debug('gc out range')
        return 0
    return 1

def gc(dna):
    gc = dna.count("1") + dna.count("2")  
    gc = gc/float(len(dna)+0.0)
    return gc

def hamming_distance(x,y):

    d = 0
    for t in xrange(0, max(len(x), len(y))):
        if(x[t] != y[t]):
            d += 1
    return d

def restricted_float(x):
    #helper function from http://stackoverflow.com/questions/12116685/how-can-i-require-my-python-scripts-argument-to-be-a-float-between-0-0-1-0-usin
    x = float(x)
    if x < 0.0 or x > 1.0:
        raise argparse.ArgumentTypeError("%r not in range [0.0, 1.0]"%(x,))
    return x


#------------------------------------------------------------------transformers------------------------------------------------------------#
def byte_to_dna_s(s):
    #convert byte data (\x01 \x02) to DNA data: ACTC
    bin_data = ''.join('{0:08b}'.format(ord(s[t])) for t in range(0,len(s)))
    return bin_to_dna(bin_data)

def byte_to_dna(s):
    #convert byte data (\x01 \x02) to DNA data: ACTC
    bin_data = ''.join('{0:08b}'.format(s[t]) for t in range(0,len(s)))
    return bin_to_dna(bin_data)

def bin_to_dna(bin_str):
    s = ''.join(str(int(bin_str[t:t+2],2)) for t in range(0, len(bin_str),2)) #convert binary 2-tuple to 0,1,2,3
    return s.translate(trantab)

def byte_from_bin(s):
    #convert string like 01010101 to string of bytes like \x01 \x02 \x03
    return ''.join(chr(int(s[t:t+8],2)) for t in xrange(0, len(s), 8))
  
def byte_to_int_array(s):
    #convert a strong like \x01\x02 to [1,2,]
    a = list()
    for t in range(0, len(s)):
        a.append(ord(s[t]))
    return a
  
def int_to_dna(a):
    #a is an array of integers between 0-255.
    #returns ACGGTC
    bin_data = ''.join('{0:08b}'.format(element) for element in a) #convert to a long sring of binary values
    s = ''.join(str(int(bin_data[t:t+2],2)) for t in range(0, len(bin_data),2)) #convert binary array to a string of 0,1,2,3
    return s.translate(trantab)
  
def int_to_four(a):
    #a is an array of integers between 0-255.
    #returns 0112322102
    bin_data = ''.join('{0:08b}'.format(element) for element in a) #convert to a long sring of binary values
    return ''.join(str(int(bin_data[t:t+2],2)) for t in range(0, len(bin_data),2)) #convert binary array to a string of 0,1,2,3 def four_to_dna(s):
    return s.translate(trantab)
  
def four_to_dna(s):
    return s.translate(trantab)
 
def dna_to_four(s):
    return s.translate(revtab)

def dna_to_byte(dna_str):
    #convert a string like ACTCA to a string of bytes like \x01 \x02
    num = dna_str.translate(revtab)
    s = ''.join('{0:02b}'.format(int(num[t])) for t in range(0, len(num),1))
    data = b''.join(bytes([int(s[t:t+8],2)]) for t in range(0, len(s), 8))

    return data
  
def dna_to_int_array(dna_str):
    #convert a string like ACTCA to an array of ints like [10, 2, 4]
    num = dna_str.translate(revtab)
    s = ''.join('{0:02b}'.format(int(num[t])) for t in range(0, len(num),1))
    data = [int(s[t:t+8],2) for t in range(0,len(s), 8)]

    return data

intab = "0123"
outtab = "ACGT"

trantab = str.maketrans(intab, outtab)
revtab = str.maketrans(outtab, intab)

#---------------------------------------------------------------------xor and other manuplations---------------------------------------#
def split_header(data_str, header_bytes):
    data = data_str[header_bytes:]
    header_raw = data_str[:header_bytes]
    header_binary = ''.join('{0:08b}'.format(ord(header_raw[t])) for t in xrange(0,header_bytes))
    
    

    header = 0
    for t in xrange(0, len(header_binary)):

        header = header << 1
        header +=  int(header_binary[t])
    
    return (header, data)

def charN(str, N):
    if N < len(str):
        return str[N]
    return 'X'
# differ for adding a x?

def xor(ord_array1, ord_array2):
       return [ord1 ^ ord2 for (ord1,ord2) in zip(ord_array1,ord_array2)]
    
#def xor(str1, str2, length):
#   return ''.join(chr(ord(str1[i]) ^ ord(str2[i])) for i in range(length))
  
def xor_np(ord_array1, ord_array2):
    return np.bitwise_xor(ord_array1, ord_array2)

def xor_ord(ord_array1, ord_array2, length):
    #ord_array_res = [None] * length
    for i in range(length):
        #ord_array_res[i] = ord_array1[i] ^ ord_array2[i]
        ord_array1[i] = ord_array1[i] ^ ord_array2[i]
    return ord_array1#_res
  
def xor_bin(str1, str2):
    length = max(len(str1),len(str2))
    bytes = ''
    for i in range(length):
         byte_xor_dec = ord(charN(str1,i)) ^ ord(charN(str2,i))
         byte_xor_bin = "{0:08b}".format(byte_xor_dec)
         bytes = ''.join([bytes, byte_xor_bin])
    return bytes

prepare(3)

xor_map = {
    'A':{
        'A': 'A',
        'C': 'C',
        'G': 'G',
        'T': 'T'
    },
    'C':{
        'A': 'C',
        'C': 'A',
        'G': 'T',
        'T': 'G'
    },
    'G':{
        'A': 'G',
        'C': 'T',
        'G': 'A',
        'T': 'C'
    },
    'T':{
        'A': 'T',
        'C': 'G',
        'G': 'C',
        'T': 'A'
    }
}
def xor_dna(d1, d2):
    if(len(d1) != len(d1)):
        logging.error("length not equal")
        return
    dr = ''.join([xor_map[c1][c2] for c1,c2 in zip(d1,d2)])
    return dr

def file_compare(f1,f2):
    l1 = len(f1)
    l2 = len(f2)
    if(l1 != l2):
        print("size not equal:",l1,l2)
    dismatch = 0
    for i in range(min(l1,l2)):
        if(f1[i] != f2[i]):
            logging.debug("byte not equal at position %d",i)
            dismatch += 1
    #if(dismatch == 0 and l1 == l2):
        #print("all the same")
    #else:
     #   print(dismatch,"dismatch")
    return dismatch
#---------------------------------------------------------------------random---------------------------------------#
def happen(prob):
    i = random.uniform(0,1)
    if i<=prob:
        return 1
    else:
        return 0
    
def random_base():
    r = random.random()
    if(r < 0.25): 
        return 'A'
    elif(r < 0.5):
        return 'C'
    elif(r < 0.75):
        return 'G'
    else:
        return 'T'
    
def random_dna(num):
    return ''.join([random_base() for i in range(num)])
    
    
def write_csv(data, file_name = 'record.csv'):
    with open(file_name,'a') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', lineterminator='\n')
        csv_writer.writerow(data)
        csv_file.close()
 #---------------------------------------------to dna---------------------------------------------------------#

toB = {
    '1' : 'TA',
    '2' : 'AA',
    '3' : 'CC',
    ' ' : 'AC',
    '4' : 'TG',
    'e' : 'CA',
    't' : 'AG',
    'a' : 'CT',
    'o' : 'GA',
    'i' : 'GT',
    'n' : 'TC',
    's' : 'GG',
    'r' : 'TT',
    'h' : 'AT',
    'd' : 'CG',
    'l' : 'GC',
    }

toC = {
   'TA' : '1',
   'AA' : '2',
   'CC' : '3',
   'AC' : ' ',
   'TG' : '4',
   'CA' : 'e',
   'AG' : 't',
   'CT' : 'a',
   'GA' : 'o',
   'GT' : 'i',
   'TC' : 'n',
   'GG' : 's',
   'TT' : 'r',
   'AT' : 'h',
   'CG' : 'd',
   'GC' : 'l'
    }


toBc = {
    'u' : 'TA',
    'c' : 'AA',
    'm' : 'CC',
    'f' : 'AC',
    'y' : 'CA',
    'w' : 'AG',
    'g' : 'CT',
    'p' : 'GA',
    'b' : 'GT',
    'v' : 'TC',
    'k' : 'TG',
    'x' : 'TT',
    'q' : 'AT',
    'j' : 'CG',
    'z' : 'GC',
    }

toCc = {
    'TA' : 'u',
    'AA' : 'c',
    'CC' : 'm',
    'AC' : 'f',
    'CA' : 'y',
    'AG' : 'w',
    'CT' : 'g',
    'GA' : 'p',
    'GT' : 'b',
    'TC' : 'v',
    'TG' : 'k',
    'TT' : 'x',
    'AT' : 'q',
    'CG' : 'j',
    'GC' : 'z'
    }


toBn = {
    '1' : 'AC',
    '2' : 'CA',
    '3' : 'AG',
    '4' : 'GA',
    '5' : 'GT',
    '6' : 'TC',
    '7' : 'TG',
    '8' : 'CT',
    '9' : 'TA',
    '0' : 'CG'
    }

toCn = {
   'AC' : '1',
   'CA' : '2',
   'AG' : '3',
   'GA' : '4',
   'GT' : '5',
   'TC' : '6',
   'TG' : '7',
   'CT' : '8',
   'TA' : '9',
   'CG' : '0'
}

toBs = {
    ',' : 'AC',
    '.' : 'CA',
    '"' : 'AG',
    ';' : 'GA',
    '\n' : 'GT',
    '!' : 'TC',
    '?' : 'TG',
    '-' : 'CT',
    '=' : 'TA',
    '\'' : 'CG'
    }

toCs = {
   'AC' : ',',
   'CA' : '.',
   'AG' : '"',
   'GA' : ';',
   'GT' : '\n',
   'TC' : '!',
   'TG' : '?',
   'CT' : '-',
   'TA' : '=',
   'CG' : '\''
    }

def toBase(c):
    bas = ''
    if('A' <= c and 'Z' >= c):
        c = c.lower()
        bas += toB['3']
    if('a' <= c  and 'z' >= c or c == ' '):
        if(c in toB):
            bas += toB[c]
        else:
            bas += toB['4'] + toBc[c]
        return bas
    elif('0' <= c and '9' >= c):
        return toB['1'] + toBn[c]
    else:
        return toB['2'] + toBs[c]
    
def toDna(s):
    dna = ''
    for c in s:
        dna += toBase(c)
    return dna

def toStr(dna):
    sentence = ''
    i = 0
    while i < len(dna):
        if(i+1 >= len(dna)):
            print('index exceed')
            break
        base2 = dna[i:i+2]
        i += 2
        c = toC[base2]
      
        if 'a' <= c  and 'z' >= c or c == ' ':
            sentence += c
            continue
        elif '4' == c:
            if(i+1 >= len(dna)):
                print('index exceed')
                break
            base2 = dna[i:i+2]
            i += 2
            sentence += toCc[base2]
            continue
        #uncaptitalized letter
        
        if '3' == c:
            if(i+1 >= len(dna)):
                print('index exceed')
                break
            base2 = dna[i:i+2]
            i += 2
            c = toC[base2]
            if '4' != c :
                sentence += c.upper()
                continue
            else:
                if(i+1 >= len(dna)):
                    print('index exceed')
                    break
                base2 = dna[i:i+2]
                i += 2
                sentence += toCc[base2].upper()
                continue
        #captitalized letter 
        
        if('1' == c):
            if(i+1 >= len(dna)):
                print('index exceed')
                break
            base2 = dna[i:i+2]
            i += 2
            sentence += toCn[base2]
            continue 
            
        if('2' == c):
            if(i+1 >= len(dna)):
                print('index exceed')
                break
            base2 = dna[i:i+2]
            i+=2
            sentence += toCs[base2]
            continue
        
        #logging.debug(sentence)
    return sentence

def to_dna_byte(str):
    b = bytes(str,encoding = 'ascii')
    logging.debug(b)
    return byte_to_dna(b)

def num_to_dna(num, qua_len):
    arr = []
    while True:
        lef = num % 4
        arr.append(lef)
        num = int(num / 4)
        if 0 == num:
            break
    outString = ''
    for n in arr:
        c = ''
        if(0 == n):
            c = 'A'
        elif(1 == n):
            c = 'C'
        elif(2 == n):
            c = 'G'
        elif(3 == n):
            c = 'T'
        outString = c + outString
    dl = qua_len - len(arr)
    if(dl < 0):
        logging.error('space not enough for encoding num')
        return -1
    elif(dl == 0):
        return outString
    else:
        return 'A' * dl + outString
    return outString