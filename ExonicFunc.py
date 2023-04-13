# -*- coding:utf-8 -*-

"""
    stop_gained = Nonsense Mutation
    silent = Synonymous mutations
"""


def trans_panel(func):
    funcs = func.split("&")
    if "stop_gained" in funcs:
        return "Nonsense mutation"
    if "start_lost" in funcs:
        return "Start-loss mutation"
    elif "stop_lost" in funcs:
        return "Nonstop mutation"
    elif "frameshift_variant" in funcs:
        return "Frameshift variant"
    elif "missense_variant" in funcs:
        return "Missense mutation"
    elif "inframe_insertion" in funcs or "inframe_deletion" in funcs:
        return "Inframe indel"
    elif "splice_donor_variant" in funcs or "splice_acceptor_variant" in funcs:
        return "Splice site variant"
    elif "5_prime_UTR_variant" in funcs or "3_prime_UTR_variant" in funcs:
        return None
    else:
        print(func)
        return None


def trans_maf(func):
    if "Nonsense_Mutation" == func:
        return "Nonsense mutation"
    if "Translation_Start_Site" == func:
        return "Start-loss mutation"
    elif "Nonstop_Mutation" == func:
        return "Nonstop mutation"
    elif "Frame_Shift_Ins" == func or "Frame_Shift_Del" == func:
        return "Frameshift variant"
    elif "Missense_Mutation" == func:
        return "Missense mutation"
    elif "In_Frame_Ins" == func or "In_Frame_Del" == func:
        return "Inframe indel"
    elif "Splice_Site" == func:
        return "Splice site variant"
    elif func in ["5'UTR", "3'UTR", "5'Flank", "3'Flank"]:
        return None
    elif "Silent" == func:
        return None
    elif "Intron" == func or "Splice_Region" == func:
        return None
    else:
        print(func)
        return None
