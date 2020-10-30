import csv
import json
import os

LOCATION_DICT = {
    "前卫": "front",
    "中卫": "middle",
    "后卫": "behind"
}


def generate_characters_json():
    obj = {}
    with open("characters.csv", "r", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if i == 0:
                continue
            chara = {
                "location": LOCATION_DICT.get(row[4], None),
                "cn_exists": row[2] == "1",
                "range": int(row[3]) if row[3] != "未知" else None,
                "init_star": int(row[5]) if row[5] != "未知" else None,
                "cn_name": row[1],
                "jp_name": row[6],
                "tw_name": row[7],
                "nicknames": []
            }
            for j in range(8, len(row)):
                if row[j] != "":
                    chara["nicknames"].append(row[j])
            obj[int(row[0])] = chara
        f.close()
    with open("./release/characters.json", "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=4, ensure_ascii=False)
        f.close()
    with open("./release/characters.min.json", "w", encoding="utf-8") as f:
        json.dump(obj, f)
        f.close()


def generate_cast_json():
    obj = {}
    with open("cast.csv", "r", encoding="utf-8-sig") as f:
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
    with open("./release/cast.json", "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=4, ensure_ascii=False)
        f.close()
    with open("./release/cast.min.json", "w", encoding="utf-8") as f:
        json.dump(obj, f)
        f.close()

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
    with open("./release/names_regex.json", "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=4, ensure_ascii=False)
        f.close()
    with open("./release/names_regex.min.json", "w", encoding="utf-8") as f:
        json.dump(obj, f)
        f.close()

def main():
    if not os.path.exists('release'):
        os.makedirs('release')
    generate_characters_json()
    generate_cast_json()
    generate_names_regex_json()

if __name__ == "__main__":
    main()