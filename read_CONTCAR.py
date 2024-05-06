#This function is desined to read poscar or CONTCAR files from vasp, input:poscar or contcar, output: final coordinates in a form of dataframe or a list 
import numpy as np
def read_CONTCAR(contcar_path, 
                 output_type = 'list',  # 'list' or df
                 coord_start_line_num = 9,
                 cell_dm_ang_line_num = 1,
                 cell_pars_line_num = 2, 
                 atom_types_line_num = 5, 
                 type_num_line_num = 6):

    def vasp_to_coordinate(coord_line, cell_matrix, atom_type):
      coord_list = coord_line.split()[0:3]
      #atom_type = coord_line.split()[0]
      for n in range(len(coord_list)):
          #coord_list[n] = re.sub("d","0",coord_list[n])
          coord_list[n] = float(coord_list[n])
      coord_array = np.array(coord_list).reshape(1,3)
      coord_array_ang = np.dot(coord_array,cell_matrix)
      return (atom_type,coord_array_ang)  
    
    all_coords = []
    #Extracting information from final CONTCAR
    contcar = open(contcar_path,'r')
    contcar_lines = contcar.readlines()

    ##cell matrix
    cell_dm_ang = float(contcar_lines[cell_dm_ang_line_num].split()[0])
    list_cell_matrix = [float(i) for i in contcar_lines[cell_pars_line_num].split() 
                        + contcar_lines[cell_pars_line_num + 1].split() 
                        + contcar_lines[cell_pars_line_num + 2].split()]
    cell_matrix = np.array(list_cell_matrix).reshape(3,3) * cell_dm_ang 

    ##generations of atom types list
    atom_types = contcar_lines[atom_types_line_num].split()
    type_num = [int(i) for i in contcar_lines[type_num_line_num].split()]
    atoms_list = ''
    for i in range(0,len(atom_types)):
        atoms_list = atoms_list + type_num[i] * (atom_types[i] + ' ')
    atoms_list = atoms_list.split()

    ##Reading cooordinates oof CONTCAR
    #The line number in the contcar where the first coordinates is written (start counting from zero not one)
    coordinates = contcar_lines[coord_start_line_num : coord_start_line_num + sum(type_num)]
    for num in range(len(coordinates)):    
        coordinate = vasp_to_coordinate(coordinates[num],cell_matrix, atoms_list[num])
        all_coords.append(coordinate)
        
    df = pd.DataFrame()
    atom_type = [i[0] for i in all_coords]
    x = [i[1][0][0] for i in all_coords]
    y = [i[1][0][1] for i in all_coords]
    z = [i[1][0][2] for i in all_coords]
    df['atom_type'] = atom_type
    df['x'] = x
    df['y'] = y
    df['z'] = z
    
    if output_type == 'list':
        return all_coords
    else:
        return df
