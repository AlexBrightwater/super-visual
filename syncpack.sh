#!/bin/bash
#

versions=("$@")

if [ ${#versions[@]} -eq 0 ]; then
	echo "No version given"
	exit 1
fi

function name() {
        ver=$(echo "$i" | sed 's/\.//g')
        name="301-$ver-dev3"
}

function sync() {
	for i in "${versions[@]}"; do
		name

		if [ ! -d manual-downloads/$i/essential ]; then
			mkdir manual-downloads/$i/essential
		fi

		cp -r /mnt/c/Users/Akorian/AppData/Roaming/PrismLauncher/instances/$name/.minecraft/config manual-downloads/$i/
		cp -r /mnt/c/Users/Akorian/AppData/Roaming/PrismLauncher/instances/$name/.minecraft/resourcepacks manual-downloads/$i/ 
		cp -r /mnt/c/Users/Akorian/AppData/Roaming/PrismLauncher/instances/$name/.minecraft/shaderpacks manual-downloads/$i/ 
		cp /mnt/c/Users/Akorian/AppData/Roaming/PrismLauncher/instances/$name/.minecraft/options.amecsapi.txt manual-downloads/$i/options.amecsapi.txt
		cp /mnt/c/Users/Akorian/AppData/Roaming/PrismLauncher/instances/$name/.minecraft/options.txt manual-downloads/$i/options.txt 
		cp /mnt/c/Users/Akorian/AppData/Roaming/PrismLauncher/instances/$name/.minecraft/essential/config.toml manual-downloads/$i/essential/config.toml
	done
}

sync
