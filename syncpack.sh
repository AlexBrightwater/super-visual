#!/bin/bash
#

versions=("$@")

if [ ${#versions[@]} -eq 0 ]; then
	echo "No version given"
	exit 1
fi

function name() {
        ver=$(echo "$i" | sed 's/\.//g')
        name="301-$ver-dev2"
}

function sync() {
	for i in "${versions[@]}"; do
		name
		cp -r /mnt/c/Users/Akorian/AppData/Roaming/PrismLauncher/instances/$name/.minecraft/config manual-downloads/$i/config
		cp /mnt/c/Users/Akorian/AppData/Roaming/PrismLauncher/instances/$name/.minecraft/options.amecsapi.txt manual-downloads/$i/options.amecsapi.txt
		cp /mnt/c/Users/Akorian/AppData/Roaming/PrismLauncher/instances/$name/.minecraft/options.txt manual-downloads/$i/options.txt
		cp /mnt/c/Users/Akorian/AppData/Roaming/PrismLauncher/instances/$name/.minecraft/essential/config.toml manual-downloads/$i/essential/config.toml
	done
}

sync
