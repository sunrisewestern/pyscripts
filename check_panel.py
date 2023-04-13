#!/mnt/sdh/xiaoxi/.linuxbrew/bin/python3
#-*- coding:utf-8 -*-

"""
    if mutation position in panel region:
        return True
    else:
        return False
"""
from tabix import tabix_bed

panel_path = {
        "Goliath" : "/mnt/sdh/xiaoxi/database/bed/Goliath.add.bed.gz"
        }

def check_panel( panel,chromo,start,end ):
    try:
        bedfile = panel_path[panel]
    except KeyError:
        print("Not a valid panel name!")
    
    out = tabix_bed(bedfile,'bed',chromo,start,end)
    if len( a:=[i for i in out])>0:
        return(True)
    else:
        return(False)
    
