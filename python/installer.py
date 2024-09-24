import requests
from bs4 import BeautifulSoup
import shutil


# Modify these as needed
class config:
    track_mod = "https://steamcommunity.com/sharedfiles/filedetails/?id=2434420628"
    track_name = "TZ.Walon Circuit.trackdata"
    game_id = 585420


class bcolors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END_C = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


mod_list = [
    "https://steamcommunity.com/sharedfiles/filedetails/?id=3335468946",
    config.track_mod
]

print("Before proceeding, please ensure you meet the prerequisites.\nYou will need to install the following mods from "
      "the Steam Workshop.")
print(bcolors.FAIL + "Failing to do so before proceeding will cause errors" + bcolors.END_C)

for x in range(len(mod_list)):
    print("•" + mod_list[x])

confirm_install = input("\nHave you installed these mods? (y/n) ")

if confirm_install == "y":
    print(bcolors.GREEN + "Continuing Installation" + bcolors.END_C)

    steam_url = input("\nPlease provide the link to your steam profile: ")
    profile_number = ''.join(c for c in steam_url if c.isdigit())

    print("Looking up profile id " + profile_number)

    url = "https://steamid.io/lookup/" + profile_number
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for bad status codes

    soup = BeautifulSoup(response.content, 'html.parser')
    steam_ids = soup.find_all('a', rel='nofollow')

    print("steamID: " + steam_ids[0].text)
    print("steamID3: " + steam_ids[1].text)

    steamID3 = steam_ids[1].text

    if steamID3 != "":
        print(bcolors.GREEN + "Found id! Continuing installation.\n" + bcolors.END_C)
        cleaned_id = ''.join(c for c in steamID3.split("[U:1:", 1)[1] if c.isdigit())
        print("Cleaning id: " + cleaned_id)

        mod_id = ''.join(c for c in config.track_mod.split("?id=", 1)[1] if c.isdigit())

        file_path = "C:\\Program Files (x86)\\Steam\\userdata\\" + cleaned_id + "\\" + str(config.game_id) \
                    + "\\remote\\Mods\\" + mod_id + "\\data_dynamic"
        print("Filepath: " + file_path)

        shutil.copy("install_files\\" + config.track_name, file_path)

        print(bcolors.GREEN + "Track file copied successfully.\n" + bcolors.END_C)

        print(bcolors.GREEN + "Current tracks installed: " + bcolors.END_C)
        f = open(file_path + "\\Save List.txt", "r")
        file_contents = f.read()
        print(file_contents)

        track_added = config.track_name in file_contents

        if track_added:
            print(bcolors.GREEN + "Track is already present in file list. Setup complete.\n" + bcolors.END_C)

        else:
            print("Track not detected. Adding track to list.")
            with open(file_path + "\\Save List.txt", "r") as file:
                lines = file.readlines()

            last = lines[-1]

            lines[-1] = lines[-1].replace("]", ",")
            lines.append("\n\"" + config.track_name + "\"]")

            with open(file_path + "\\Save List.txt", "w") as file:
                file.writelines(lines)
            print(bcolors.GREEN + "Track added to file list. Setup complete.\n" + bcolors.END_C)

else:
    print(bcolors.FAIL + "Aborting Process" + bcolors.END_C)
