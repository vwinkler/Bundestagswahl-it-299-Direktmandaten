#!/usr/bin/env python3
import argparse
import pandas as pd

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("kerg2_file", type=str)
    parser.add_argument("votes_csv_file", type=str)
    args = parser.parse_args()

    df = pd.read_csv(args.kerg2_file, skiprows=9, sep=";")
    df = df[(df["Wahlart"] == "BT") & (df["Gruppenart"] == "Partei")]
    df["Anzahl"] = df["Anzahl"].fillna(0)
    
    df_votes = df[(df["Gebietsart"] == "Wahlkreis") & (df["Stimme"] == 1)].copy()
    df_votes = df_votes[["Gebietsname", "Gruppenname", "Anzahl"]]
    df_votes = df_votes.rename(columns={"Gebietsname": "constituency",
                            "Gruppenname": "party", "Anzahl": "votes"})
    df_votes["votes"] = df_votes["votes"].astype(int)
    df_votes.to_csv(args.votes_csv_file, index=False)
