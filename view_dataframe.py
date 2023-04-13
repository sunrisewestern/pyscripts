#!/usr/bin/env python3.10
# -*-coding:utf-8 -*-
import pandas as pd
import subprocess
import tempfile


def view(df):
    if isinstance(df, pd.DataFrame):
        temp = tempfile.NamedTemporaryFile(suffix=".xlsx")
        df.to_excel(temp)
        subprocess.Popen(["open", "-a", "Microsoft Excel", rf"{temp.name}"])
    else:
        raise ValueError("Only take pandas dataframe as input.")


if __name__ == "__main__":
    import numpy as np

    df = pd.DataFrame(np.random.randint(0, 100, size=(100, 4)), columns=list("ABCD"))
    df2 = df.copy()
    df2.columns = pd.MultiIndex.from_product([df2.columns, [""]])
    df3 = df2.copy()
    df3.columns = pd.MultiIndex.from_tuples(
        [
            ("A", 0),
            ("A", 1),
            ("A", 2),
            ("A", 3),
        ]
    )
    view(df3)
