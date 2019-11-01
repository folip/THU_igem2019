from Helper_Functions import *
from math import sqrt
import json

process = 0


class Mask:
    # random mask generator
    def __init__(self, seed=11211, scanner=None, mask_length=96, withdraw=0,
                 mask_space_size=2, fp=None, rp=None):
        self.mask_length = mask_length
        self.mask_space_size = mask_space_size
        self.seed = seed
        self.withdraw = withdraw
        self.scanner = scanner
        if self.scanner == None:
            self.scanner = Scanner()
        self.masks = self.gen_random_masks(4 ** self.mask_space_size)
        self.fp = fp
        self.rp = rp
        self.hit_indexes = []
        self.encode_result = []
        self.fail = []

    def gen_random_mask(self):
        return random_dna(self.mask_length)

    def gen_random_masks(self, mask_num=16):
        self.refresh()
        self.masks = [self.gen_random_mask() for i in range(mask_num)]
        return self.masks

    def refresh(self):
        random.seed(self.seed)
        for i in range(self.withdraw):
            random.randint(0, 255)

    def assemble(self, dna, mask_index):
        dna = num_to_dna(mask_index, self.mask_space_size) + dna
        if self.rp != None and self.fp != None:
            return self.fp + dna + self.rp
        else:
            return dna

    def encode_dna(self, dna):
        temp = []
        for (i, m_dna) in enumerate(self.masks):
            masked_dna = self.assemble(xor_dna(dna, m_dna), i)
            temp.append(masked_dna)
            if (self.scanner.Pass(masked_dna)):
                return i, masked_dna, 0
        # all fail
        masked_dna, max_homo = self.scanner.select_best(temp)
        #         self.hit_indexes.append(-1)
        #         self.encode_result.append(masked_dna)
        return -1, masked_dna, max_homo

    def encode(self, dnas):
        process = 0
        self.encode_result = []
        self.hit_indexes = []
        self.fail = []
        for j, dna in enumerate(dnas):
            hit_index, masked_dna, max_homo = self.encode_dna(dna)
            self.hit_indexes.append(hit_index)
            self.encode_result.append(masked_dna)
            if (j % 10 == 0):
                process = int(100 * j / len(dnas))
                print(process)
            if (hit_index == -1):
                self.fail.append([j, masked_dna, max_homo])
        return self.encode_result, self.hit_indexes

    def decode(self, dnas):
        self.re_dnas = []
        for re_dna in dnas:
            mask_index = dna_to_int_array(re_dna[:self.mask_space_size])[0]
            re_dna = xor_dna(re_dna[self.mask_space_size:], self.masks[mask_index])
            self.re_dnas.append(re_dna)
        return self.re_dnas

    def save(self, file_name, index_l, rs=0, ori_file_name=None):
        with open(file_name, 'w') as f:
            dic = {
                'Encoding': 'DNA Mask',
                'Chunk Nums': len(self.encode_result),
                'Index Length': index_l,
                'rs': rs,
                'Mask length': self.mask_length,
                'seed': self.seed,
                'withdraw': self.withdraw,
                'mask_space_size': self.mask_space_size
            }
            if (ori_file_name != None):
                dic['file name'] = ori_file_name
            info = json.dumps(dic)
            f.write(info + '\n')

            for dna in self.encode_result:
                f.write(dna + '\n')
            f.close()

    def decode_from_file(self, file_name):
        f = open(file_name, 'r')

        json_para = f.readline()
        dic = json.loads(json_para)

        chunk_num = dic['Chunk Nums']
        index_l = dic['Index Length']
        rs = dic['rs']

        self.mask_length = dic['Mask length']
        self.seed = dic['seed']
        self.withdraw = dic['withdraw']
        self.mask_space_size = dic['mask_space_size']
        self.masks = self.gen_random_masks(4 ** self.mask_space_size)

        self.re_dnas = []
        i = 0
        process = 0
        while True:
            re_dna = f.readline().split('\n')[0]
            i += 1
            if re_dna == '':
                break
            if (i % 10 == 0):
                process = int(100 * i / chunk_num)
                print(process)
            mask_index = dna_to_int_array(re_dna[:self.mask_space_size])[0]
            re_dna = xor_dna(re_dna[self.mask_space_size:], self.masks[mask_index])
            self.re_dnas.append(re_dna)
        return self.re_dnas, chunk_num, index_l, rs
