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

def expand_charge_file_VASP(acf_dat,
                            input_path,
                            input_type = 'vasp',
                            supercell_size = [2,2,1]):
    
    if len(supercell_size)!= 3:
        return 'supercell size should have this format: [int, int, int]'
    repetition = np.prod(supercell_size)
    supercell_size_str = ''.join([str(i) for i in supercell_size])
    new_poscar_path = input_path +  '.' + f'{supercell_size_str}'
    new_acf_path = acf_dat + '.' + f'{supercell_size_str}'
    new_acf = open(new_acf_path,'w')



    input_ = open(input_path,'r')
    input_lines = input_.readlines()
    input_.close()

    structure = Structure.from_file(input_path)
    structure.make_supercell(supercell_size)
    structure.to(fmt = 'POSCAR',filename = new_poscar_path)

    new_poscar_coordinates = read_CONTCAR(new_poscar_path)

    acf_dat = open(acf_dat,'r')
    acf_dat_lines = acf_dat.readlines()
    acf_dat.close()

    non_rep_list = ['---','X','VACUUM','NUMBER']
    for line in acf_dat_lines:
        if find_element(non_rep_list, line):
            new_acf.write(line)
        else:
            for i in range(0, repetition):
                new_acf.write(line)

    new_acf.close()

    new_bader_df = bader_df(acf_dat=new_acf_path,
                            input_type = 'vasp',
                            input_path = new_poscar_path,
                            valence_dict = valence_electrons,
                            slab = True,
                            atom_types_line_num = 5, 
                            type_num_line_num = 6,
                            z_threshhold = 1.0)

    new_poscar_df = read_CONTCAR(new_poscar_path,output_type='df')

    new_bader_df['x'] = new_poscar_df['x']
    new_bader_df['y'] = new_poscar_df['y']
    new_bader_df['z'] = new_poscar_df['z']

    return new_bader_df
    
        
        
    
     
    
    
    

    
    
