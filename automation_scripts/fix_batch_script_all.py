import os
import shutil
import re
Subhmoy_materials_str = ''
Subhmoy_materials = Subhmoy_materials_str.split()

Satvik_materials_str = ''
Satvik_materials = Satvik_materials_str.split()

person ='Satvik'
if person == 'Subhmoy':
    used_materials = Subhmoy_materials
if person == 'Satvik':
    used_materials = Satvik_materials
#mols = ['2_N2','3_H2','4_N2H']
mols = ['3_H2']
cluster = 'narval'
for i in range(len(used_materials)):
    material = str(i) + '_' + used_materials[i]
    material_dir = f'/home/pagh/scratch/ML_project/{person}/' + material 
    for mol in mols:
        main_dir = material_dir + '/' + mol + '/'
        all_list = list(os.listdir(main_dir))
        print(len(all_list))
        directory_list = []
        for i in all_list:
            if 'ad_site' in i:
                directory_list.append(i)
        directory_list = sorted(directory_list,key=lambda x: int(re.findall(r'\d+', x)[0]))

        for ad_site in directory_list:
            os.chdir(main_dir + ad_site + '/')
            batch_source = open(main_dir + ad_site + '/' + f'submitVASP_{cluster}.sh','r')
            batch_main =  open(main_dir + ad_site + '/' + f'submitVASP_{cluster}_main.sh','w')
            for line in batch_source.readlines():
                if '#SBATCH --account' in line:
                    line = re.sub('#SBATCH --account.*',f"#SBATCH --account=ctb-ghumanku",line)
                if '#SBATCH --nodes=' in line:
                    line=re.sub('#SBATCH --nodes.*','#SBATCH --nodes=2',line)
                if  '#SBATCH --ntasks-per-node' in line:
                    line = re.sub('#SBATCH --ntasks-per-node.*','#SBATCH --ntasks-per-node=48',line)
                if  '#SBATCH --time=' in line:
                    line = re.sub('#SBATCH --time.*','#SBATCH --time=48:00:00',line)
                batch_main.write(line)
            batch_main.close()
            batch_source.close()
            os.remove(main_dir + ad_site + '/' + f'submitVASP_{cluster}.sh')
            os.rename(main_dir + ad_site + '/' + f'submitVASP_{cluster}_main.sh',main_dir + ad_site + '/' + f'submitVASP_{cluster}.sh')

