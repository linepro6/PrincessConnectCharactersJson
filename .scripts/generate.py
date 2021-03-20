import csv
import json
import os

LOCATION_DICT = {
    "前卫": "front",
    "中卫": "middle",
    "后卫": "behind"
}

LOCATION_INDEX_DICT = {
    "front": 0,
    "middle": 1,
    "behind": 2
}

SPECIAL_CN_CHARAS = [ 1701, 1702 ]

def json_release(filename, obj):
    with open(os.path.join("./release", f"{filename}.json"), "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=4, ensure_ascii=False)
        f.close()
    with open(os.path.join("./release", f"{filename}.min.json"), "w", encoding="utf-8") as f:
        json.dump(obj, f)
        f.close()

def generate_characters_json():
    charas_dict = {}
    with open("characters.csv", "r", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if i == 0:
                continue
            if row[0] == '':
                continue
            chara = {
                "location": LOCATION_DICT.get(row[4], None),
                "cn_exists": row[2] == "1",
                "range": int(row[3]) if row[3] != "未知" else None,
                "init_star": int(row[5]) if row[5] != "未知" else None,
                "cn_name": row[1],
                "jp_name": row[6],
                "tw_name": row[7],
                "main_nickname": row[8],
                "nicknames": []
            }
            for j in range(9, len(row)):
                if row[j] != "":
                    chara["nicknames"].append(row[j])
            charas_dict[int(row[0])] = chara
        f.close()

    charas_special = {}
    with open("characters_special.csv", "r", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if i == 0:
                continue
            item = {
                "jp_max_star": 6 if row[2] == "1" else 5,
                "cn_max_star": 6 if row[3] == "1" else 5,
                "jp_weapon": row[4] == "1",
                "cn_weapon": row[5] == "1"
            }
            charas_special[int(row[0])] = item
            charas_dict[int(row[0])]['max_star'] = 6 if item["jp_max_star"] == 6 or item["cn_max_star"] == 6 else 5
        f.close()
    
    characters_cn = {}
    characters_jp = {}
    for chara_id, chara in charas_dict.items():
        chara_special = charas_special[chara_id]
        if chara["location"] is None:
            continue
        if chara_id not in SPECIAL_CN_CHARAS:
            characters_jp[chara_id] = {
                "name": chara["jp_name"],
                "location": LOCATION_INDEX_DICT[chara["location"]],
                "range": chara["range"],
                "init_star": chara["init_star"],
                "max_star": chara_special["jp_max_star"],
                "have_weapon": chara_special["jp_weapon"],
                "cn_name": chara["cn_name"],
                "tw_name": chara["tw_name"],
                "main_cn_nickname": chara["main_nickname"],
                "cn_nicknames": chara["nicknames"],
            }
        if chara["cn_exists"]:
            characters_cn[chara_id] = {
                "name": chara["cn_name"],
                "location": LOCATION_INDEX_DICT[chara["location"]],
                "range": chara["range"],
                "init_star": chara["init_star"],
                "max_star": chara_special["cn_max_star"],
                "have_weapon": chara_special["cn_weapon"],
                "jp_name": chara["jp_name"],
                "tw_name": chara["tw_name"],
                "main_nickname": chara["main_nickname"],
                "nicknames": chara["nicknames"],
            }
    json_release('characters', charas_dict)
    json_release("characters_cn", characters_cn)
    json_release("characters_jp", characters_jp)


def generate_cast_json():
    obj = {}
    with open("cv.csv", "r", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if i == 0:
                continue
            obj[int(row[0])] = {
                "cn_name": row[1],
                "cv_name": row[2],
                "cv_regex": row[3],
            }
        f.close()
    json_release('cv', obj)

def generate_names_regex_json():
    obj = {}
    with open("names_regex.csv", "r", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if i == 0 or row[0] == "":
                continue
            if row[4] == "":
                nicknames = []
                nicknames += row[1:4]
                for j in range(6, len(row)):
                    if row[j] != "":
                        nicknames.append(row[j])
                regex = "|".join(nicknames)
                loose_regex = regex
                strict_regex = regex
            else:
                loose_regex = row[4]
                strict_regex = row[5]
            obj[int(row[0])] = {
                'loose_regex': loose_regex,
                'strict_regex': strict_regex
            }
        f.close()
    json_release('names_regex', obj)

def main():
    if not os.path.exists('release'):
        os.makedirs('release')
    generate_characters_json()
    generate_cast_json()
    generate_names_regex_json()

if __name__ == "__main__":
    main()