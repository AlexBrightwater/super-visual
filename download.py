import requests
import argparse
import os
import sys

def download_mod(mod_identifier, modloader_version, minecraft_version, download_folder):
    # Check if file already exists
    if os.path.exists(f"./downloads/{download_folder}/{mod_identifier}.jar"):
        return f"{mod_identifier}.jar already exists. Skipping download."

    # Base URL for Modrinth API
    base_url = "https://api.modrinth.com/v2"

    # Fetch mod versions
    versions_url = f"{base_url}/project/{mod_identifier}/version?facets=[['versions:{minecraft_version}'],['loader:{modloader_version}']]"
    response = requests.get(versions_url)
    if response.status_code != 200:
        return f"\033[91mError: Unable to fetch mod versions for {mod_identifier}. Status code: {response.status_code}\033[0m"

    versions = response.json()

    # Filter versions based on modloader and Minecraft version
    filtered_versions = [
        v for v in versions if modloader_version in v['loaders'] and minecraft_version in v['game_versions']
    ]

    if not filtered_versions:
        return f"\033[91mError: No compatible mod version found for {mod_identifier}.\033[0m"

    # Download the mod JAR file
    download_url = filtered_versions[0]['files'][0]['url']
    jar_response = requests.get(download_url)

    if jar_response.status_code != 200:
        return f"\033[91mError: Unable to download {mod_identifier}. Status code: {jar_response.status_code}\033[0m"

    # Create directory if it doesn't exist
    if not os.path.exists(f'./downloads/{download_folder}'):
        os.makedirs(f'./downloads/{download_folder}')

    # Save the JAR file
    with open(f"./downloads/{download_folder}/{mod_identifier}.jar", "wb") as f:
        f.write(jar_response.content)

    return f"Successfully downloaded {mod_identifier}.jar"

# Command-line argument parsing
parser = argparse.ArgumentParser(description='Download mods from Modrinth.')
parser.add_argument('--loader', type=str, default='fabric', help='Mod loader (e.g., fabric, forge)')
parser.add_argument('--mc_version', type=str, default='1.20.1', help='Minecraft version (e.g., 1.20.1)')
parser.add_argument('--modlist', type=str, default='mods.list', help='File containing list of mods to download')
args = parser.parse_args()

# Construct the download folder name
download_folder = f"latest_{args.loader}_{args.mc_version}"

# Read mod identifiers from specified file
try:
    with open(args.modlist, "r") as f:
        mod_identifiers = f.readlines()
except FileNotFoundError:
    print(f"\033[91mError: File {args.modlist} not found.\033[0m")
    sys.exit(1)

# Remove any leading or trailing whitespace from each mod identifier
mod_identifiers = [mod.strip() for mod in mod_identifiers]

# Initialize log for failed downloads
failed_downloads = []

# Download each mod
for mod_identifier in mod_identifiers:
    result = download_mod(mod_identifier, args.loader, args.mc_version, download_folder)
    print(result)

    if "Error" in result:
        failed_downloads.append(result)

# Write failed downloads to log
if failed_downloads:
    with open(f"./downloads/{download_folder}.log", "w") as f:
        for entry in failed_downloads:
            f.write(f"{entry}\n")

