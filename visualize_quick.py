#Define a function that shows the structure of a material from different angles
def visualize_qsinput(input_file, figsize = (6,5),view = 'top',savefile = None,title=None):
    import re
    import matplotlib.pyplot as plt
    import seaborn as sns
    from mpl_toolkits import mplot3d
    import numpy as np
    def qsline_to_arcoord(coord_line, cell_matrix):
        coord_list = coord_line.split()[1:4]
        atom_type = coord_line.split()[0]
        for n in range(len(coord_list)):
            coord_list[n] = re.sub("d","0",coord_list[n])
            coord_list[n] = float(coord_list[n])
        coord_array = np.array(coord_list).reshape(1,3)
        coord_array_ang = np.dot(coord_array,cell_matrix)
        return (atom_type,coord_array_ang)
    
    
    input_ = open(input_file,"r").readlines()
    #cell_parameters
    for line_n in range(len(input_)):
        if "celldm" in input_[line_n]:
            celldm_bohr = float(re.findall(r"\d+\.\d+",input_[line_n])[0])
            celldm_ang = celldm_bohr * 0.529177
        if "nat" in input_[line_n]:
            natom = int(re.findall(r"\d+",input_[line_n])[0])
            
        if "CELL_PARAMETERS" in input_[line_n]:
            cell_start = line_n + 1
            cell_end = line_n + 3
            
        if "ATOMIC_POSITIONS" in input_[line_n]:
            coord_start = line_n + 1
        
    cell_lines = input_[cell_start: cell_end + 1]
    coord_lines = input_[coord_start : coord_start + natom]
    
    cell_list = []
    for line in cell_lines:
        line = re.sub("d","0",line)
        line_list = line.split()
        for element in line_list:
            cell_list.append(float(element))
    cell_matrix = np.array(cell_list).reshape(3,3)
    cell_matrix = cell_matrix * celldm_ang
    
    atom_types = []
    x = []
    y = []
    z = []
    
    for line in coord_lines:
        atom_type = qsline_to_arcoord(line, cell_matrix = cell_matrix)[0]
        arcoord = qsline_to_arcoord(line, cell_matrix = cell_matrix)[1]
        atom_types.append(atom_type)
        x.append(arcoord[0][0])
        y.append(arcoord[0][1])
        z.append(arcoord[0][2])
        
    title = input_file.split('/')[-1] if title == None else title
    plt.figure(figsize=figsize)
    plt.title(title)
    if savefile != None:
        if view == 'top':
            figure_ = sns.scatterplot(x,y,hue=atom_types)
            plt.savefig(savefile,dpi=300)
            return figure_
            
        elif view == 'side':
            figure_ = sns.scatterplot(x,z,hue=atom_types)
            plt.savefig(savefile,dpi=300)
            return figure_
    
    else:
        if view == 'top':
            figure_ = sns.scatterplot(x,y,hue=atom_types)
            #plt.savefig()
            return figure_
            
        elif view == 'side':
            figure_ = sns.scatterplot(x,z,hue=atom_types)
            #plt.savefig()
            return figure_
            
        
        
        
    #elif view = '3d':
        #return sns.scatterplot(y,z,hue=atom_types)#side  = xz
    #3d = xyz
    
    #fig = plt.figure(figsize=figsize)
    #ax = plt.axes(projection="3d")
    #return sns.scatterplot(y,z,hue=atom_types)
    #return ax.scatter3D(x,y,z)
    
    
    
        
    
    
    

    
    
