from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.endpoints import leaguedashplayerstats, leaguedashteamstats
from sklearn.ensemble import RandomForestRegressor
import pandas as pd
import joblib
import json
import sys


def trenowanie():
    dataset = pd.read_csv(
        "All-NBA_Teams_dane.csv"
    )

    rookies_dataset = pd.read_csv(
        "All-Rookie_Teams_dane.csv"
    )

    valid = dataset[
        dataset["SEASON"] == "2025-26"
        ]

    rookies_valid = rookies_dataset[
        rookies_dataset["SEASON"] == "2025-26"
        ]


    # TARGET = "Pts Won"
    FEATURES = dataset.drop(columns=['Pts Won', 'PLAYER_ID', 'PLAYER_NAME', 'NICKNAME', 'TEAM_ID', 'TEAM_ABBREVIATION', 'TEAM_NAME', 'SEASON']).columns.tolist()

    X_valid = valid[FEATURES]
    # y_valid = valid[TARGET]
    season_2026 = valid

    X_rookies_valid = rookies_valid[FEATURES]
    # y_rookies_valid = rookies_valid[TARGET]
    rookies_2026 = rookies_valid

    model_rf = joblib.load(
        "model_rf.pkl"
    )

    model_rookies_rf = joblib.load(
        "model_rookies_rf.pkl"
    )

    season_2026["Pts Won"] = (
    # season_2026.loc[:, "Pts Won"] = (
        model_rf.predict(
            X_valid
        )
    )

    season_2026 = (
        season_2026
        .sort_values(
            "Pts Won",
            ascending=False
        )
    )

    rookies_2026["Pts Won"] = (
        model_rookies_rf.predict(
            X_rookies_valid
        )
    )

    rookies_2026 = (
        rookies_2026
        .sort_values(
            "Pts Won",
            ascending=False
        )
    )

    first_team = (
        season_2026
        .head(5)["PLAYER_NAME"]
        .tolist()
    )

    second_team = (
        season_2026
        .iloc[5:10]["PLAYER_NAME"]
        .tolist()
    )

    third_team = (
        season_2026
        .iloc[10:15]["PLAYER_NAME"]
        .tolist()
    )

    first_rookie_team = (
        rookies_2026
        .head(5)["PLAYER_NAME"]
        .tolist()
    )

    second_rookie_team = (
        rookies_2026
        .iloc[5:10]["PLAYER_NAME"]
        .tolist()
    )

    result = {
        "first all-nba team": first_team,
        "second all-nba team": second_team,
        "third all-nba team": third_team,
        "first rookie all-nba team": first_rookie_team,
        "second rookie all-nba team": second_rookie_team
    }

    if len(sys.argv) > 1:
        output_path = sys.argv[1]
    try:
        with open(output_path, "w") as f:
            json.dump(
                result,
                f,
                indent=2
            )
    except Exception:
        print("Należy podać jeden parametr przekazany w linii poleceń: bezwzględną ścieżką do nieistniejącego pliku wyjściowego (podawaną jako np. /home/WZUM_projec/Nazwisko_Imie.json).")


if __name__ == '__main__':
    trenowanie()