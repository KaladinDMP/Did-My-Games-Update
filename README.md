# Did My Steam Games Update?

This script, compiled as an executable (`DidMyGamesUpdate.exe`), checks your Steam library for game updates and new games without the need to have them all installed. It's an easy way to keep track of updates for your extensive game collection.

## Features

- Fetches your owned games from the Steam API
- Loads all Steam games and their AppIDs
- Checks for new games in your library and adds them to the game data
- Fetches the latest build ID for each game and compares it with the stored build ID
- Identifies games that have been updated since the last check
- Saves the updated game data and a list of updated games with their old and new build IDs
- Generates a JSON file with the updated and new games for easy reference

## Prerequisites

- Windows operating system
- A Steam account
- A Steam API key (obtained from the [Steam Web API](https://steamcommunity.com/dev/apikey) page)
- Owned games on your Steam account

## Setup

1. Obtain a Steam API key from the [Steam Web API](https://steamcommunity.com/dev/apikey) page.
2. Create a file named `steam_credentials.txt` in the same directory as the `DidMyGamesUpdate.exe` file.
3. In the `steam_credentials.txt` file, enter your Steam API key (30 digit, letters and numbers) on the first line and your Steam User ID (17 numbers) on the second line, with nothing else in the file. 

For example:
```
YOUR_STEAM_API_KEY
YOUR_STEAM_ID
```
	 
4. Save the `steam_credentials.txt` file.

Note: If you don't create a `steam_credentials.txt` file, the script will prompt you to enter your Steam API key and Steam ID on the first run, and it will create the file for you.

## Usage

1. Run the `DidMyGamesUpdate.exe` file.
2. The script will load your game data from the `game_data.json` file (if it exists) and check for updates.
3. It will identify new games in your library and fetch their build IDs.
4. The script will compare the latest build ID with the stored build ID for each game to identify updates.
5. Updated games and new games will be saved in a JSON file named `newupdated[DATE][TIME].json` (e.g., `newupdated06.13.2024.14.30.json`) in the same directory as the executable.
6. The script will also update the `game_data.json` file with the latest build IDs.

## Output

The script generates a JSON file (`newupdated[DATE][TIME].json`) with the following structure:

```json
{
 "updated_games": {
     "appid1": {
         "name": "Game Name 1",
         "old_build_id": "1234567",
         "new_build_id": "1234568"
     },
     "appid2": {
         "name": "Game Name 2",
         "old_build_id": "7654321",
         "new_build_id": "7654322"
     }
 },
 "new_games": {
     "appid3": {
         "name": "New Game 1",
         "build_id": "1111111"
     },
     "appid4": {
         "name": "New Game 2",
         "build_id": "2222222"
     }
 }
}
```

## Logging
The script logs its progress and any errors encountered during execution. The log messages are displayed in the console and include timestamps and log levels (INFO or ERROR).


### Notes

- The script requires an active internet connection to fetch data from the Steam API.
- Ensure that your Steam API key and Steam ID are correct to avoid any issues.
- The script may take some time to complete depending on the size of your game library and the number of updates available.
