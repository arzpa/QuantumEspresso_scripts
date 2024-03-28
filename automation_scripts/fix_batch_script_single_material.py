import os
import shutil
import re
mols = ['2_N2','3_H2','4_N2H']
cluster = 'narval'
material = str(input('Please enter material directory name:  '))
material_dir = '/home/pagh/scratch/ML_project/Subhmoy/' + material 
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
            if 'rrg' in line:
                line = re.sub('rrg',f"def",line)
            if '#SBATCH --nodes=' in line:
                line=re.sub('#SBATCH --nodes.*','#SBATCH --nodes=1',line)
            if  '#SBATCH --ntasks-per-node' in line:
                line = re.sub('#SBATCH --ntasks-per-node.*','#SBATCH --ntasks-per-node=64',line)
            if  '#SBATCH --time=' in line:
                line = re.sub('#SBATCH --time.*','#SBATCH --time=48:00:00',line)
            batch_main.write(line)
        batch_main.close()
        batch_source.close()
        os.remove(main_dir + ad_site + '/' + f'submitVASP_{cluster}.sh')
        os.rename(main_dir + ad_site + '/' + f'submitVASP_{cluster}_main.sh',main_dir + ad_site + '/' + f'submitVASP_{cluster}.sh')

