import struct
import random
import os
import numpy as np
import pandas as pd 
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
import math
import pprint
from Fountain_Helpers import *
import csv
#----------------------------------------------------Droplet-------------------------------------------------#  
class Droplet:
    def __init__(self, data, seed, num_chunks = None, rs = 0, rs_obj = None, degree = None):
        #num_chunks is a list of the orignal packets numbers used to xor 
        #rs is the number of Reed Solomon symbols to add to the message

        self.data = data

        self.seed = seed
        self.num_chunks = set(num_chunks)
        self.rs = rs
        self.rs_obj = rs_obj
        self.degree = degree

        self.DNA = None

    def chunkNums(self):
        return self.num_chunks
    
    def chunkNum(self):
        return self.degree
    
    def toDNA(self, flag = None):
        #this function wraps the seed, data payload, and Reed Solomon.

        if self.DNA is not None:
            return self.DNA
        
        self.DNA = int_to_four(self._package())
        return self.DNA
    
    def chunkStr(self):
        num = 0
        s = ''
        for i in self.num_chunks:
            if(6 == num):
                s += '...'
                break
            s+= str(i) + ' '
        num += 1
        return s
        

    def to_human_readable_DNA(self):
        #converts the DNA into a human readable [A,C,G,T
        return four_to_dna(self.toDNA())
        
    def _package(self):
        #this function converts the seed to a list of 4bytes HARD CODED!!!
        #adds the seed to the data (list of integers)
        #computes a reed solomon on the seed+data.
        #returns everything.

        seed_ord = self.seed.to_bytes(4, byteorder = 'big')
            #converting the seed into exectly four bytes.
        message = seed_ord + bytes(self.data)
        
        if self.rs > 0:
            message = self.rs_obj.encode(message) #adding RS symbols to the message

        return message
    
#----------------------------------------------------Fountain-------------------------------------------------#      
class DNAFountain:

    def __init__(self, 
                file_in, 
                file_size, 
                chunk_size,
                alpha, 
                stop = None,
                rs = 0, 
                c_dist = 0.1, 
                delta = 0.5, 
                np = False,
                max_homopolymer = 3,
                gc = 0.05
                ):

        #alpha is the redundency level
        #stop is whether we have a limit on the number of oligos
        #chunk_size and file_size are in bytes
        #rs is the number of bytes for reed-solomon error correcting code over gf(2^8).
        #c_dist is a parameter of the degree distribution
        #delta is a parameter of the degree distribution
        #np: should we use numpy random number generator? Faster, but incompatible for previous versions
        #max_homopolymer: the largest homopolymer allowed
        #gc: the allowable range of gc +- 50%

        #things realted to data:
        self.file_in = file_in
        self.chunk_size = chunk_size
        self.num_chunks = int(ceil(file_size / float(chunk_size)))
        self.file_size = file_size
        self.alpha = alpha
        self.stop = stop
        self.final = self.calc_stop()

        #things related to random mnumber generator
        self.lfsr = lfsr(lfsr32s(), lfsr32p()) #starting an lfsr with a certain state and a polynomial for 32bits.
        self.lfsr_l = len(    '{0:b}'.format( lfsr32p() )   ) - 1 #calculate the length of lsfr in bits 
        self.seed = self.lfsr.__next__()


        self.PRNG = PRNG(K = self.num_chunks, delta = delta, c = c_dist, np = np) #creating the solition distribution object
        self.PRNG.set_seed(self.seed)

        #things related to error correcting code:
        self.rs = rs #the number of symbols (bytes) to add
        self.rs_obj = RSCodec(self.rs)#initalizing an reed solomon object

        #things related to biological screens:
        self.gc = gc
        self.max_homopolymer = max_homopolymer
        self.tries = 0 #number of times we tried to create a droplet
        self.good = 0 #droplets that were screened successfully.
        self.oligo_l = self.calc_oligo_length()
        self.dna_df = None
        self.dna_dl = []
    
    def df(self):
        self.dna_df = pd.DataFrame(data = self.dna_dl,columns = ['dna','gc','degree','chunk_nums'])
        return self.dna_df
    
    def calc_oligo_length(self):
        #return the number of nucleotides in an oligo:
        bits = self.chunk_size * 8 + self.lfsr_l + self.rs * 8
        return bits/4


    def calc_stop(self):

        if self.stop is not None:
            return self.stop
        
        stop = int(self.num_chunks*(1+self.alpha))+1
        return stop

    def droplet(self):
        #creating a droplet.
        data = None

        d, num_chunks = self.rand_chunk_nums() #creating a random list of segments.
        #print(num_chunks)
        for num in num_chunks: #iterating over each segment
            #logging.debug(data)
            if data is None: #first round. data payload is empty.
                data = self.chunk(num) #just copy the segment to the payload.
                #print("data in: ",data)
            else: #more rounds. Starting xoring the new segments with the payload.
                data = xor(data,self.chunk(num))  #map(operator.xor, data, self.chunk(num))
                #print("after xor: ",data)
        #print(data)
        self.tries +=  1 #upadte counter.

        #we have a droplet:
        return Droplet(data = data, 
                       seed = self.seed, 
                       rs = self.rs,
                       rs_obj = self.rs_obj,
                       num_chunks = num_chunks,
                       degree = d)

    def chunk(self, num):
        #return the num-th segment from the file
        return self.file_in[num]

    def updateSeed(self):
        #This function creates a fresh seed for the droplet and primes the solition inverse cdf sampler
        self.seed = self.lfsr.__next__() #deploy one round of lfsr, and read the register.
        self.PRNG.set_seed(self.seed) #update the seed with the register

    def rand_chunk_nums(self):
        #This funcation returns a subset of segments based on the solition distribution.
        #It updates the lfsr to generates a new seed.

        self.updateSeed() #get a fresh seed and prime the solition inverse cdf sampler.
        blockseed, d, ix_samples = self.PRNG.get_src_blocks_wrap()
        return d, ix_samples #return a list of segments.

    def screen(self, droplet):

        if screen_repeat(droplet, self.max_homopolymer, self.gc):
        #if self.screen_obj.screen(droplet.toDNA(), self.oligo_l):
            self.good += 1
            GC = gc(droplet.toDNA())
            dna = droplet.to_human_readable_DNA()
            degree = droplet.chunkNum()
            chunk_str = droplet.chunkStr()
            self.dna_dl.append([dna,GC,degree,chunk_str])
            return 1
        return 0
    
    def seed_test(self,seed):
        self.PRNG.set_seed(seed)
        blockseed, d, ix_samples = self.PRNG.get_src_blocks_wrap()
        print(ix_samples)
        
