import cv2 as cv2
import matplotlib.pyplot as plt
import numpy as np

C = {
    'A': (0,0.4,1),
    'T': (0.8,0.2,0.2),
    'G': (1,0,0.8),
    'C': (0,1,0.4),
    'D': (1,1,1),
    'I': (0.8,0.8,0.4),
    'B': (0,0,0)
}

class dna_painter:
    def __init__(self,W = 10,H = 10):
        self.W = W
        self.H = H
        self.Line_width = int(H/3) + 1
        self.Line_spacing = int(H/2) + 1
        
    def rec(self,img,x,n,c,ins = 0):
        if ins == 1:
            cv.rectangle(img,(x*self.W,n*self.H),(x*self.W+self.W-1,n*self.H+self.H-1),C['I'],-1)
        else:
            cv.rectangle(img,(x*self.W,n*self.H),(x*self.W+self.W-1,n*self.H+self.H-1),c,-1)
    
    def line(self,img,x,n,l):
        cv.line(img,(x*self.W, n*self.H + self.Line_spacing),(x*self.W + l*self.W-1,n*self.H + self.Line_spacing),(1,1,1),self.Line_width)
    
    def draw_dna(self,img,dna,row = 0):
        for i,base in enumerate(dna):
            self.rec(img,i,row,C[base])
            
    def draw_text(self,img,text,x,n,c = (1,1,1)):
        
        cv.putText(img, text, (x * self.W,n * self.H+3), cv.FONT_HERSHEY_COMPLEX, 0.6, c, 1)

    def draw_dnas(self,dna_array,src = 'dna.png'):
        img = np.zeros([self.H*(len(dna_array) * 2 + 2),len(dna_array[0])*self.W,3])
        for i in range(len(dna_array)):
            self.draw_dna(img,dna_array[i],i*2)
        plt.imsave(src,img)
        
        return plt.imshow(img)
    
    def draw_dnas_with_marks(self,dna_array,src = 'dna_repeat.png', scanner = None):
        color = lambda b: (0,1,0) if b == True else (1,0,0)  
        self.scanner = scanner
        if scanner == None:
            self.scanner = Scanner()
        gcs = [[self.scanner.Gc(dna), self.scanner.gc_pass(dna)] for dna in dna_array]
        homos = [self.scanner.scan_repeats(dna,True) for dna in dna_array] 
        # get gc and rp
        
        img = np.zeros([self.H*(len(dna_array) * 2),(len(dna_array[0])+11)*(self.W),3])
        #init image
        
        for i in range(len(dna_array)):
            self.draw_dna(img,dna_array[i],i*2)
            for homo in homos[i]:
                l = homo[1]
                start = homo[2]
                self.line(img,start,i*2 + 1,l)
            self.draw_text(img,str(gcs[i][0])[:4],len(dna_array[0]) + 1, i*2+1, color(gcs[i][1]))
            if (homos[i] != []):
                self.draw_text(img,'rej',len(dna_array[0]) + 6, i*2+1, color(False))
            else:
                self.draw_text(img,'pas',len(dna_array[0]) + 6, i*2+1, color(True))
        plt.imsave(src,img)
        
        return plt.imshow(img)

    def draw_error(self,img,errors,row,num):
        for error in errors:
            x = error[0]
            typ = error[1]
            to = error[2]
            if(typ == '-'):
                to = 'D'
            if(typ != '+'):
                self.rec(img,x,row,C[to])
            else:
                self.rec(img,x,row,C[to],1)