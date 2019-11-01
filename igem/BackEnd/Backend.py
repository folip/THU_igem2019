# from Helper_Functions import *
from FT_class import *
import logging

logging.getLogger().setLevel(logging.INFO)
from Visual import *
from dna_painter import *
from DNAMask import *
import os
from c_progress import ProgressDialog


class Backend:
    def __init__(self):
        self.dic = {
            'encoding method': 'DNA Fountain',
            'chunk_size': 32,
            'rs_length': 0,
            'alpha': 0.5,
            'gc': [0.45, 0.55],
            'max_homo_length': 3,
            'forward_primer': 'ATCGAGCTGACTAC',
            'reverse_primer': 'TCAGTCGATCGTGT',
            'file_name': None,
            'FT_key': [2 ** 32, 1103, 12345],
            'Mask_key': [17312, 123],
            'Mask_length': 3
        }
        self.scanner = Scanner(self.dic['max_homo_length'], self.dic['gc'])
        self.data = None
        self.dnas = None
        self.painter = DNA_painter()

    def change_file_name(self, file_name):
        self.dic['file_name'] = file_name
        return self.analyze_file(file_name)

    def change_config(self, dic):
        self.update_dic(dic)
        self.scanner = Scanner(self.dic['max_homo_length'], self.dic['gc'])
        if (self.dic['file_name'] == None):
            return False
            # just change configration, not analyzing files
        return self.analyze_file(self.dic['file_name'])

    def update_dic(self, dic):
        for key in dic.keys():
            self.dic[key] = dic[key]
        return self.dic

    def analyze_file(self, file_name):
        self.file_size = os.path.getsize(file_name)
        self.data = preprocess(file_name, self.dic['chunk_size'])
        self.dnas = [byte_to_dna(d) for d in self.data]
        analyze_result = self.scanner.analyze(self.dnas)

        hist(analyze_result['gc_list'], lb='gc', des='figure/gc.jpg')
        hist(analyze_result['homo_list'], lb='homo', des='figure/homo.jpg')
        result_dic = {
            'gc_out_of_range': analyze_result['gc_out'],
            # 'average_gc':analyze_result['average_gc'],
            'chunks_with_long_homo': analyze_result['homo_too_long'],
            'chunk_num': len(self.data),
            'file_size': self.file_size
        }
        return result_dic

    def start_encoding(self):
        if (self.dic['encoding method'] == 'DNA Fountain'):
            return self.start_encoding_FT()
        else:
            return self.start_encoding_Mask()

    def start_encoding_FT(self):
        self.f = DNAFountain(self.data, alpha=self.dic['alpha'], rs=self.dic['rs_length'],
                             scanner=self.scanner)
        self.f.encode(self.data)
        self.f.save('temp/FT.dna', ori_file_name=file_name_pure(self.dic['file_name']))

        droplets_nums = self.f.final
        # try to decode
        self.FT_decode('temp/FT.dna')
        if (self.decode_success == True):
            decode_num_requires = len(self.solve_num)
            self.g.Save('temp/BackFT.' + self.dic['file_name'].split('.')[1])
        # draw dna images
        droplets = [d[0] for d in self.f.dna_dl]
        self.painter.draw_dnas_with_marks(self.dnas[:25], src='figure/ori_dna.jpg')
        self.painter.draw_dnas_with_marks(droplets[:25], src='figure/FT_encoded_dna.jpg')

        # return infomations
        dna_segments = [['forward primer', len(self.dic['forward_primer'])], ['', 0], ['seed', 16], \
                        ['data', self.dic['chunk_size'] * 4], ['rs', self.dic['rs_length'] * 4], \
                        ['reverese primer', len(self.dic['reverse_primer'])]]
        info = []
        if (self.decode_success == False):
            info.append('!!!!ERROR:')
            info.append('Can Only decode ' + str(self.solve_num[-1]) + ' chunks ')
            info.append('Please increase alpha.')
            info = '\n'.join(info)
            return {
                # 'segments': dna_segments,
                'segments': [s[1] for s in dna_segments],
                'info': info,
                'chunk_num': self.dic['chunk_num'],
                'oligo_num': droplets_nums
            }

        info.append('$$$Error Correcting ability: ')
        info.append('Up to ' + str(int(0.5 * self.dic['rs_length'])) + ' errors in one sequence')
        info.append('Up to ' + str(droplets_nums - decode_num_requires) + ' sequence lost\n')

        info.append('$$$Bio: ')
        info.append('Gc interval: ' + str(self.dic['gc'][0]) + ' to ' + str(self.dic['gc'][1]))
        info.append('Max Homo: ' + str(self.dic['max_homo_length']) + '\n')

        info.append('$$$Information Density(without primer): ')
        info.append(str(self.information_density_FT()) + 'bits/base')
        info.append(str(100 * self.reduancy_FT()) + '% reduency added\n')

        info = '\n'.join(info)
        return {
            'segments': [s[1] for s in dna_segments],
            'info': info,
            'chunk_num': len(self.data),
            'oligo_num': droplets_nums
        }

    def start_encoding_Mask(self):
        # adding rs code
        self.data = rs_encode(self.data, self.dic['rs_length'])
        # indexing
        self.dnas, self.index_length = data_to_indexed_dnas(self.data)
        # masking
        key = self.dic['Mask_key']
        self.m = Mask(seed=key[0], withdraw=key[1], scanner=self.scanner, \
                      mask_length=len(self.dnas[0]), mask_space_size=self.dic['Mask_length'])
        encode_result, hit = self.m.encode(self.dnas)
        self.succ_rate = (1 - hit.count(-1)) / len(hit)
        # draw result
        self.painter.draw_dnas_with_marks(self.dnas[:25])
        self.painter.draw_dnas_with_marks(encode_result[:25])

        # construct info
        info = self.encode_info_Mask()
        segments = self.encode_segments_Mask()
        return {
            # 'segments': segments,
            'segments': [s[1] for s in segments],
            'info': info,
            'chunk_num': len(self.data),
            'oligo_num': len(self.dnas),
        }

    def encode_segments_Mask(self):
        dna_segments = [['forward primer', len(self.dic['forward_primer'])], ['mask index', self.dic['Mask_length']], \
                        ['chunk index', self.index_length], \
                        ['data', self.dic['chunk_size'] * 4], ['rs', self.dic['rs_length'] * 4], \
                        ['reverese primer', len(self.dic['reverse_primer'])]]
        return dna_segments

    def encode_info_Mask(self):
        info = []
        info.append('$$$Error Correcting ability: ')
        info.append('Up to ' + str(int(0.5 * self.dic['rs_length'])) + ' errors in one sequence\n')

        info.append('$$$Bio: ')
        info.append('Gc interval: ' + str(self.dic['gc'][0]) + ' to ' + str(self.dic['gc'][1]))
        info.append('Max Homo: ' + str(self.dic['max_homo_length']))
        info.append(str(100 * (1 - self.succ_rate)) + '% pass' + '\n')

        info.append('$$$Information Density(without primer): ')
        info.append(str(self.information_density_Mask()) + 'bits/base')
        info.append(str(100 * self.reduancy_Mask()) + '% reduency added')

        return '\n'.join(info)

    def save_encoding_result(self, file_name=None):
        if file_name == None:
            file_name = 'pool/' + file_name_no_type(self.dic['file_name']) + '.dna'
        if self.dic['encoding method'] == 'DNA Fountain':
            self.f.save(file_name, ori_file_name=file_name_pure(self.dic['file_name']))
        else:
            self.m.save(file_name, index_l=self.index_length, ori_file_name=file_name_pure(self.dic['file_name']))

    def decode(self, file_name):
        # touch
        dic = touch(file_name)
        self.dic['encoding method'] = dic['Encoding']
        self.dic['file_name'] = dic['file name']
        self.dic['rs'] = dic['rs']
        des_file_name = 're/' + self.dic['file_name']
        # choose ways to decode
        if self.dic['encoding method'] == 'DNA Fountain':
            FT_decode(file_name)
            if (self.decode_success):
                self.FT_save_recovered_file(des_file_name)
            else:
                logging.error('decoding failed.')
        else:
            self.data, bad_pos = self.Mask_decode(file_name)
            # print(bad_pos)
            if (bad_pos == []):
                join_and_save(self.data, des_file_name)

    def reduancy_Mask(self):
        return (self.dic['chunk_size'] * 4 + self.index_length + self.dic['rs_length'] * 4 + self.dic[
            'Mask_length']) / (self.dic['chunk_size'] * 4) - 1

    def information_density_Mask(self):
        return 2 / (self.reduancy_Mask() + 1)

    def reduancy_FT(self):
        return (1 + self.dic['alpha']) * (self.dic['chunk_size'] + self.dic['rs_length'] + 4) / self.dic[
            'chunk_size'] - 1

    def information_density_FT(self):
        return 2 / (1 + self.reduancy_FT())

    # ------------decode-----------------#
    def FT_decode(self, file_name):
        self.g, self.solve_num, self.decode_success = FT_decode(file_name)

    def FT_save_recovered_file(self, des_file_name):
        self.g.Save(des_file_name)

    def Mask_decode(self, file_name):
        self.m = Mask()
        dnas, chunk_num, index_l, rs = self.m.decode_from_file(file_name)
        # return dnas
        data = dnas_to_data(dnas, chunk_num, index_l)
        self.data, bad_pos = rs_decode(data, rs)
        return data, bad_pos
