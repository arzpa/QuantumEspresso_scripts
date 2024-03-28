import os
import re


#Inputs
cluster_name = 'narval' #str(input('Please enter name of the cluster you are using: '))

#Subhmoy_materials_str = ''
Subhmoy_materials = Subhmoy_materials_str.split()

Satvik_materials_str = ''
Satvik_materials = Satvik_materials_str.split()




material_num_index = int(input('Please enter material index: '))
material_name = f'{material_num_index}_{Satvik_materials[material_num_index]}'

#material_name = str(input('Please enter name of the Material directory: '))
mol_to_run = 'all' #str(input('Molecule (example entries: N2):  '))
#mols = ['N2','H2','N2H'] #The same list of mols which you used to generate the adsites
mols = ['N2','H2']
if mol_to_run == 'all':
    for molecule in mols:
        main_dir = '/home/pagh/scratch/ML_project/Satvik/'
        surf_ad_folder = main_dir + str(f'{material_name}/') + str(mols.index(molecule)+2) + '_' + molecule + "/"
        directory_list = os.listdir(surf_ad_folder)
        directory_list = sorted(directory_list,key=lambda x: int(re.findall(r'\d+', x)[0]))
        print(directory_list)
        print('The number of adsite for this sctructure is',len(directory_list))    
        to_do_adsites = 'all'
        if to_do_adsites == 'all':
                for ad_site_folder in directory_list:
                    print(ad_site_folder)
                    os.chdir(surf_ad_folder + ad_site_folder)
                    os.system(f'sbatch submitVASP_{cluster_name}.sh')
