# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.endpoints import leaguedashplayerstats, leaguedashteamstats
from sklearn.ensemble import RandomForestRegressor
import pandas as pd


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


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

    valid = dataset[
        dataset["SEASON"] == "2025-26"
        ]

    rookies_train = rookies_dataset[
        rookies_dataset["SEASON"] <= "2024-25"
    ]

    rookies_valid = rookies_dataset[
        rookies_dataset["SEASON"] == "2025-26"
        ]

    TARGET = "Pts Won"
    FEATURES = dataset.drop(columns=['Pts Won', 'PLAYER_ID', 'PLAYER_NAME', 'NICKNAME', 'TEAM_ID', 'TEAM_ABBREVIATION', 'TEAM_NAME', 'SEASON']).columns.tolist()

    X_train = train[FEATURES]
    y_train = train[TARGET]

    X_valid = valid[FEATURES]
    # y_valid = valid[TARGET]
    season_2026 = valid

    X_rookies_train = rookies_train[FEATURES]
    y_rookies_train = rookies_train[TARGET]

    X_rookies_valid = rookies_valid[FEATURES]
    # y_rookies_valid = rookies_valid[TARGET]
    rookies_2026 = rookies_valid

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

    import json
    import sys

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

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # print_hi('PyCharm')
    trenowanie()