# Blender Manual Atlas Helper

## Overview
This is a Blender addon for Blender 2.79 (and 2.79a/2.79b) that will allow you to manually texture atlas your meshes more easily.
This technique is especially useful for game development, as it allows you to greatly reduce the amount of material slots that your meshes take up, resulting in better performance in most rendering pipelines.

## Installation
[Download the latest release zip from the Releases page.](https://github.com/HugoZink/BlenderManualAtlasHelper/releases) Go to your preferences, and under addons, click `Install from zip file...` and point it to the release zip. Enable the addon and save settings.

## Usage
Find the Manual Atlas Helper tab under the tool shelf. Select the mesh, and select how big the target texture is. Optionally, you can set the `Size Multiplier` to a different value.
`1.1` is the default, which means that the UV's will be scaled to 1.1x their "absolute" size. This is because texture baking can be a lossy process, and this setting ensures no quality is lost.