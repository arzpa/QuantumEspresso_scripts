import re
import os
import shutil
import filecmp


Subhmoy_materials_str = 'Co3Ni  CoPt3  CuPt   Fe3Co   FeCo  FeNi3  FePt3  NiPt VPt   VPt3  Zn11Co2  Zn13Co  Zn22Ni3 Zn3Cu  Zn8Cu5  ZnCu  ZnPt Co3Pt  Cu3Pt  CuPt7  Fe9Co7  FeNi  FePt   Ni3Pt  NiPt3  V3Pt VPt2  VPt8  Zn11Ni2  Zn13Fe  Zn35Cu17  Zn3Pt  Zn9Fe4  ZnNi  ZnPt3'

Subhmoy_materials = Subhmoy_materials_str.split()

Satvik_materials_str = 'Al13Fe4  Al3Ni   Al3Pt5  Al5Co2  AlCu3  AlNi3  AlV   V3Ni   VFe3 Al21Pt8  Al3Ni2  Al3V    Al9Co2   AlFe   AlPt   AlV3  V3Ni2  VNi2 Al2Cu    Al3Ni5  Al4Cu9  AlCo    AlFe3  AlPt2  V3Co  V4Zn5  VNi3 Al2Pt    Al3Pt2  Al4Ni3  AlCu    AlNi   AlPt3  V3Fe  VCo3   VZn3'

Satvik_materials = Satvik_materials_str.split()

person ='Satvik'
if person == 'Subhmoy':
    used_materials = Subhmoy_materials
if person == 'Satvik':
    used_materials = Satvik_materials

main_dir = f'/home/pagh/scratch/ML_project/{person}/'
cluster_name = 'narval'
rerun = True

not_converged_list = []
material_num_index = int(input('Please enter material index: '))
material = f'{material_num_index}_{used_materials[material_num_index]}'
mols = ['2_N2','3_H2']
for mol in mols:
    num_sites = []
    sites_dir = main_dir + material + '/' + mol + '/'
    for i in os.listdir(sites_dir):
        if '_ad_site' in i:
            num_sites.append(i)
    num_sites = sorted(num_sites, key=lambda x: int(re.findall(r'\d+', x)[0]))
    for site in num_sites:
        converged = 0
        if 'OUTCAR' in os.listdir(sites_dir + site + '/'):
            outcar = open(sites_dir + site + '/' + 'OUTCAR','r')
            outcar_lines = outcar.readlines()
            for line in outcar_lines:
                if 'reached required accuracy - stopping structural energy minimisation' in line:
                    converged = converged + 1
            outcar.close()
            if converged > 0:
                print(mol, site, 'CONVERGED')
            else:
                print(mol, site, 'NOT CONVERGED')
                mol_code = int(re.findall(r'\d+',mol)[0])
                site_code = int(re.findall(r'\d+',site)[0])
                notconv_code = f'{mol_code}/{site_code}'
                not_converged_list.append(notconv_code)
                #os.chdir(sites_dir + site + '/')
                all_files = os.listdir(sites_dir + site + '/')
                if 'incar_new' not in all_files:
                    os.mkdir(sites_dir + site + '/' + 'incar_new' + '/')
                incar_old = open(sites_dir + site + '/' + 'INCAR','r')
                incar_old_lines = incar_old.readlines()
                incar_new = open(sites_dir + site + '/' + 'incar_new' + '/' + 'INCAR', 'w')
                for line in incar_old_lines:
                    if 'ISTART' in line:
                        line = re.sub('ISTART.*',"ISTART = 1",line)
                    if 'ICHARG' in line:
                        line = re.sub('ICHARG.*',"ICHARG = 1",line)
                    incar_new.write(line)
                incar_old.close()
                incar_new.close()

                os.remove(sites_dir + site + '/' + 'INCAR')
                shutil.copy(sites_dir + site + '/' + 'incar_new' + '/' + 'INCAR', sites_dir + site + '/')
                shutil.copy(sites_dir + site + '/' + 'CONTCAR', sites_dir + site + '/' + 'POSCAR')
                os.remove(sites_dir + site + '/' + 'incar_new' + '/' + 'INCAR')
                if rerun:
                    outcars_list = []
                    for f in os.listdir(sites_dir + site + '/'):
                        if 'OUTCAR.' in f:
                            outcars_list.append(f)
                    if len(outcars_list) == 0:
                        shutil.copy(sites_dir + site + '/'  + 'OUTCAR', sites_dir + site + '/' + 'OUTCAR.1')
                        outcars_list = ['OUTCAR.1']
                    outcars_list = sorted(outcars_list, key=lambda x: int(re.findall(r'\d+', x)[0]))
                    last_outcar_number = int(re.findall(r'\d+', outcars_list[-1])[0])
                    if filecmp.cmp(sites_dir + site + '/' + 'OUTCAR',sites_dir + site + '/' + f'OUTCAR.{last_outcar_number}') == False:
                        shutil.copy(sites_dir + site + '/'  + 'OUTCAR', sites_dir + site + '/' + f'OUTCAR.{last_outcar_number + 1}')
                    
                    os.chdir(sites_dir + site + '/')
                    os.system(f'sbatch submitVASP_{cluster_name}.sh')
        else:
            print(mol, site, 'NO OUTCAR')
print(not_converged_list)
