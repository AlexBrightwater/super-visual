# Super Visual Modpack

This repository is dedicated to the Super Visual Modpack for Minecraft, featuring a powerful script to automate the modpack creation process. It focuses on downloading mods and resource packs directly from Modrinth, streamlining the modpack assembly.

## download.py
An enhanced Python script for efficiently downloading Minecraft mods and resource packs from Modrinth.

### Key Features

- Download mods and resource packs by project_id or slug.
- Supports batch downloads through list files.
- Compatible with all modloaders.
- Error logging and download report.

### How to Use

#### Arguments:

- `--mc_version`: Specify the Minecraft version for the mods/resource packs. Default: `1.20.1`.
- `--loader`: Choose the mod loader (`fabric`, `forge`, `quilt`, or `neo-forge`). Default: `fabric`.
- `--mod`: Identifier for a single mod download.
- `--modlist`: File containing mod identifiers for batch download.
- `--tex`: Identifier for a single resource pack download.
- `--texlist`: File containing resource pack identifiers for batch download.
- `--name`: Custom name for the download directory. Default: `latest_<loader>_<mc_version>`

#### Usage Examples:

1. Download a single mod with Fabric:
```bash
python3 download.py --mod mod_identifier
```
2. Batch download mods with Quilt loader:
```bash
python3 download.py --loader quilt --modlist lists/mod_list_file.txt
```

3. Download resource packs to a custom directory:
```bash
python3 download.py --texlist lists/texture_pack_list_file.list --name custom_texture_folder
```

### Additional Notes:

Mods and resource packs are saved in `./downloads/{download_folder}`.  
File names for mods include a suffix based on the loader (e.g., mod_identifier_fabric.jar).  
Resource packs are saved with a .zip extension.  
Failed downloads are logged in `./downloads/{download_folder}.log`.  
List files should contain one identifier per line.  

# syncpack.sh
This is just a personal wrapper copying config files to make them available for the `buildpack.sh` script.

**⚠️ Warning:**  
Customize the script before usage.

## buildpack.sh

The buildpack.sh Bash script automates the process of building Super Visual. It includes functionalities for downloading mods using download.py, setting up mod directories, and copying local downloads to the Minecraft instances.
Customize before use.

### Key Features

- Automates mod downloads for specified Minecraft versions.
- Creates necessary directories if they don't exist.
- Copies downloaded and locally available mods, resource packs, and shaders to the respective Minecraft instance folders.

### How to Use

Run the script with the desired Minecraft versions as command-line arguments:

```bash
./buildpack.sh 1.19.4 
```
This script will handle downloading, directory setup, and file copying for each specified version.
Files/Folders in `./manual-downloads/<version>` must be present.  


**⚠️ Warning:**  
Customize the script before usage.