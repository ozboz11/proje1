# app.py
import streamlit as st
import pandas as pd
from sklearn.neighbors import NearestNeighbors


# 1. Load data
@st.cache_data
def load_data():
    # Load the single combined dataset
    df = pd.read_csv("seasons_scaled/final_table.csv")
    return df

# Load once
df = load_data()

# 2. Sidebar inputs
st.sidebar.title("Player Similarity Explorer")
year = st.sidebar.selectbox(
    "Select Year:",
    sorted(df["season"].unique())
)
# Player selection filtered by year
player = st.sidebar.selectbox(
    "Select player:",
    sorted(df[df["season"] == year]["PLAYER_NAME"].unique())
)
# Minimum minutes filter
min_minutes = st.sidebar.slider(
    "Minimum minutes played:",
    int(df["MIN"].min()),
    int(df["MIN"].max()),
    25
)


all_features = df.drop(["PLAYER_NAME","MIN","GP","TEAM_ABBREVIATION","W_PCT","season","W","L","TEAM_ID"],axis=1).columns
feature_cols = st.sidebar.multiselect(
    "Select features to include:",
    options=all_features,
    default=["OFF_RATING", "DEF_RATING", "AST_PCT", "EFG_PCT", "TS_PCT"]
)

#
# 5. Prediction / similarity lookup
def find_closest_player(PLAYER_NAME,SEASON,MIN_THRESHOLD,feature_cols):
    MINUTES_COL = "MIN"

   

    # -----------------------------
    # 3. Build masks
    # -----------------------------
    mask_minutes = df[MINUTES_COL] >= MIN_THRESHOLD
    mask_me      = (df["PLAYER_NAME"] == PLAYER_NAME) & (df["season"] == SEASON)

    if mask_me.sum() != 1:
        raise ValueError(f"Expected exactly one row for {PLAYER_NAME}-{SEASON}, got {mask_me.sum()}.")
 

    # -----------------------------
    # 4. Prepare query & pool
    # -----------------------------
    # query row (still a 2-D array for scikit-learn)
    query_vec = (
        df.loc[mask_me, feature_cols]
        
        .to_numpy()
    )

    # pool = everyone else, minutes-qualified
    mask_pool  = (df["PLAYER_NAME"] != PLAYER_NAME) & mask_minutes
    df_pool    = (
        df.loc[mask_pool, feature_cols]
    )
    X_pool     = df_pool.to_numpy()



    # -----------------------------
    # 6. k-NN on scaled data
    # -----------------------------
    knn = NearestNeighbors(metric="cosine", n_neighbors=5)
    knn.fit(X_pool)

    dists, idxs   = knn.kneighbors(query_vec)
    similar       = df.loc[mask_pool].iloc[idxs[0]].copy()
    similar["cosine_distance"] = dists[0]

    return similar[["PLAYER_NAME", "season", "cosine_distance"]]

# 6. Display
st.header(f"Players similar to {player}")
sim_df = find_closest_player(player,year,min_minutes,feature_cols)
st.dataframe(sim_df)

