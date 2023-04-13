#!/mnt/sdh/xiaoxi/.linuxbrew/bin/python3
#-*- coding:utf-8 -*-

import re
from pybedtools import BedTool
from pybedtools.helpers import BEDToolsError

SID_dic = {}
plist = '/mnt/sdh/xiaoxi/06_EGFR_mining/row_data/SUMMARY-PASS20200515.csv'
with open(plist,'r') as f:
    for idx,line in enumerate(f):
        ls = line.strip().split(",")
        if idx==0:
            ls0=ls
            continue
        dic = { ls0[i]:ls[i] for i in range(len(ls))}
        SID = dic["#SAMPLE"]
        cfg = dic['CONFIGPATH'].split("/")[-1]
        SID_dic[SID] = cfg 

cfg_dic = {}
with open('/mnt/sdh/xiaoxi/database/bed/bed.list','r') as f:
    while 1:
        line = f.readline()
        if ".cfg" in line:
            cfg = line.strip()
            line = f.readline()
            ls = line.strip().split()
            bedname = ls[-1].split("/")[-1]
            cfg_dic[cfg] = bedname
        if not line:
            break

beds = {}
genes = {}
for bedname in list(set(list(cfg_dic.values()))):
    bedfile = "/mnt/sdh/xiaoxi/database/bed/"+bedname
    refer_bed = BedTool(bedfile)
    beds[bedname] = refer_bed
    genelist=[]
    with open(bedfile,'r') as f:
        genelist = [ line.strip().split()[3].split(":")[0] for line in f]
    genelist = list(set(genelist))
    genes[bedname] = genelist


def check_bed(mut,SID):
    bedname = cfg_dic[SID_dic[SID]]
    match = re.match(r'chr(\d+):(\d+)-chr\d+:(\d+)-.+-.+',mut)
    if match:
        chromo,start,end = re.match(r'chr(\d+):(\d+)-chr\d+:(\d+)-.+-.+',mut).groups()
        refer_bed = beds[bedname]
        mybed = BedTool(f'{chromo}\t{start}\t{end}',from_string=True)
        try:
            intersect = mybed.intersect(refer_bed,u=True,f=0.5)
        except BEDToolsError: 
            return("OUT")
        if intersect!="":
            return("IN")
        else:
            return("OUT")
    else:
        gene = mut
        if mut in genes[bedname]:
            return("IN")
        else:
            return("OUT")

def check_inbed(mut,bed):
    bedname = cfg_dic[bed]
    match = re.match(r'chr(\d+):(\d+)-chr\d+:(\d+)-.+-.+',mut)
    if match:
        chromo,start,end = re.match(r'chr(\d+):(\d+)-chr\d+:(\d+)-.+-.+',mut).groups()
        refer_bed = beds[bedname]
        mybed = BedTool(f'{chromo}\t{start}\t{end}',from_string=True)
        try:
            intersect = mybed.intersect(refer_bed,u=True,f=0.5)
        except BEDToolsError:
            return("OUT")
        if intersect!="":
            return("IN")
        else:
            return("OUT")
    else:
        gene = mut
        if mut in genes[bedname]:
            return("IN")
        else:
            return("OUT")

   
if __name__ == "__main__":
    a=check_bed("chr2:294513343798-chr2:2945353531798-A-A",'P180518120513-T-CLN')
    b=check_bed("chr2:29451798-chr2:29451798-A-A",'P180518120513-T-CLN')
    c=check_bed("ERBB2",'P180518120513-T-CLN')
    print(b,c)
    
