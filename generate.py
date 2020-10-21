import csv
import json

dicts = {
    "前卫": "front",
    "中卫": "middle",
    "后卫": "behind"
}

def main():
    global dicts
    obj = {}
    with open("characters_origin.csv", "r", encoding="utf-8-sig") as f_r:
        reader = csv.reader(f_r)
        for i, row in enumerate(reader):
            if i == 0: continue
            chara = {
                "location": dicts.get(row[4], None),
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
        f_r.close()
    with open("characters.json", "w", encoding="utf-8") as f_w:
        json.dump(obj, f_w, indent=4, ensure_ascii=False)
        f_w.close()

main()