from cProfile import label
import plotly.express as px
import streamlit as st 

import pandas as pd


def readfromhtml(filepath):
    """
    x = readfromhtml(
        "https://fbref.com/en/comps/Big5/shooting/players/Big-5-European-Leagues-Stats"
    )
    """

    df = pd.read_html(filepath)[0]
    column_lst = list(df.columns)
    for index in range(len(column_lst)):
        column_lst[index] = column_lst[index][1]

    df.columns = column_lst
    df.drop(df[df["Player"] == "Player"].index, inplace=True)
    df = df.fillna("0")
    df.set_index("Rk", drop=True, inplace=True)
    try:
        df["Comp"] = df["Comp"].apply(lambda x: " ".join(x.split()[1:]))
        df["Nation"] = df["Nation"].astype(str)
        df["Nation"] = df["Nation"].apply(lambda x: x.split()[-1])
    except ValueError:
        print("Error in uploading file:" + filepath)
    finally:
        df = df.apply(pd.to_numeric, errors="ignore")
        return df
df_fbref = readfromhtml('https://fbref.com/en/comps/Big5/passing/players/Big-5-European-Leagues-Stats')

no_90s = 10
df_fil = df_fbref[df_fbref['90s']>=no_90s]
df_fil = df_fbref[df_fbref['90s']>=no_90s]
df_fil = df_fil[df_fil['Pos'].apply(lambda x: x in ['MF','MF,FW','FW,MF'])]


fig = px.scatter(df_fil, x=(df_fil['Prog']/df_fil["90s"]), y=(df_fil['Att'].iloc[:,0]/df_fil["90s"]),title='Prog/90 vs Att/90s', hover_data=['Player','Pos','Comp','Nation'], color="Player", size="90s",text="Player", labels={"x": "Prog/90", "y": "Att/90s"})
fig.update_traces(textposition="top center", width=1000, height=1000)
fig.show()
st.plotly_chart(fig, use_container_width=True)