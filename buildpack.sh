#!/bin/bash
#
# Always update line 8 and 9
#

# Define the base path for the PrismLauncher
basePath="/mnt/c/Users/Akorian/AppData/Roaming/PrismLauncher/instances"

versions=("$@")
supeVisualVersion="301"
devVersion="dev3"

function constructInstanceName() {
	local version=$1
	echo "$supeVisualVersion-$(echo "$version" | sed 's/\.//g')-$devVersion"
}

function setupDirectories() {
	local instanceName=$1
	local instancePath="$basePath/$instanceName"
	local dirs=("mods" "shaderpacks" "resourcepacks" "config")

	if [ ! -d "$instancePath" ]; then
		echo "Prism Instance not found ($instanceName)"
		exit 1
	fi

	for dir in "${dirs[@]}"; do
		mkdir -p "$instancePath/.minecraft/$dir"
	done
}

function downloadPacks() {
	for version in "${versions[@]}"; do
		local instanceName=$(constructInstanceName "$version")
		setupDirectories "$instanceName"
		echo "##############"
		echo "Downloading Pack $instanceName"
		echo "##############"
		python3 download.py --loader fabric --mc_version "$version" --modlist "lists/$instanceName" --name "$instanceName" 
	done
}

function copyDownloaded() {
	for version in "${versions[@]}"; do
		local instanceName=$(constructInstanceName "$version")
		setupDirectories "$instanceName"
		cp -r downloads/$instanceName/* "$basePath/$instanceName/.minecraft/mods/"
	done
}

function copyLocal() {
	for version in "${versions[@]}"; do
		local instanceName=$(constructInstanceName "$version")
		setupDirectories "$instanceName"
		local instancePath="$basePath/$instanceName/.minecraft"

		if [ ! -d $instancePath/essential ]; then
			mkdir -p $instancePath/essential
		fi
		cp manual-downloads/$version/essential/config.toml "$instancePath/essential/"

		cp -r manual-downloads/$version/mods/* "$instancePath/mods"
		cp -r manual-downloads/$version/shaderpacks "$instancePath"
		cp -r manual-downloads/$version/resourcepacks "$instancePath"
		cp -r manual-downloads/$version/config "$instancePath"
		cp manual-downloads/$version/*.txt "$instancePath"
	done
}

#downloadPacks
#copyDownloaded
copyLocal
