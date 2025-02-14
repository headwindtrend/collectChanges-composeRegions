# collectChangesCommand Sublime Text 3 Plugin

## Overview
The `collectChangesCommand` is a Sublime Text 3 plugin that allows users to collect all modifications made to a file and display them in a quick panel. This plugin serves as an improved alternative for reviewing and managing modifications, offering features such as multi-region selection and the ability to include or exclude arbitrary regions.

## Features
- Collect and display all modifications in a quick panel.
- Highlight and center on regions when hovered over in the quick panel.
- Include current selections and arbitrary regions into the collection.
- Easily exclude specific regions from the collection.
- Select or delete all collected modifications with clipboard commands.

## Installation
1. Copy the `collectChangesCommand` code into a new file named `collect_changes_or_compose_regions.py` in your Sublime Text `Packages/User` directory.
2. Restart Sublime Text 3 or reload the plugin by running `Preferences: Browse Packages` and navigating to the `User` directory, then opening the file in Sublime Text 3 and saving it.
3. Add these 2 lines into the key bindings.
	- `{ "keys": ["ctrl+shift+."], "command": "collect_changes" },`
	- `{ "keys": ["ctrl+shift+,"], "command": "collect_changes", "args": {"addArbitraryRegions": true} },`

## Usage and Operation
1. For collecting all the changes, `ctrl+shift+.`.
2. For adding arbitrary regions (current selection), `ctrl+shift+,`.
3. Rightclick any line on the quick panel to show that part of the file at the center of the view. Or, Up-arrow (`up`) / Down-arrow (`down`) on the quick panel for the same purpose.
4. Click (Leftclick) any line to Exit or Exclude. "Exit" will automatically select all the regions of the collection whereas "Exclude" will remove the region from the collection.
5. To cancel operation after the quick panel has shown, Esc (`escape`) (or click elsewhere (outside the quick panel)).
6. To select all the regions of the collection without showing the quick panel, copy this `select myCollection` text string (into the clipboard) before `ctrl+shift+,`.
7. To delete all the regions of the collection at once (without showing the quick panel), copy this `delete myCollection` text string (into the clipboard) before `ctrl+shift+,`.

## Contributing
Feel free to submit issues, fork the repository, and send pull requests. Contributions are welcome!

## License
The "default" License.
