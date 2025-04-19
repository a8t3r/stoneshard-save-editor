# stoneshard-save-editor  
  
A save file editor for the game Stone Shard. Tested against version beta 0.8.1.x.  
  
## How to run  
  
- Install [Python 3](https://www.python.org/downloads/)  
- Clone or download this repo  
- Edit `config.ini`  
- Run `python3 main.py`  
  
## Configuration  
  
Configuration takes place in `config.ini`.  
  
`filesystem.input_save_file_path`: the path of your input save file, uses [pathlib.Path](https://docs.python.org/3/library/pathlib.html), so it should handle both Windows and Unix paths    
`filesystem.input_save_file_path`: the path you want to save to, or `overwrite` which will overwrite the `input_save_file_path`, if this is not set then it defaults to the value of `input_save_file_path` with an extension of `.new`  

Available options under `character` section:  
`xp`: sets your experience points; integer  
`level`: sets your level; integer, max 30  
`ability_points`: sets your ability points; integer  
`skill_points`: sets your skill points; integer  
`strength`: sets your strength; integer, max 30  
Similarly for `agility`, `perception`, `vitality`, `will`

Additionally available options are:  
`clear_skills`: clears the list of learned skills, removes skill icons from skill panels and returns available points to use; boolean  
`clear_abilities`: reduces the values of all abilities to a threshold value `10` and returns available points to use; boolean
  
`inventory.moneybag`: sets how much cash you have in your money bag; integer, max ???, won't set if you do not have a money bag in your character's inventory  
  
## Disclaimers  

It has been tested: 
* on Windows 11, and ran the code from inside the WSL2 against saves from Stone Shard beta 0.8.1.x.
* on Linux (Ubuntu 24), Stone Shard beta 0.9.212
  
Make backups. If this eats your hard earned character that's on you.  
  
## Todo  
  
Allow setting more attributes. Maybe add a sub command to dump the deserialized state.  
