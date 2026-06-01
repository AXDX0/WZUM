from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.endpoints import leaguedashplayerstats, leaguedashteamstats
from sklearn.ensemble import RandomForestRegressor
import pandas as pd
import joblib


def trenowanie():
    dataset = pd.read_csv(
        "All-NBA_Teams_dane.csv"
    )

    rookies_dataset = pd.read_csv(
        "All-Rookie_Teams_dane.csv"
    )

    train = dataset[
        dataset["SEASON"] <= "2024-25"
    ]

    rookies_train = rookies_dataset[
        rookies_dataset["SEASON"] <= "2024-25"
    ]

    TARGET = "Pts Won"
    FEATURES = dataset.drop(columns=['Pts Won', 'PLAYER_ID', 'PLAYER_NAME', 'NICKNAME', 'TEAM_ID', 'TEAM_ABBREVIATION', 'TEAM_NAME', 'SEASON']).columns.tolist()

    X_train = train[FEATURES]
    y_train = train[TARGET]

    X_rookies_train = rookies_train[FEATURES]
    y_rookies_train = rookies_train[TARGET]

    model_rf = RandomForestRegressor(
        n_estimators=500,
        random_state=42,
        n_jobs=-1
    )

    model_rookies_rf = RandomForestRegressor(
        n_estimators=500,
        random_state=42,
        n_jobs=-1
    )

    model_rf.fit(
        X_train,
        y_train
    )

    model_rookies_rf.fit(
        X_rookies_train,
        y_rookies_train
    )

    joblib.dump(
        model_rf,
        "model_rf.pkl"
    )

    joblib.dump(
        model_rookies_rf,
        "model_rookies_rf.pkl"
    )


if __name__ == '__main__':
    trenowanie()