# Super Visual Modpack
This is the GitHub Repo for Super Visual, a Modrinth Modpack. This repo focuses on the automatisation part of the modpack creation, it also stores some static files that need a place to live :)

# downlaod.py
A simple script to download Minecraft mods and resource packs from Modrinth.

## Features

- Download individual mods or resource packs by project_id or slug.
- Batch download mods or resource packs using a list.
- Best used with Fabric or Quilt.
- Error logging for failed downloads.

## Usage

### Required Arguments:

- `--mc_version`: The Minecraft version for which you want to download the mod or resource pack. (Default is `1.20.1`)

### Optional Arguments:

- `--loader`: Choose the mod loader (either `fabric` or `forge`). Default is `fabric`.
- `--mod`: Specify the identifier of a single mod to download.
- `--modlist`: Specify a file containing a list of mod identifiers to download.
- `--tex`: Specify the identifier of a single resource pack to download.
- `--texlist`: Specify a file containing a list of resource pack identifiers to download.
- `--use_fabric`: Use this flag to fallback to Fabric if the mod download with the initial loader fails.
- `--name`: Custom name for the download directory.

### Example Commands:

1. Download a single mod for Fabric loader:
   ```
   python3 download.py --mod mod_identifier
   ```

2. Download mods from a list for Quilt loader and falling back to fabric if no quilt version is available:
   ```
   python3 download.py --loader quilt --modlist lists/mod_list_file.txt --use_fabric
   ```

3. Download resource packs from a list and use a custom download folder name:
   ```
   python3 download.py --texlist lists/texture_pack_list_file.list --name texture_collection
   ```

## Notes:

- Mods are saved with a prefix of `F_` for Fabric, `Q_` for Quilt.
- Resource packs do not have a prefix.
- The default download directory is `./downloads/latest_{loader}_{mc_version}`.
- A log file is created in the download directory for any failed downloads.
- Lists are one id/slug per line

