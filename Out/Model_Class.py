import pandas as pd
import math
import random
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import numpy as np
from Model_Helpers import *
from Visual import *
class pool:
    def __init__(self,dna_list,PR):
        self.dna_list = dna_list
        self.sequence_num = len(dna_list)
        self.gc = [0 for i in range(self.sequence_num)]
        self.set_gc()
        self.oligo_num_total = PR * self.sequence_num
        self.oligo_nums = [PR for i in range(self.sequence_num)]
        self.cumu_prob = [0 for i in range(self.sequence_num)]
        
        self.set_cumu_prob()
       
    
    def set_gc(self):
        for i in range(self.sequence_num):
            self.gc[i] = gc(self.dna_list[i])
    
    def set_cumu_prob(self):
        cumu_prob = 0
        for i in range(self.sequence_num):
            cumu_prob += self.oligo_nums[i] / self.oligo_num_total
            self.cumu_prob[i] = cumu_prob
          
    def sample(self,num):
        for i in range(self.sequence_num):
            self.oligo_nums[i] = 0
        random_pick(num,self.cumu_prob,self.oligo_nums)
        self.oligo_num_total = 0
        for i in self.oligo_nums:
            self.oligo_num_total += i
        print(self.oligo_num_total)
        self.set_cumu_prob()
        return data_display(self.oligo_nums)
        
    def sequencing(self,num):
        sequenced_oligo_nums = [0 for i in range(self.sequence_num)]
        random_pick(num,self.cumu_prob,sequenced_oligo_nums)
        if 0:
            for i in range(3): #supposed to be 10
                dna = self.dna_list[i]
                snum = sequenced_oligo_nums[i]
                print('original DNA:')
                print_dna(dna)
                print('sequenced_DNA:')
                for j in range(min(snum,5)):
                    print_dna(sequencing_result(dna))
        return sequenced_oligo_nums[0:11]
        #return sequenced_oligo_nums.count(0)
        #return max(sequenced_oligo_nums)
        #return data_display(sequenced_oligo_nums)
        
    def PR(self):
        return self.oligo_num_total/self.sequence_num
        
    def PCR(self,PCRC):
        for i in range(self.sequence_num):
            para = PCR_para(self.dna_list[i])
            amplify_ratio = pow(para,PCRC)
            self.oligo_nums[i] *= amplify_ratio
        self.update_total_num()
        self.set_cumu_prob()
        return data_display(self.oligo_nums)

    def recommended_PCRC(self):
        PR = self.PR()
        return math.log(ref_target_num/PR,amplification_base_rate)
   
    def update_total_num(self):
        self.oligo_num_total = 0
        for i in self.oligo_nums:
            self.oligo_num_total += i
        
    def oligo_num_review(self):
        x = [0,1,2,3,4,5,6,7,8,9,10]
        y = [0 for i in range(11)]
        for num in self.oligo_nums:
            if 0<= num and 10>= num:
                y[num] += 1
        source = pd.DataFrame({
            'oligo_num': x,
            'freq': y
        })
        return alt.Chart(source).mark_bar().encode(
            x='oligo_num',
            y='freq',
        )
    
    def display(self):
        return data_display(self.oligo_nums)
    
    
    def decay_f(self,time):
        print(self.oligo_nums[1:10]) #test
        self.oligo_num_total = 0
        self.decay(time)
        self.set_cumu_prob()
        print(self.oligo_nums[1:10]) #test
        return data_display(self.oligo_nums)
        
    def decay(self,time):
        htc = time/ref_half_time #half_time_cycle
        if enzyme_type == "proof_reading":
            for i in range(self.sequence_num):
                decay_para =  (depurination_rate + c2u_rate * self.gc[i] * 2) / 100
                decay_ratio = pow(1-decay_para, htc)
                self.oligo_nums[i] *=  decay_ratio
                self.oligo_num_total += self.oligo_nums[i]
        else:
            decay_para = depurination_rate
            decay_ratio = pow(1-decay_para, htc) / 100
            for i in range(self.sequence_num):
                self.oligo_nums[i] *=  decay_ratio
                self.oligo_num_total += self.oligo_nums[i]