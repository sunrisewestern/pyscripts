#!/mnt/sdh/xiaoxi/.linuxbrew/bin/python3
#-*- coding:utf-8 -*-

import re

def getQCfromFILE(summary_file,SID,*args):
    summary = {}
    with open(summary_file,'r') as f:
        for idx,line in enumerate(f):
            ls = line.strip().split(",")
            if idx==0:
                ls0=ls
                continue
            dic = {ls0[i]:ls[i] for i in range(len(ls0))}
            SampleID = dic['#SAMPLE']
            summary[SampleID] = dic
            
    for _sid in summary.keys():
        if SID in _sid:
            dic = summary[_sid]
            values = [ dic.get(i,"NA") for i in args]
            if len(values)==1:
                values = values[0]
            return(values)
    else:
        raise KeyError(f"{SID} not found in Summary file")

if __name__ == "__main__":
    print(getQCfromFILE("P17010643209-T-CLN","MEDIAN_DEPTH"))


