#This files gives the final bader charge analysis from ACF.dat file and input file (input:QS or POSCAR VASP ,output: bader_df )
import matplotlib.pyplot as plt
#import numpy as np
import pandas as pd
import os
import shutil
import re
import seaborn as sns
from itertools import combinations
import numpy as np
from pymatgen.core.structure import Structure
valence_electrons = {'Ag':19.0,
                     'Au':11.0,
                     'Co':17.0,
                     'Fe':16.0,
                     'Ru':16.0,
                     'Pd':16.0,
                     'Pt':16.0,
                     'Cu':19.0,
                     'Ni':18.0,
                      'N':5.0}

def bader_df(acf_dat = './ACF.dat', 
             input_type = 'qs',
             input_path = './input.in',
             valence_dict = valence_electrons,
             slab = True,
             atom_types_line_num = 5, 
             type_num_line_num = 6,
             z_threshhold = 1.0):

    acf_file = open(acf_dat, 'r')
    acf_lines = acf_file.readlines()[2:-4]
    
    acf_file.close()
    col_names=['#','x','y','z','Charge','Min_dist','atomic_volume']
    acf_df = pd.DataFrame()
    for i in range(len(col_names)):
        acf_df[col_names[i]] = [float(re.findall(r'\d+\.*\d*', line.split()[i])[0]) for line in acf_lines]
    acf_df.drop('#',axis=1,inplace=True)
    
    input_file = open(input_path, 'r')
    input_file_lines = input_file.readlines() 
    input_file.close()
    if input_type == 'qs':
        for line_num in range(len(input_file_lines)):
            line = input_file_lines[line_num]
            if 'nat' in line:
                nat = int(re.findall(r'\d+', line)[0])
            if 'ATOMIC_POSITIONS' in line:
                start_coord = line_num + 1
                #end_coord = start_coord + nat
                break
        end_coord = start_coord + nat
        coordinate_lines = input_file_lines[start_coord: end_coord] 
        atoms_list = []
        for line in coordinate_lines:
            atom_type = line.split()[0]
            atoms_list.append(atom_type)
        
    elif input_type == 'vasp':
        atom_types = input_file_lines[atom_types_line_num].split()
        type_num = [int(i) for i in input_file_lines[type_num_line_num].split()]
        atoms_list = ''
        for i in range(0,len(atom_types)):
            atoms_list = atoms_list + type_num[i] * (atom_types[i] + ' ')
        atoms_list = atoms_list.split()
    
    acf_df['atom_type'] = atoms_list
    acf_df = acf_df[['atom_type','x', 'y', 'z', 'Charge', 'Min_dist', 'atomic_volume']]
    
    if slab == True:
        acf_df['surface_atom'] = np.where(acf_df['z'] > max(acf_df['z'])- z_threshhold,1,0)
        
    valence_list = [valence_dict.get(i) for i in atoms_list] 
    acf_df['bader_charge'] = valence_list - acf_df['Charge']
    acf_df.index = acf_df.index + 1
    return acf_df
    
#bader_df(acf_dat = '0_test_bader/ACF_original.dat', 
         #input_type = 'vasp',
         #input_path = '0_test_bader/CONTCAR')        
    
        
        
        
        
            
        
    
