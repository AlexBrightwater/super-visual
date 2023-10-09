# Super Visual Modpack
This is the GitHub Repo for Super Visual, a Modrinth Modpack. This repo focuses on the automatisation part of the modpack creation, it also stores some static files that need a place to live :)

# downlaod.py
This script downloads the latest versions of minecraft mods based off a few parameters.  

`--modlist:` Sets the file with your modlist (default: mods.list)  
`--loader:` Sets the loader for the mods (default: fabric)  
`--mc_version:` Sets the Minecraft Version for the mods you want to download (default: 1.20.1)  
`--use_fabric:` Use Fabric as a fallback if the mod isn't found for the specified loader. Only works when --loader is set to 'quilt'.  

## Exapmple Command
```bash
python3 download.py --loader fabric --mc_version 1.20.1 --modlist mods.list
python3 download.py --loader quilt --mc_version 1.18.2 --use_fabric

```

## Mod List file
The file is expected to be in a dir called mod-lists, but that can be changed through the var mod_list_directory at top of the script.
Just store one mod per line in this file without blank lines. Take the name from the URL of the mod's modrinth page or use it's project_id.