#----------------------------------------------------Glass-------------------------------------------------#        

from collections import defaultdict
class Glass:
    def __init__(self, num_chunks, out, header_size = 4, 
                 rs = 0, c_dist = 0.1, delta = 0.5, 
                flag_correct = True, gc = 0.05, max_homopolymer = 3, 
                max_hamming = 100, decode = True, chunk_size = 32, exDNA = False, np = False, truth = None):
        
        self.entries = []
        self.droplets = set()
        self.num_chunks = num_chunks
        self.chunks = [None] * num_chunks
        self.header_size = header_size
        self.decode = decode
        self.chunk_size = chunk_size
        self.exDNA = exDNA
        self.np = np
        self.chunk_to_droplets = defaultdict(set)
        self.done_segments = set()
        self.truth = truth
        self.out = out

        self.PRNG = PRNG(K = self.num_chunks, delta = delta, c = c_dist, np = np)

        self.max_homopolymer = max_homopolymer
        self.gc = gc
        prepare(self.max_homopolymer)
        self.max_hamming = max_hamming

        self.rs = rs
        self.RSCodec = None
        self.correct = flag_correct
        self.seen_seeds = set()
        
        if self.rs > 0:
            self.RSCodec = RSCodec(rs)
       

    def add_dna(self, dna_string):
        #header_size is in bytes
 
        #data = dna_to_byte(dna_string)

        data = dna_to_int_array(dna_string)
         
        if self.rs > 0:
            #there is an error correcting code
            if self.correct: #we want to evaluate the error correcting code
                try:
                    data_corrected = list(self.RSCodec.decode(data))
                    
                except:
                    logging.debug('can not correct ori data')
                    return -1, None #could not correct the code

                #we will encode the data again to evaluate the correctness of the decoding
                data_again = list(self.RSCodec.encode(data_corrected)) #list is to convert byte array to int

                if np.count_nonzero(data != list(data_again)) > self.max_hamming: #measuring hamming distance between raw input and expected raw input
                    #too many errors to correct in decoding
                    logging.debug('too many errors!')
                    logging.info('rs died')
                    return -1, None

            else: #we don't want to evaluate the error correcting code (e.g. speed)
                data_corrected  = data[0:len(data) - self.rs] #just parse out the error correcting part

        else:
            data_corrected = data
            
        logging.info('1 in')    
        seed_array = data_corrected[:self.header_size]
        seed = sum([   int(x)*256**i        for i, x in enumerate(seed_array[::-1])   ])
        payload = data_corrected[self.header_size:]
        
        
        # if seed in self.seen_seeds:
        #     return -1, None
        self.add_seed(seed)

        if self.decode:
            

            self.PRNG.set_seed(seed)
            blockseed, d, ix_samples = self.PRNG.get_src_blocks_wrap()
      
            d = Droplet(payload, seed, ix_samples)
            
            #more error detection (filter DNA that does not make sense)
            #if not screen_repeat(d, self.max_homopolymer, self.gc):
            #    print("fake dna")
            #   print(d.to_human_readable_DNA())
            #   return -1, None
            #note that when adding rs code when encoding, running this may lead to some error because we don't add rs code here

            self.addDroplet(d)
            
        return seed, data

    def addDroplet(self, droplet):


        self.droplets.add(droplet)
        for chunk_num in droplet.num_chunks:
            self.chunk_to_droplets[chunk_num].add(droplet) #we document for each chunk all connected droplets        
        #logging.debug(''.join(map(chr,droplet.data)))
        self.updateEntry(droplet) #one round of message passing

        
    def updateEntry(self, droplet):

        #removing solved segments from droplets
        for chunk_num in (droplet.num_chunks & self.done_segments):
            #if self.chunks[chunk_num] is not None:
                #we solved already this input segment. 
            if droplet.seed == 830344004:
                logging.debug("\n index %d removing",chunk_num)
                logging.debug("data before removal is:")
                logging.debug(''.join(map(chr,droplet.data)))
                logging.debug(droplet.__dict__)
                logging.debug(droplet.data)
            droplet.data = xor(droplet.data,self.chunks[chunk_num])
            #subtract (ie. xor) the value of the solved segment from the droplet.
            droplet.num_chunks.remove(chunk_num)
            #cut the edge between droplet and input segment.
            self.chunk_to_droplets[chunk_num].discard(droplet)
            #cut the edge between the input segment to the droplet               
            if droplet.seed == 830344004:
                logging.debug("data after removal is:")
                logging.debug(''.join(map(chr,droplet.data)))
                logging.debug(droplet.num_chunks)
                logging.debug(droplet.__dict__)
                logging.debug(droplet.data)
        #logging.info("data: ")
        #logging.info(droplet.data)
        #solving segments when the droplet have exactly 1 segment
        if len(droplet.num_chunks) == 1: #the droplet has only one input segment
            lone_chunk = droplet.num_chunks.pop()
            
            #logging.info("\nlone chunk appear: index %d",lone_chunk)
            #logging.info(''.join(map(chr,droplet.data)))
                          
            self.chunks[lone_chunk] = droplet.data #assign the droplet value to the input segment (=entry[0][0])
            #print(self.chunks)
            self.done_segments.add(lone_chunk) #add the lone_chunk to a data structure of done segments.
            if self.truth:
                self.check_truth(droplet, lone_chunk)
            self.droplets.discard(droplet) #cut the edge between the droplet and input segment
            self.chunk_to_droplets[lone_chunk].discard(droplet) #cut the edge between the input segment and the droplet
            
            #update other droplets
            for other_droplet in self.chunk_to_droplets[lone_chunk].copy():
                self.updateEntry(other_droplet)


    def String(self):
        #return ''.join(x or ' _ ' for x in self.chunks)
        res = ''
        for x in self.chunks:
            res += ''.join(map(chr, x))
        return res
    
    def StringNoPadding(self):
        return self.String().rstrip('\0')
    
    def removePadding(self):
        crp = []
        for b in self.chunks[-1]:
            if 0 == b:
                break 
            crp.append(b)
        self.chunks[-1] = crp
        return crp
    
    def Save(self,file_name):
        self.removePadding()
        with open(file_name,'wb') as f:
            for c in self.chunks:
                f.write(bytes(c))
            logging.info('saved')
            f.close()
    
    def reDNA(self):
        self.removePadding()
        dna = byte_to_dna(self.binString())
        return dna
        
    def binString(self):
        bs = b''
        for c in self.chunks:
            bs += bytes(c)
        return bs
    
    def print_chunks(self):
        print(self.chunks)
        
    def display_chunks(self):
        i = 0
        not_none = []
        for x in self.chunks:
            print(i,''.join(map(chr, x)))
            i+=1
            if x!= None:
                not_none.append(i)
        return not_none
    
    def check_truth(self, droplet, chunk_num):
        try:
            truth_data = self.truth[chunk_num]
        except:
            print("Error. chunk:", chunk_num, " does not exist.")
            quit(1)

        
        if not droplet.data == truth_data:
            #error
            print("Decoding error in ", chunk_num, ".\nInput is:", truth_data,"\nOutput is:", droplet.data,"\nDNA:", droplet.to_human_readable_DNA(flag_exDNA = False))
            quit(1)
        else:
            #print chunk_num, " is OK. ", self.chunksDone, " are done"
            return 1

    def add_seed(self, seed):
        self.seen_seeds.add(seed)

    def len_seen_seed(self):
        return len(self.seen_seeds)

    def isDone(self):
        if self.num_chunks - len(self.done_segments) > 0:
            return None 
        return True

    def chunksDone(self):
        return len(self.done_segments)

    def seed_test(self,seed):
        self.PRNG.set_seed(seed)
        blockseed, d, ix_samples = self.PRNG.get_src_blocks_wrap()
        print(ix_samples)

