import os
import subprocess
import time
import urllib.request
from bs4 import BeautifulSoup

max_attempts = 10  # Maximum number of attempts
attempt_delay = 10  # Number of seconds to wait between attempts

# URL to download SteamCMD
steamcmd_url = os.environ.get("STEAMCMD_URL") 
#export STEAMCMD_URL="https://steamcdn-a.akamaihd.net/client/installer/steamcmd_linux.tar.gz"

# User and Password of a account with arma 3 purchased. Must have deacctivated Steam Guard
user=os.environ.get("STEAM_USER")
password=os.environ.get("STEAM_PASS")

# Path to where SteamCMD will be installed
steamcmd_path = str(os.environ.get("STEAM_PATH")) 

# Path to where the Arma 3 server will be installed
arma3_server_path = str(os.environ.get("STEAM_SERVER_PATH"))

mods_file_path = str(os.environ.get("MODS_FILE_PATH"))
# List of ids mods for installation
#export MODS="450814997","843425103","843577117","463939057","843593391","773131200","773125288","820924072","884966711","1858075458","751965892","333310405","735566597","583496184","583544987","1109528858"
#mod_ids = os.environ.get("MODS").split(",")
# Read the mod IDs from the file
with open(mods_file_path, "r") as f:
    mod_ids = f.read().splitlines()


# Download SteamCMD
print("Downloading SteamCMD...")
os.makedirs(steamcmd_path, exist_ok=True)
urllib.request.urlretrieve(steamcmd_url, steamcmd_path+"/steamcmd.tar.gz")

# Extract SteamCMD
print("Extracting SteamCMD...")
subprocess.run(["tar", "-xvzf", steamcmd_path+"/steamcmd.tar.gz", "-C", steamcmd_path])

# Install Arma 3 server
print("Installing Arma 3 server...")
os.makedirs(arma3_server_path, exist_ok=True)
subprocess.run([
    os.path.join(steamcmd_path, "steamcmd.sh"),
    "+login", user, password,
    "+force_install_dir", arma3_server_path,
    "+app_update", "233780", "validate",
    "+quit"
])

print("server Done!")



# Loop through the list of mod IDs and download each mod
for mod_id in mod_ids:
    print(f"Attempting to download mod {mod_id}...")

    # Loop until the mod is successfully downloaded or the maximum number of attempts is reached
    for i in range(max_attempts):
        print(f"attempt: {i}")
        # Use SteamCMD to download the mod
        result = subprocess.run([
            os.path.join(steamcmd_path, "steamcmd.sh"),
            "+login", "anonymous",
            "+force_install_dir", arma3_server_path,
            "+workshop_download_item", "107410", str(mod_id),
            "+quit"
        ], capture_output=True)
        # Check if the mod was successfully downloaded
        if b"Success" in result.stdout:
            print(f"Mod {mod_id} downloaded successfully!")
            break
        else:
            print(f"Mod {mod_id} download failed (attempt {i+1}/{max_attempts}). Retrying in {attempt_delay} seconds...")
            time.sleep(attempt_delay)
    else:
        print(f"Maximum number of attempts reached for mod {mod_id}. Mod download failed.")




