# app.py
import streamlit as st
import pandas as pd
from sklearn.neighbors import NearestNeighbors
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

st.set_page_config(
    page_title="🔍 Player Similarity",
    page_icon="🔍",
    layout="wide"
)

st.title("Player Similarity")
st.write("Sol taraftaki widgetlarla metrik ekleyebilirsiniz ve yıl seçebilirsiniz.")

# 1. Load data
@st.cache_data
def load_data():
    # locate this file’s directory
    base_dir = Path(__file__).parent
    csv_path = base_dir  / "final_table.csv"
    if not csv_path.exists():
        st.error(f"Couldn't find data at {csv_path}")
        return pd.DataFrame()  # or raise an exception
    return pd.read_csv(csv_path, index_col=0)

df = load_data()
# Load once



tab1, tab2 = st.tabs(["Player Similarity", "Player Seperation"])

with tab1:
# 2. Sidebar inputs
    st.sidebar.title("Player Similarity Explorer")
    year = st.sidebar.selectbox(
        "Select Year:",
        sorted(df["season"].unique())
    )
    # Player selection filtered by year
    player = st.sidebar.selectbox(
        "Select player:",
        sorted(df[df["season"] == year]["PLAYER_NAME"].unique()))
    # Minimum minutes filter
    min_minutes = st.sidebar.slider(
        "Minimum minutes played:",
        int(df["MIN"].min()),
        int(df["MIN"].max()),
        25)

    advanced_features_in = st.checkbox("Use advanced stats subset.")
    traditional_features_in = st.checkbox("Use traditional stats subset.")
    ## shooting features ?

    advanced_features = ["DEF_RATING","OFF_RATING","EFG_PCT","TS_PCT","PIE","POSS","OREB_PCT","DREB_PCT",'PCT_PTS_2PT',
       'PCT_PTS_2PT_MR', 'PCT_PTS_3PT','PCT_PTS_PAINT', 'PCT_AST_2PM', 'PCT_UAST_2PM', 'PCT_AST_3PM',
       'PCT_UAST_3PM',"PTS","FGA","FGM","STL","BLK","AST_RATIO","AST_PCT","AST_TO"]

    traditional_features = ["PTS","AST","REB",'FGM', 'FGA', 'FG3M', 'FG3A',"DREB","OREB","TOV","STL","BLK"]

    all_features = df.drop(["PLAYER_NAME","MIN","GP","TEAM_ABBREVIATION","W_PCT","season","W","L","TEAM_ID"],axis=1).columns
    if advanced_features_in and traditional_features_in:
        default_features = list(set(advanced_features+traditional_features))
        st.info("ADVANCED AND TRADITIONAL FEATURES ARE SELECTED", icon = "ℹ️")
    elif traditional_features_in:
        default_features =  traditional_features
    elif advanced_features_in:
        default_features =  advanced_features
    else:
        default_features = ["PTS","AST","BLK","STL","OREB","DREB"]
        st.info("You can choose more features.")
    
    feature_cols = st.sidebar.multiselect(
            "Select features to include:",
            options=all_features,
            default=default_features
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

with tab2:
    st.header(f"Detailed breakdown of top 6 seperated metric for: {player}")

    def calculate_top_n_cols(n_features: int, season: int, min_minutes: int, player: str):
        try:
            row = (
                df[
                    (df["season"] == season) &
                    (df["MIN"] >= min_minutes) &
                    (df["PLAYER_NAME"] == player)
                ]
                .drop(["PLAYER_NAME", "TEAM_ABBREVIATION", "TEAM_ID", "season", "GP", "W", "L", "MIN"], axis=1)
                .iloc[0]
            )

            topn_cols = abs(row).nlargest(n_features).index.tolist()
            return topn_cols

        except IndexError:
            print(f"[!] No matching row found for {player} in {season} with at least {min_minutes} minutes.")
            return []  # or return None or raise a custom error if desired


    top_cols = calculate_top_n_cols(6,year,min_minutes,player)

    def plot_single_metric(
        ax, df, player: str, season: int, min_minutes: float,
        metric: str, bins: int = 20
    ):
        """
        Draws on the given Axes:
        - a histogram of `metric` for all players in `season` with MIN>=min_minutes
        - a blue dotted line at the median
        - a red dashed line at the chosen player's value
        """
        if len(metric) == 0 :
            print("NOTHING TO PRINT")
            
        else:
        # filter the season & minutes
            season_df = df[(df["season"] == season) & (df["MIN"] >= min_minutes)]
            data = season_df[metric].dropna()

            # compute median
            med = data.median()

            # find the player's value
            vals = df.loc[
                (df["PLAYER_NAME"] == player) & (df["season"] == season),
                metric
            ].values
            player_val = vals[0] if len(vals) else None

            # plot histogram
            ax.hist(data, bins=bins, edgecolor="black")
            ax.set_title(f"{metric} in {season}")
            ax.set_xlabel(metric)
            ax.set_ylabel("Count")

            # median line
            ax.axvline(med,
                    color="blue",
                    linestyle=":",
                    linewidth=2,
                    label=f"Median: {med:.2f}")

            # player line
            if player_val is not None:
                ax.axvline(player_val,
                        color="red",
                        linestyle="--",
                        linewidth=2,
                        label=f"{player}: {player_val:.2f}")

            ax.legend()


    def plot_metrics_grid(
        df, player: str, season: int, min_minutes: float,
        metrics: list[str], bins: int = 20,
        ncols: int = 2, figsize: tuple[int,int] = (12, 12)
    ):
        """
        Builds a grid of subplots (nrows x ncols) for the given list of metrics.
        Returns the Figure.
        """
      
        n = len(metrics)
        if n > 0 :
            nrows = (n + ncols - 1) // ncols
            fig, axes = plt.subplots(nrows, ncols, figsize=figsize)
            axes = axes.flatten()

            for ax, metric in zip(axes, metrics):
                plot_single_metric(ax, df, player, season, min_minutes, metric, bins=bins)

            # turn off any unused axes
            for ax in axes[n:]:
                ax.axis("off")

            fig.tight_layout()
            return fig

    if len(top_cols) > 0 :
        fig = plot_metrics_grid(
            df=df,
            player=player,
            season=year,
            min_minutes=min_minutes,
            metrics=top_cols,
            bins=20,
            ncols=2,
            figsize=(12, 12)
        )
        st.pyplot(fig)

    else:
        st.warning("You should lower the selected minutes for player min_minutes!")

    