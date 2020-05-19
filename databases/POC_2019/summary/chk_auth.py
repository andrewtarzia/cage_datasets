old_list = ['ABIKUU', 'ABILAB', 'ABILEF', 'ABILIJ', 'ABILOP', 'ABILUV', 'ABIMAC', 'ABIMEG', 'ABIMIK', 'ABIMOQ', 'ABIMUW', 'ABINAD', 'ABINEH', 'ABINIL', 'ABINUX', 'ABIPAF', 'ABIPEJ', 'ABIQEK', 'ABIQIO', 'CAFJAX', 'CAFJEB', 'CANHOR', 'CAXFIT', 'CAXFOZ', 'DEDTOY', 'DEDTUE', 'DEDVAM', 'DEDVEQ', 'DENMIV', 'DENMUH', 'DENNAO', 'GICGUX', 'IFAJOR', 'IFAJUX', 'IFAKAE', 'IFAKEI', 'IFAKIM', 'IYEMAC', 'IYEMEG', 'IYEMIK', 'KENRED', 'MAGJUC', 'PAWSEO', 'PAWSIS', 'PIFHIY', 'PIFHUK', 'PIFJAS', 'PIFJEW', 'PIFJIA', 'PIFJOG', 'PIFJUM', 'PIFKAT', 'PIFKEX', 'PIFKIB', 'PIFKOH', 'PIFKUN', 'PIFTOQ', 'PIFTUW', 'PIFVAE', 'PIFVEI', 'PIFVIM', 'PIFVOS', 'PIFVUY', 'PIFWAF', 'REGDUF', 'REHCIT', 'RELZEQ', 'RELZIU', 'RELZOA', 'RELZUG', 'REMBAP', 'REMBET', 'SAVYAS', 'SENNOR', 'SENNUX', 'SENPAF', 'SENPIN', 'SENPOT', 'SENPUZ', 'SENQAG', 'SENQEK', 'SENQIO', 'SENQOU', 'SENQUA', 'SENRAH', 'SENREL', 'TASPUB', 'TASQAI', 'TASQEM', 'TASQIQ', 'TASQOW02', 'TASQOW', 'XAMQEK', 'XAMQIO', 'XAMQOU', 'XAMQUA', 'XAYMOC', 'XAYMUI', 'YEZLOH', 'YEZLUN', 'YEZMAU', 'YEZMIC', 'YEZMOI', 'YEZMUO', 'YEZNAV', 'YIGPOW', 'YIGQEN']
print(len(old_list))
new_list = open('DB.gcd', 'r').readlines()
print(len(new_list))
new_list = [i.rstrip() for i in new_list]
count = 0
for i in old_list:
    if i not in new_list:
        print(i)
        count += 1
print(count)

