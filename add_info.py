# -*- coding:utf-8 -*-
import os
import pandas as pd


class add_info:
    """
    Extract info from sample info file.
    """
    def __init__(self, files, kwords=None, SID_name=None, PID_name=None):
        self.info_file = files
        self.which = kwords
        # ["PatientID", "SampleType", "CollectionDate", "Timepoint", "status"]
        self.SID_name = SID_name if SID_name else "SampleID"
        self.PID_name = PID_name if PID_name else "PatientID"
        self.coln_pair = {self.PID_name: "PatientID"}
        match kwords:
            case list() | tuple():
                self.coln_pair.update({i: i for i in kwords})
            case dict():
                self.coln_pair.update(kwords)

    ext_sep = {".tsv": "\t", ".txt": "\t", ".csv": ",", ".maf": "\t", ".xls": "\t"}

    def parse_file(self, fn, SID_name=None, PID_name=None):
        SP_df = dict()
        P_dic = dict()
        # df = pd.read_excel(fn, index_col=False)
        df = pd.read_csv(fn, index_col=False)
        df["SID_short"] = df[SID_name].apply(lambda x: x.split("-")[0])
        SP_df = df.set_index("SID_short")[self.coln_pair.values()].rename(
            columns=self.coln_pair
        )
        for idx, dic in df.iterrows():
            PID = dic[PID_name]
            SID = dic[SID_name]
            SID_short = SID.split("-")[0]
            if not P_dic.get(PID):
                P_dic[PID] = []
            P_dic[PID].append(SID_short)
        return SP_df, P_dic

    def get_info(self):
        self.SP_df, self.PS_dic = self.parse_file(
            self.info_file, SID_name=self.SID_name, PID_name=self.PID_name
        )

    def to_sample(
        self, infile, SID_name, skip=None, subset=None, outname=None, outext=None
    ):
        match infile:
            case str():
                filename, fileext = os.path.splitext(infile)

                if fileext == ".xlsx":
                    df = pd.read_excel(infile, skiprows=skip)
                else:
                    sep = self.ext_sep[fileext]
                    df = pd.read_csv(infile, sep=sep, skiprows=skip)

                if outext:
                    fileext = "." + outext
                    if fileext != ".xlsx":
                        sep = self.ext_sep[fileext]

                outfile = f"{filename}_add_info{fileext}"
            case pd.DataFrame():
                df = infile
                filename, fileext = os.path.splitext(outname)
                sep = self.ext_sep[fileext]
                outfile = f"{filename}_add_info{fileext}"
            case _:
                raise TypeError("File type not recognized...")

        df.rename(
            columns={
                "Start_position": "Start_Position",
                "End_position": "End_Position",
            },
            inplace=True,
        )

        df["SID_short"] = df[SID_name].apply(lambda SID: SID.split("-")[0])
        df = df.drop(columns=list(self.coln_pair.values()), errors="ignore")
        df2 = self.SP_df.join(df.set_index("SID_short"), how="right")

        if subset:
            dfo = df2[
                sorted(df.columns.intersection(subset).to_list(), key=subset.index)
            ]
        else:
            dfo = df2

        if fileext == ".xlsx":
            dfo.to_excel(outfile, index=False)
        else:
            dfo.to_csv(outfile, sep=sep, index=False)

    def df_to_sample(
        self,
        df,
        SID_name="SampleID",
        skip=None,
        subset=None,
    ):
        df.rename(
            columns={
                "Start_position": "Start_Position",
                "End_position": "End_Position",
            },
            inplace=True,
        )
        df["SID_short"] = df[SID_name].apply(lambda SID: SID.split("-")[0])
        df = df.drop(columns=list(self.coln_pair.values()), errors="ignore")

        df2 = self.SP_df.join(df.set_index("SID_short"), how="right")

        if subset:
            dfo = df2[
                sorted(df.columns.intersection(subset).to_list(), key=subset.index)
            ]
        else:
            dfo = df2

        return dfo