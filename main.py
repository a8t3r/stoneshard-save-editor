#!/usr/bin/env python3
from pathlib import Path
from typing import Dict
import configparser
import hashlib
import json
import sys
import zlib


def load_config() -> Dict:
    config = {"character": {}, "inventory": {}, "filesystem": {}}

    parser = configparser.ConfigParser()
    parser.read("config.ini")

    for section in config.keys():
        for key, value in (parser[section] or {}).items():
            config[section][key] = value

    # If output file is not set don't clobber the input
    if "output_save_file_path" not in config["filesystem"]:
        config["filesystem"]["output_save_file_path"] = (
            config["filesystem"]["input_save_file_path"] + ".new"
        )
    elif config["filesystem"]["output_save_file_path"] == "overwrite":
        config["filesystem"]["output_save_file_path"] = config["filesystem"][
            "input_save_file_path"
        ]

    return config


def decompress_stoneshard_sav(sav_path: Path) -> Dict:
    if not sav_path.exists():
        print(f"Unable to find save file at {sav_path}")
        sys.exit(1)

    content = sav_path.open("rb").read()
    decompressed_content = zlib.decompress(content)
    decoded_content = decompressed_content[:-33].decode("utf8")

    return json.loads(decoded_content)


def generate_salt(sav_path: Path):
    dir_2 = sav_path.parent.name
    dir_1 = sav_path.parent.parent.name

    return f"stOne!characters_v1!{dir_1}!{dir_2}!shArd"


def compress_stoneshard_sav(content: Dict, sav_path: Path) -> Dict:
    salt = generate_salt(sav_path)
    serialized_content = json.dumps(content)
    checksum = (
        hashlib.md5((serialized_content + salt).encode("utf8"))
        .hexdigest()
        .encode("utf8")
    )
    compressed_content = zlib.compress(
        serialized_content.encode("utf8") + checksum + b"\x00"
    )

    with sav_path.open("wb") as output_file:
        output_file.write(compressed_content)

    print(f"Updated save file written to {sav_path}")

config_items = {
    "xp": "XP",
    "ability_points": "AP",
    "skill_points": "SP",
    "level": "LVL",
    "strength": "STR",
    "agility": "AGL",
    "perception": "PRC",
    "vitality": "Vitality",
    "will": "WIL"
}

default_skill_names = [
    "o_skill_butchering_ico",
    "o_skill_craft_ico",
    "o_pass_skill_Sudden_Attacks",
    "o_skill_trap_search_ico"
]

def mutate_character(save_content: Dict, character_config: Dict):
    character = save_content["characterDataMap"]
    skills_list = save_content["skillsDataMap"]["skillsAllDataList"]
    skills_panel = save_content["skillsDataMap"]["skillsPanelDataList"]

    for key, value in character_config.items():
        if key == "clear_skills" and value == "true":
            count = 0
            for i in range(0, len(skills_list), 5):
                if skills_list[i] not in default_skill_names and int(skills_list[i + 1]) == 1:
                    count += 1
                    skills_list[i + 1] = "0.0"
            character["SP"] = count
            for i in range(0, 4):
                skills_panel[i] = [ -4.0, -4.0, -4.0, -4.0, -4.0, -4.0, -4.0, -4.0, -4.0, -4.0 ]

        if key == "clear_abilities" and value == "true":
            count = 0
            abilities = ["STR", "AGL", "PRC", "Vitality", "WIL"]
            for ability in abilities:
                minimum = min(int(character[ability]), 10)
                count += int(character[ability]) - minimum
                character[ability] = minimum
            character["AP"] = count

        if key in config_items:
            character[config_items[key]] = int(value)

def mutate_inventory(save_content: Dict, inventory_config: Dict):
    inventory = save_content["inventoryDataList"]
    for key, value, *ignored in inventory:
        if "moneybag" in inventory_config and key == "o_inv_moneybag":
            value["Stack"] = int(inventory_config["moneybag"])


def main():
    config = load_config()

    path = Path(config["filesystem"]["input_save_file_path"]).expanduser()
    save_content = decompress_stoneshard_sav(path)

    mutate_character(save_content, config["character"])

    mutate_inventory(save_content, config["inventory"])

    path = Path(config["filesystem"]["output_save_file_path"]).expanduser()
    compress_stoneshard_sav(save_content, path)


if __name__ == "__main__":
    main()
