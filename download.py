import requests
import argparse
import os
import sys

# Directory where mod lists are located
mod_list_directory = "mod-lists"

def download_mod(mod_identifier, modloader_version, minecraft_version, download_folder, mod_prefix):
    base_url = "https://api.modrinth.com/v2"

    versions_url = f"{base_url}/project/{mod_identifier}/version?facets=[['versions:{minecraft_version}'],['loader:{modloader_version}']]"
    response = requests.get(versions_url)

    if response.status_code != 200:
        return None

    versions = response.json()
    filtered_versions = [
        v for v in versions if modloader_version in v['loaders'] and minecraft_version in v['game_versions']
    ]

    if not filtered_versions:
        return None

    download_url = filtered_versions[0]['files'][0]['url']
    jar_response = requests.get(download_url)

    if jar_response.status_code != 200:
        return None

    if not os.path.exists(f'./downloads/{download_folder}'):
        os.makedirs(f'./downloads/{download_folder}')

    with open(f"./downloads/{download_folder}/{mod_prefix}{mod_identifier}.jar", "wb") as f:
        f.write(jar_response.content)

    if modloader_version == "quilt":
        return f"Successfully downloaded {modloader_version.upper()}" + "  mod: " + f"{mod_prefix}{mod_identifier}.jar"
    else:
        return f"Successfully downloaded {modloader_version.upper()} mod: {mod_prefix}{mod_identifier}.jar"

parser = argparse.ArgumentParser(description='Download mods from Modrinth.')
parser.add_argument('--loader', type=str, default='fabric', help='Mod loader (e.g., fabric, forge)')
parser.add_argument('--mc_version', type=str, default='1.20.1', help='Minecraft version (e.g., 1.20.1)')
parser.add_argument('--modlist', type=str, default='mods.list', help='File containing list of mods to download')
parser.add_argument('--use_fabric', action='store_true', help='Use Fabric as fallback if mod download with initial loader fails')
parser.add_argument('--name', type=str, help='Custom download directory name')
args = parser.parse_args()

if args.name:
    download_folder = args.name
else:
    download_folder = f"latest_{args.loader}_{args.mc_version}"

try:
    with open(f"{mod_list_directory}/{args.modlist}", "r") as f:
        mod_identifiers = f.readlines()
except FileNotFoundError:
    print(f"Error: File {mod_list_directory}/{args.modlist} not found.")
    sys.exit(1)

mod_identifiers = [mod.strip() for mod in mod_identifiers]
failed_downloads = []

# Check if basemods list file exists for the loader
basemods_file = f"{mod_list_directory}/{args.loader}-basemods.list"
if os.path.exists(basemods_file):
    with open(basemods_file, "r") as f:
        basemods_identifiers = f.readlines()
    basemods_identifiers = [mod.strip() for mod in basemods_identifiers]
    mod_identifiers.extend(basemods_identifiers)  # Add basemods to the list

for mod_identifier in mod_identifiers:
    mod_prefix = 'Q_' if args.loader == 'quilt' else 'F_'
    result = download_mod(mod_identifier, args.loader, args.mc_version, download_folder, mod_prefix)

    if result is None and args.use_fabric:
        mod_prefix = 'F_'
        result = download_mod(mod_identifier, 'fabric', args.mc_version, download_folder, mod_prefix)

    if result is None:
        error_message = f"Error: No compatible mod version found for {mod_identifier}."
        print(error_message)
        failed_downloads.append(error_message)
    else:
        print(result)

if failed_downloads:
    with open(f"./downloads/{download_folder}.log", "w") as f:
        for entry in failed_downloads:
            f.write(f"{entry}\n")

