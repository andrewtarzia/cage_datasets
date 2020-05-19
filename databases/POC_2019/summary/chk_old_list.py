cd ../POC_manual/
import glob
old_list = glob.glob('*.cif')
cd ../POC_list_2/
old_list = [i.replace('.cif' , '') for i in old_list]
old_list = [i.replace('_nosolv' , '') for i in old_list]
old_list = [i.replace('_ordered' , '') for i in old_list]
old_list = [i.replace('_cleaned1' , '') for i in old_list]
old_list = set(old_list)
new_list = open('DB.gcd', 'r').readlines()
print(len(new_list))
new_list = [i.rstrip() for i in new_list]
new_list2 = open('post_pw.gcd', 'r').readlines()
new_list2 = [i.rstrip() for i in new_list2]
count = 0
for i in old_list:
    if i not in new_list:
        print(i)
        count += 1
print(count)
count = 0 
for i in old_list: 
    if i not in new_list2: 
        print(i) 
        count += 1 
print(count)

