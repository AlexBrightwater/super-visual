import requests
import argparse
import os
import sys

# ANSI color escape codes
RED = '\033[91m'
ENDC = '\033[0m'

BASE_URL = "https://api.modrinth.com/v2"

def fetch_versions(identifier, minecraft_version, item_type="mod"):
    if item_type == "mod":
        versions_url = f"{BASE_URL}/project/{identifier}/version?game_versions=[\"{minecraft_version}\"]"
    else:
        versions_url = f"{BASE_URL}/project/{identifier}/version?game_versions=[\"{minecraft_version}\"]"
    
    response = requests.get(versions_url)
    if response.status_code != 200:
        return None
    return response.json()

def filter_versions(versions, modloader_version, minecraft_version, item_type="mod"):
    if item_type == "mod":
        return [v for v in versions if modloader_version in v['loaders'] and minecraft_version in v['game_versions']]
    else:
        return [v for v in versions if minecraft_version in v['game_versions']]

def download_file(identifier, modloader_version, minecraft_version, download_folder, prefix, item_type="mod"):
    versions = fetch_versions(identifier, minecraft_version, item_type)
    if versions is None:
        return None

    filtered_versions = filter_versions(versions, modloader_version, minecraft_version, item_type)
    if not filtered_versions:
        return None

    download_url = filtered_versions[0]['files'][0]['url']
    response = requests.get(download_url)
    if response.status_code != 200:
        return None

    download_path = f'./downloads/{download_folder}'
    if not os.path.exists(download_path):
        os.makedirs(download_path)


    file_extension = ".jar" if item_type == "mod" else ".zip"
    with open(f"{download_path}/{prefix}{identifier}{file_extension}", "wb") as f:
        f.write(response.content)
    return f"Successfully downloaded {item_type}: {prefix}{identifier}{file_extension}"

def main():
    parser = argparse.ArgumentParser(description='Download mods and resource packs from Modrinth.')
    parser.add_argument('--loader', type=str, default='fabric', help='Mod loader (e.g., fabric, forge)')
    parser.add_argument('--mc_version', type=str, default='1.20.1', help='Minecraft version (e.g., 1.20.1)')
    parser.add_argument('--mod', type=str, help='Single mod to download')
    parser.add_argument('--modlist', type=str, help='File containing list of mods to download')
    parser.add_argument('--tex', type=str, help='Single Resourcepack to download')
    parser.add_argument('--texlist', type=str, help='File containing list of Resource Packs to download')
    parser.add_argument('--use_fabric', action='store_true', help='Use Fabric as fallback if mod download with initial loader fails')
    parser.add_argument('--name', type=str, help='Custom download directory name')
    args = parser.parse_args()

    download_folder = args.name or f"latest_{args.loader}_{args.mc_version}"

    identifiers = []
    item_type = ""
    if args.mod:
        identifiers.append(args.mod)
        item_type = "mod"
    elif args.modlist:
        try:
            with open(f"{args.modlist}", "r") as f:
                identifiers = f.readlines()
            item_type = "mod"
        except FileNotFoundError:
            error_message = f"Error: File {args.modlist} not found."
            print(f"{RED}{error_message}{ENDC}")
            sys.exit(1)
    elif args.tex:
        identifiers.append(args.tex)
        item_type = "tex"
    elif args.texlist:
        try:
            with open(f"{args.texlist}", "r") as f:
                identifiers = f.readlines()
            item_type = "tex"
        except FileNotFoundError:
            error_message = f"Error: File {args.texlist} not found."
            print(f"{RED}{error_message}{ENDC}")
            sys.exit(1)

    identifiers = [identifier.strip() for identifier in identifiers]
    failed_downloads = []

    for identifier in identifiers:
        if item_type == "mod":
            prefix = 'Q_' if args.loader == 'quilt' else 'F_'
        else: 
            prefix = ""
            
        result = download_file(identifier, args.loader, args.mc_version, download_folder, prefix, item_type)
        if result is None and args.use_fabric and item_type == "mod":
            prefix = 'F_'
            result = download_file(identifier, 'fabric', args.mc_version, download_folder, prefix, item_type)
        if result is None:
            error_message = f"Error: No compatible {item_type} version found for {identifier}."
            print(f"{RED}{error_message}{ENDC}")
            failed_downloads.append(error_message)
        else:
            print(result)

    if failed_downloads:
        with open(f"./downloads/{download_folder}.log", "w") as f:
            for entry in failed_downloads:
                f.write(f"{entry}\n")

if __name__ == "__main__":
    main()
