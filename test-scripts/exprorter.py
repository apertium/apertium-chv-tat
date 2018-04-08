#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
print('USE python3.5 @scriptname.py ')
print('WHEN YOU DONT USE PYTHON 3.5 PRESS ENTER FOR EXIT ELSE enter filename without format')
print('required just  .txt')
def _remover(string):########<e><p><l>|тинĕс|<s n="|n|"/></l><r>|диңгез|<s n="|n|"/></r></p></e>
    string=string.split(',')#
    for x in range(len(string)):
        string[x].replace(' ','')
    return string
def truer(string):
    lib=[]
    string=string.replace('"','')
    if len(string)==0:
        return string
    if string[0]==' ':
        string=string.replace(' ','')
        for x in range(len(string)):
            if string[x]==' ':
                string=string.replace(' ','<b/>')
                break
    return string
def fixer(string):
    liba=['adj+adv','adj','adj','adj']
    preva=['A1','A2','A3','A4']
    for x in range(len(preva)):
        if string==preva[x]:
            return liba[x]
    lib=['n','n','adv']
    prev=['N1','N1-RUS','ADV']
    for x in range(len(lib)):
        if string==prev[x]:
            string=lib[x]
            #print(string)
            return string
    for x in range(len(lib)):
        if string[0:len(lib[x])]==lib[x].upper():
                  string=lib[x]
                  #print(string)
                  return string
    libv=['v-tv','v-tv','v-iv','v-iv']
    prev=['V-TV-IR','V-TV-AR','V-IV-AR','V-IV-IR']
    for x in range(len(libv)):
        if string[0:len(libv[x])]==libv[x].upper():
            string=libv[x]
            string=string.replace(libv[x],'v"/><s n="'+libv[x][2:]+'\'')
            return string
            #<e><p><l>йӗркеле<s n="v"/><s n="tv"/></l><r>оештыр<s n="v"/><s n="tv"/></r></p></e>
            #<e><p><l>хыҫ<s n="v"/><s n="tv"/></l><r>арт<s n="v"/><s n="tv"/></r></p></e>
            #<e><p><l>хыҫ<s n="v-iv"/></l><r>арт<s n="v-iv"/></r></p></e>
    return string
def verb(string):
    #v"/><s n="tv
    exit
def proc(lstapp,listin):
    data=['adj','adv']
    p1='<e><p><l>'#тинĕс
    p2='<s n="'#n
    p3='"/></l><r>'#диңгез
    p4='<s n="'#n
    p5='"/></r></p></e>'
    more='<b/>'
    Np1='<e r="LR"><p><l>'#<e r="LR"><p><l>Np1|аборт|<s n="2|n|"/></l><r>3|аборт|<s n="4|n|"/></r></p></e>5
    pl=fixer(listin[2])
    comm=''
    if listin[2]==pl or listin[2]=='A3' or listin[2]=='A4' :
        comm='    <!--CHECK THIS (A3,A4) OR SMTHNG -->'
    pr=truer(listin[1])
    if pl=='adj+adv':
        for n in range(len(data)):
            if len(listin)>6:
                add=p1+listin[3]+p2+data[n]+p3+pr+p4+data[n]+p5
                #print(add)
                lstapp.append(add)
               # print(listin[2],' ',add)
                for k in range(len(listin)-6):
                    add=Np1+truer(listin[3+k+1])+p2+data[n]+p3+pr+p4+data[n]+p5+comm
                    #print(add)
                    lstapp.append(add)
                    #print(listin[2],' ',add)
            if len(listin)==6 and listin[3]!='':
                string=p1+listin[3]+p2+data[n]+p3+pr+p4+data[n]+p5+comm
                lstapp.append(string)
                #print(listin[2],' ',string)
        return
    if len(listin)>6:
        add=p1+listin[3]+p2+pl+p3+pr+p4+pl+p5
        #print(add)
        lstapp.append(add)
        #print(x,' ',add)
        for k in range(len(listin)-6):
            add=Np1+truer(listin[3+k+1])+p2+pl+p3+pr+p4+pl+p5+comm
            #print(add)
            lstapp.append(add)
            #print(x,' ',add)
    if len(listin)==6 and listin[3]!='':
        string=p1+listin[3]+p2+pl+p3+pr+p4+pl+p5+comm
        lstapp.append(string)
        #print(x,' ',string)
filename=input()
if filename=='':
    raise SystemExit
f=open(filename+'.txt','r',encoding='utf-8')
tff=f.readlines()
f.close()
fout=open(filename+'out'+'.txt','w',encoding='utf-8')
lst=[]
for x in range(len(tff)):
    if x==0:
        continue
    tff[x]=_remover(tff[x])
    #print(tff[x])
    proc(lst,tff[x])
#for x in range(len(lst)):
#    print(lst[x])
for x in range(len(lst)):
    fout.write(lst[x]+'\n')
print('DONE! check ',filename+'out.txt')
fout.close()