def pre_process(file_name, chunk_size):
    try:
      f = open(file_name, 'rb')
    except: 
      logging.error("%s file not found", file_name)
      sys.exit(0)
    data = f.read()    
    original_size = os.path.getsize(file_name)

    pad = -len(data) % chunk_size
    if pad > 0:
      logging.debug("Padded the file with %d zero to have a round number of blocks of data", pad)    
    data += b'\0' * pad #zero padding.
    size = len(data)
    #divide into chunks

    chunk_num = int(size/chunk_size)
    data_array = [None]*chunk_num
    for num in range(chunk_num):
        start = chunk_size * num
        end = chunk_size * (num+1)
        chunk_binary = data[start:end]
        data_array[num] = chunk_binary
    f_in = data_array
    f_size = len(data)

    return(f_in, f_size, chunk_num)

def spray(f,out_file_name, out_csv_name):
    out = open(out_file_name, 'w')
    time = 0
    succ = 0
    while f.good < f.final:
        d = f.droplet()
        time += 1
        #print(d.to_human_readable_DNA())
        if f.screen(d):
            out.write("{}\n".format(d.to_human_readable_DNA()))
            succ += 1
        #if time%1000 == 0:
            #print("%d tries, %d succ",time,succ)
    out.close()
    logging.info("Finish generating %d chunks after %d tries", succ,time)
    #print(succ/time)
    df = f.df()
    df.to_csv(out_csv_name)
    df.head()
    return time, succ
    
