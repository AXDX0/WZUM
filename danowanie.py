from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.endpoints import leaguedashplayerstats, leaguedashteamstats
import pandas as pd
# import requests


def danowanie():
    ##
    seasons = ["2025-26", "2024-25"]
    measure_types_player = ["Base", "Advanced", "Usage", "Misc", "Scoring", "Defense"]
    measure_type_team = ["Base", "Advanced", "Misc", "Scoring", "Defense", "Four Factors", "Opponent"]
    dfs = []
    for season in seasons:
        players_stats = []
        for measure_type in measure_types_player:
            player_stats = leaguedashplayerstats.LeagueDashPlayerStats(
                season=season,
                per_mode_detailed="PerGame",
                measure_type_detailed_defense=measure_type
            ).get_data_frames()[0]
            players_stats.append(player_stats)
        df_players = pd.concat(
            players_stats,
            axis='columns'
        )
        df_players = df_players.loc[:, ~df_players.columns.duplicated()]
        # print(df_players.columns.tolist())
        # print(df_players.head().to_string())

        ##
        teams_stats = []
        for measure_type in measure_type_team:
            team_stats = leaguedashteamstats.LeagueDashTeamStats(
                season=season,
                measure_type_detailed_defense=measure_type
            ).get_data_frames()[0]
            teams_stats.append(team_stats)
        df_teams = pd.concat(
            teams_stats,
            axis='columns'
        )
        df_teams = df_teams.loc[:, ~df_teams.columns.duplicated()]
        # print(df_teams.columns.tolist())
        # print(df_teams.head().to_string())

        ##
        df = df_players.merge(
            df_teams,
            on="TEAM_ID",
            how="left"
        )

        voting = pd.read_csv(
            "All-NBA_Teams_" + season + ".csv"
        )
        voting.columns = voting.iloc[0]
        # voting.columns = voting.columns.str.lstrip("0")
        voting = voting[1:]
        voting = voting.reset_index(drop=True)
        voting.rename(columns={'Player': 'PLAYER_NAME'}, inplace=True)
        voting = voting[['PLAYER_NAME', 'Pts Won']]
        # print(voting.head().to_string())
        df = df.merge(
            voting,
            on=[
                # "SEASON",
                "PLAYER_NAME"
            ],
            how="left"
        )
        df["Pts Won"] = (
            df["Pts Won"]
            .fillna(0)
        )

        ##
        df["SEASON"] = season

        ##
        dfs.append(df)
    dataset = pd.concat(
        dfs,
        ignore_index=True
    )
    # print(dataset.columns.tolist())
    # print(dataset.head().to_string())

    dataset.to_csv(
        "All-NBA_Teams_dane.csv",
        index=False
    )


if __name__ == '__main__':
    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    #     'Accept': 'application/json, text/plain, */*',
    #     'Accept-Language': 'en-US,en;q=0.9,pl;q=0.8',
    #     'Origin': 'https://www.nba.com',
    #     'Referer': 'https://nba.com',
    # }
    # response = requests.get('https://stats.nba.com', timeout=60)
    danowanie()