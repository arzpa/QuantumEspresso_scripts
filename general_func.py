#Some general functions
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

def qsline_to_coordinate(coord_line, cell_matrix):
    coord_list = coord_line.split()[1:4]
    atom_type = coord_line.split()[0]
    for n in range(len(coord_list)):
        coord_list[n] = re.sub("d","0",coord_list[n])
        coord_list[n] = float(coord_list[n])
    coord_array = np.array(coord_list).reshape(1,3)
    coord_array_ang = np.dot(coord_array,cell_matrix)
    return (atom_type,coord_array_ang)

def vasp_to_coordinate(coord_line, cell_matrix, atom_type):
    coord_list = coord_line.split()[0:3]
    #atom_type = coord_line.split()[0]
    for n in range(len(coord_list)):
        #coord_list[n] = re.sub("d","0",coord_list[n])
        coord_list[n] = float(coord_list[n])
    coord_array = np.array(coord_list).reshape(1,3)
    coord_array_ang = np.dot(coord_array,cell_matrix)
    return (atom_type,coord_array_ang)  

def TOTEN_vasp(outcar_path, decimal = 4):
    outcar = open(outcar_path, 'r')
    outcar_lines = outcar.readlines()
    for n_line in range(len(outcar_lines)):
        if 'TOTEN' in outcar_lines[n_line]:
            TOTEN = round(float(outcar_lines[n_line].split()[4]),decimal)
    return TOTEN

def two_atoms_dist(atom1_coord, atom2_coord, decimal = decimal):
    return round(np.linalg.norm(atom1_coord - atom2_coord),decimal)
