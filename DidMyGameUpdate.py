import requests
import json
import logging
import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 1. Read API key and Steam ID from a text file
with open('steam_credentials.txt', 'r') as file:
    lines = file.readlines()
    USER_API_KEY = lines[0].strip()
    USER_STEAM_ID = lines[1].strip()

# 2. Fetch owned games
user_url = f'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={USER_API_KEY}&steamid={USER_STEAM_ID}&format=json'
user_game_data = requests.get(url=user_url).json()
games_owned_id = {game['appid'] for game in user_game_data['response']['games']}

# 3. Load all Steam games
api = 'https://api.steampowered.com/ISteamApps/GetAppList/v2/'
res = requests.get(url=api)
dict = res.json()['applist']['apps']
data_clean = {game['appid']: game['name'] for game in dict}

def get_name(appid):
    return data_clean.get(appid, "Unknown Game")

def fetch_steam_api_data(appid):
    try:
        response = requests.get(f'https://api.steamcmd.net/v1/info/{appid}')
        data = response.json()
        return data['data'][str(appid)]['depots']['branches']['public']['buildid']
    except (KeyError, json.JSONDecodeError):
        return None

def load_game_data():
    try:
        with open('game_data.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_game_data(data):
    with open('game_data.json', 'w') as file:
        json.dump(data, file, indent=4)

def check_for_updates():
    logging.info("Checking for updates...")
    game_data = load_game_data()
    updated_games = {}
    new_games = {}
    
    # 5a. Check for new games and add them to the dictionary
    for appid in games_owned_id:
        if appid not in game_data:
            game_name = get_name(appid)
            new_games[appid] = {'name': game_name, 'build_id': None}
            game_data[appid] = {'name': game_name, 'build_id': None}
            logging.info(f"New game found: {game_name} (AppID: {appid})")
    logging.info(f"{len(new_games)} new games found. Proceeding to fetch build IDs.")
   
    build_ids_added = 0
    games_updated = 0
    games_to_remove = []
    
    # 5b. Fetch the latest build id for each game
    for appid, info in game_data.items():
        logging.info(f"Fetching build ID for {info['name']} (AppID: {appid})")
        newest_build_id = fetch_steam_api_data(appid)
        if newest_build_id:
            if info['build_id'] is None:
                # 5c. First time fetching build id for this game
                game_data[appid]['build_id'] = newest_build_id
                build_ids_added += 1
                logging.info(f"First time fetching build ID for {info['name']} (AppID: {appid})")
            else:
                current_build_id = info['build_id']
                if int(newest_build_id) > int(current_build_id):
                    # 5c. Game has been updated
                    updated_games[appid] = {'name': game_data[appid]['name'], 'old_build_id': current_build_id, 'new_build_id': newest_build_id}
                    game_data[appid]['build_id'] = newest_build_id
                    games_updated += 1
                    logging.info(f"Update found for {info['name']} (AppID: {appid})")
        else:
            # Add the AppID to the list of games to be removed
            games_to_remove.append(appid)
            logging.info(f"Marked {info['name']} (AppID: {appid}) for removal due to null build ID.")
    
    # Remove games with null build IDs from game_data
    for appid in games_to_remove:
        game_data.pop(appid, None)
        logging.info(f"Removed game with AppID: {appid} from game data due to null build ID.")
    
    # Remove games with null build IDs from new_games
    new_games = {appid: info for appid, info in new_games.items() if info['build_id'] is not None}
    
    # 5d. Save the updated game data
    save_game_data(game_data)
    logging.info(f"Added build IDs for {build_ids_added} games.")
    logging.info(f"{games_updated} games had updates.")
    logging.info("Update check completed.")
    return updated_games, new_games

def save_updated_games(updated_games, new_games):
    now = datetime.datetime.now()
    filename = f"newupdated{now.strftime('%m.%d.%Y.%H.%M')}.json"
    data = {
        "updated_games": updated_games,
        "new_games": new_games
    }
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)
    logging.info(f"Saved updated games to {filename}")

def main():
    logging.info("Starting script...")
    updated_games, new_games = check_for_updates()
    if updated_games or new_games:
        save_updated_games(updated_games, new_games)
    else:
        logging.info("No updates found.")

    logging.info("Script completed.")
    exit()

if __name__ == "__main__":
    main()
