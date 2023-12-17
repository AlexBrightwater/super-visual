#!/bin/bash
#
# ./download.py --loader fabric --mc_version 1.20.4 --modlist lists/301-1201-dev2 --name 301-1204-dev1
# cp -r downloads/301-1202-dev2/* /mnt/c/Users/Akorian/AppData/Roaming/PrismLauncher/instances/301-1202-dev2/.minecraft/mods/
# versions=("1.19.4" "1.20.1" "1.20.2" "1.20.3" "1.20.4")

versions=("$@")

function name() {
	ver=$(echo "$i" | sed 's/\.//g')
	name="301-$ver-dev3"
}

function check() {
	if [ ! -d "/mnt/c/Users/Akorian/AppData/Roaming/PrismLauncher/instances/$name/" ]; then
		echo "Prism Instance not found ($name)"
                exit 1
        fi

        if [ ! -d "/mnt/c/Users/Akorian/AppData/Roaming/PrismLauncher/instances/$name/.minecraft/mods" ]; then
        	mkdir -p "/mnt/c/Users/Akorian/AppData/Roaming/PrismLauncher/instances/$name/.minecraft/mods" && echo "Created mods dir for $name"
        fi
	
	if [ ! -d "/mnt/c/Users/Akorian/AppData/Roaming/PrismLauncher/instances/$name/.minecraft/mods" ]; then
		echo "The mods dir is not present"
	fi

	if [ ! -d "/mnt/c/Users/Akorian/AppData/Roaming/PrismLauncher/instances/$name/.minecraft/shaderpacks" ]; then
		echo "The shaderpacks dir is not present"
	fi

	if [ ! -d "/mnt/c/Users/Akorian/AppData/Roaming/PrismLauncher/instances/$name/.minecraft/resourcepacks" ]; then
		echo "The resourcepacks dir is not present"
	fi
}

function download() {
	for i in "${versions[@]}"; do
		name
		check
    		echo "##############"
    		echo "Downloading Pack $name"
    		echo "##############"
    		python3 download.py --loader fabric --mc_version "$i" --modlist "lists/$name" --name "$name" 
	done
}

function copy_downloaded() {
	for i in "${versions[@]}"; do
		name
		check
		cp -r downloads/$name/* /mnt/c/Users/Akorian/AppData/Roaming/PrismLauncher/instances/$name/.minecraft/mods/ 
	done
}

function copy_local() {
	for i in "${versions[@]}"; do
		name
		check

        cp -r manual-downloads/$i/mods/* /mnt/c/Users/Akorian/AppData/Roaming/PrismLauncher/instances/$name/.minecraft/mods
		cp -r manual-downloads/$i/shaderpacks /mnt/c/Users/Akorian/AppData/Roaming/PrismLauncher/instances/$name/.minecraft/shaderpacks
		cp -r manual-downloads/$i/resourcepacks /mnt/c/Users/Akorian/AppData/Roaming/PrismLauncher/instances/$name/.minecraft/resourcepacks
		cp -r manual-downloads/$i/config /mnt/c/Users/Akorian/AppData/Roaming/PrismLauncher/instances/$name/.minecraft/config
		cp manual-downloads/$i/*.txt /mnt/c/Users/Akorian/AppData/Roaming/PrismLauncher/instances/$name/.minecraft/
		cp manual-downloads/$i/essential/config.toml /mnt/c/Users/Akorian/AppData/Roaming/PrismLauncher/instances/$name/.minecraft/essential/config.toml
        done
}



download
copy_downloaded
copy_local
