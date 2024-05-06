#This function convert a quantum espresso input to VASP POSCAR
def qs_to_vasp_poscar(qs_input,filename):
    input_ = open(qs_input,'r')
    input_lines = input_.readlines()
    input_.close()
    poscar_path = filename
    
    #Extract general infos
    cell_dm = 1
    pattern = re.compile("^\s*!") #we want to see if celldm is mentioned
    for line_num in range(len(input_lines)):
        line = input_lines[line_num]
        if bool(pattern.match(line)) == False:
            if 'CELL_PARAMETERS' in line:
                cell_pars_line_num = line_num + 1
                if 'ang' in line:
                    ang_constant = 1
                else:
                    ang_constant = 0.529177
            if 'celldm' in line:
                cell_dm = float(re.findall(r'\d+\.*\d*', line.split('=')[-1])[0])
            if 'nat' in line:
                nat = int(re.findall(r'\d+', line)[0])
            if 'ATOMIC_POSITIONS' in line:
                start_coord = line_num + 1
                end_coord = start_coord + nat
    
    #Transfer coordinates in QS to VASP
    coordinate_lines = input_lines[start_coord: end_coord]
    coord_vasp_list = []
    for line in coordinate_lines:
        atom_type = line.split()[0]
        each_coord_list = line.split()[1:]
        each_coord_vasp =  '   '.join(each_coord_list)
        coord_vasp_list.append((atom_type,each_coord_vasp))
    atoms_list = []
    atoms_dict = {}
    for line in coordinate_lines:
        atom_type = line.split()[0]
        atoms_list.append(atom_type)
    
    atom_types = list(set(atoms_list))
    for each_atom_type in atom_types:
        atoms_dict[each_atom_type] = []
    
    for each_atom in coord_vasp_list:
        atom_type = each_atom[0]
        atoms_dict[atom_type].append(re.sub('d','0',each_atom[1]))

    ##cell matrix
    cell_dm_ang = cell_dm * ang_constant
    list_cell_matrix = [float(re.sub('d', '0', i)) for i in input_lines[cell_pars_line_num].split() 
                        + input_lines[cell_pars_line_num + 1].split() 
                        + input_lines[cell_pars_line_num + 2].split()]    
    cell_matrix = np.array(list_cell_matrix).reshape(3,3) * cell_dm_ang 
    
    
    #Writing the lines in poscar file
    line_1 = 'Enter your title\n'
    line_2 = '1\n'
    line_3 = f'{round(cell_matrix[0][0],8)}    {round(cell_matrix[0][1],8)}     {round(cell_matrix[0][2],8)}\n'
    line_4 = f'{round(cell_matrix[1][0],8)}    {round(cell_matrix[1][1],8)}     {round(cell_matrix[1][2],8)}\n'
    line_5 = f'{round(cell_matrix[2][0],8)}    {round(cell_matrix[2][1],8)}     {round(cell_matrix[2][2],8)}\n'
    line_6 = '    '.join(atom_types) + '\n'
    line_7 = '    '.join([str(len(atoms_dict[atom_type])) for atom_type in atom_types]) + '\n'
    line_8 = 'Selective dynamics\n'
    line_9 = 'Direct\n'
    
    initial_lines = [line_1, line_2, line_3, line_4, line_5,
                    line_6, line_7, line_8, line_9]
    
    poscar = open(poscar_path,'w')
    for line in initial_lines:
        poscar.write(line)
    for atom_type in atom_types:
        coord_list = atoms_dict[atom_type]
        for line in coord_list:
            if len(line.split()) > 3 and len(line.split()) < 7:
                coords = '    '.join(line.split()[0:3])
                fixed = '  '
                for TorF in line.split()[3:]:
                    if TorF == '0':
                        fixed = fixed + re.sub('0',' F ',TorF)
                    elif TorF == '1':
                        fixed = fixed + re.sub('1',' T ',TorF)
                line = coords + fixed    
                poscar.write(line + '\n')
            elif len(line.split()) == 3:
                poscar.write(line + '  T  T  T' + '\n')
        
    poscar.close()

    
    
    
    
    
    
        