def decode(skip, g, out_file_name):    
    #@title decode
    logging.getLogger().setLevel(logging.INFO)
    f = open(out_file_name,'r')
    
    x = []
    y = []
    
    line = 0
    errors = 0
    seen_seeds = defaultdict(int)
    
    for i in range(skip * 500):
        try:     
            dna = f.readline().rstrip('\n')
        except:
            logging.info("Finished reading input file!")
            break
            
    while True:
        #read one dna in dna 
        try:     
            dna = f.readline().rstrip('\n')
        except:
            logging.info("After reading %d lines, %d chunks are done. So far: %d rejections (%f) %d barcodes", line, g.chunksDone(), errors, errors/(line+0.0), g.len_seen_seed())
            logging.info("Finished reading input file!")
            return -1
        if len(dna) == 0:
            logging.info("Finished reading input file!")
            return -1
        
        line += 1
        seed, data = g.add_dna(dna)
        
        if seed == -1: #reed-solomon error!
            errors += 1
            print('error!',line)
        else:
            seen_seeds[seed] += 1       

        if line % 100 == 0:
            logging.info("After reading %d lines, %d chunks are done. So far: %d rejections (%f) %d barcodes", line, g.chunksDone(), errors, errors/(line+0.0), g.len_seen_seed())
            pass
        x.append(line)
        y.append(g.chunksDone())

        if g.isDone():
            logging.info("After reading %d lines, %d chunks are done. So far: %d rejections (%f) %d barcodes", line, g.chunksDone(), errors, errors/(line+0.0), g.len_seen_seed())
            logging.info("Done!")
            f.close()
            return line
