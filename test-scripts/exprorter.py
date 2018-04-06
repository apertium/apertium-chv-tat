#!/usr/bin/env python
# -*- coding: utf-8 -*-
def _remover(string):
    string=string.split(',')
    for x in range(len(string)):
        string[x].replace(' ','')
    return string
def truer(string):
    lib=[]
    string=string.replace('"','')
    if string[0]==' ':
        string=string.replace(' ','')
    for x in range(len(string)):
        if string[x]==' ':
            string=string.replace(' ','<b/>')
            break
    return string
def fixer(string):
    lib=['n','n','adv','v']
    prev=['N1','N1-RUS','ADV','V']
    for x in range(len(lib)):
        if string==prev[x]:
            string=lib[x]
            return string
    for x in range(len(lib)):
        if string[0:len(lib[x])]==lib[x].upper():
                  string=lib[x]
                  return string
filename=input('Enter .csv filename(example inputtext !without format, just .txt!)')
f=open(filename+'.txt','r',encoding='utf-8')
tff=f.readlines()
f.close()
fout=open(filename+'out'+'.txt','w',encoding='utf-8')
part1='<e><p><l>'
part2='<s n="'
part3='"/></l><r>'
part4='<s n="'
part5='"/></r></p></e>'
more='<b/>'
spart1='<e r="LR"><p><l>'#
lst=[]
for x in range(len(tff)):
    if x==0:
        continue
    tff[x]=_remover(tff[x])
    pl=fixer(tff[x][2])
    if len(tff[x])>6:
        add=part1+truer(tff[x][3])+part2+pl+part3+tff[x][1]+part4+pl+part5
        lst.append(add)
        for k in range(len(tff[x])-6):
            add=spart1+truer(tff[x][3+k+1])+part2+pl+part3+tff[x][1]+part4+pl+part5
            lst.append(add)
    if len(tff[x])==6 and tff[x][3]!='':
        string=part1+tff[x][3]+part2+pl+part3+tff[x][1]+part4+pl+part5
        lst.append(string)
for x in range(len(lst)):
    print(lst[x])
for x in range(len(lst)):
    fout.write(lst[x]+'\n')
fout.close()


