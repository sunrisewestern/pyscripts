# -*- coding:utf-8 -*-

import pandas as pd


def make_db_maf(filename, level=1, skip=None):
    df = pd.read_csv(filename, sep="\t", skiprows=skip)

    if level == 1:
        df = df[df["ONCOGENIC"].eq("Oncogenic")]
    else:
        df = df[df["ONCOGENIC"].str.contains("Oncogenic")]
    df.rename(
        columns={"Start_position": "Start_Position", "End_position": "End_Position"},
        inplace=True,
    )
    df["Chromosome"] = df["Chromosome"].apply(lambda x: str(x).strip("cChr"))
    df = df[
        [
            "Chromosome",
            "Start_Position",
            "End_Position",
            "Reference_Allele",
            "Tumor_Seq_Allele2",
            "HGVSp_Short",
        ]
    ]
    db = {"-".join(map(str, row[1:6])): row[6] for row in df.itertuples()}
    return db


def check_mut(
    chromo=None,
    start=None,
    end=None,
    ref=None,
    alt=None,
    db=None,
    skip=None,
    *,
    HGVSp_Short=None
):
    if isinstance(db, str):
        db = make_db_maf(db, skip)
    if chromo and start and end and ref and alt:
        mut = "-".join(map(str, (chromo, start, end, ref, alt)))
        if db.get(mut):
            return True
        else:
            return False
    else:
        if HGVSp_Short:
            if HGVSp_Short in db.values():
                return True
            else:
                return False


if __name__ == "__main__":
    filename = "../database/Oncokb20210510/Cosmic91_oncokb_annotator_20210510.tsv"

    check_mut(1, 1688745, 1688745, "T", "A", db)
