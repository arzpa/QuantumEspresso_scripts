import os
import re


#Inputs
cluster_name = str(input('Please enter name of the cluster you are using: '))
material_name = str(input('Please enter name of the Material directory: '))
molecule = str(input('Molecule (example entries: N2):  '))
mols = ['N2','H2','N2H'] #The same list of mols which you used to generate the adsites


main_dir = '/home/pagh/scratch/ML_project/Subhmoy/'
surf_ad_folder = main_dir + str(f'{material_name}/') + str(mols.index(molecule)+2) + '_' + molecule + "/"

directory_list = os.listdir(surf_ad_folder)
directory_list = sorted(directory_list,key=lambda x: int(re.findall(r'\d+', x)[0]))
print(directory_list)
print('The number of adsite for this sctructure is',len(directory_list))
to_do_adsites = str(input('Please enter the range of adsites-to-run --format: "all", "11:13")'))

if to_do_adsites != 'all':
    range_ = to_do_adsites.split(':')
    min_ = int(range_[0])
    max_ = int(range_[1]) + 1
    for i in range(min_,max_):
        ad_site_folder = f'{i}_ad_site'
        print(ad_site_folder)
        os.chdir(surf_ad_folder + ad_site_folder)
        os.system(f'sbatch submitVASP_{cluster_name}.sh')
else:
    for ad_site_folder in directory_list:
        print(ad_site_folder)
        os.chdir(surf_ad_folder + ad_site_folder)
        os.system(f'sbatch submitVASP_{cluster_name}.sh')
