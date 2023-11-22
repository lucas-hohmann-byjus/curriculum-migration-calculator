# %%


cls = 62

for src, dst in MIGRATIONS_INTER["INT"]["BEG"]["1:1"]:
    if src >= cls:
        break

print(src, dst)

# %%
CURRICULUMS = {
    "BEG": {
        "1:1": [
            {"name": "SpriteLab", "start": 1, "end": 29},
            {"name": "AppLab_1", "start": 30, "end": 56},
            {"name": "GameLab", "start": 57, "end": 78},
            {"name": "AppLab_2", "start": 79, "end": 106},
            {"name": "Teachable_Machine", "start": 107, "end": 113},
            {"name": "Pictoblox", "start": 114, "end": 144},
        ]
    },
    "INT": {
        "1:1": [
            {"name": "SpriteLab", "start": 1, "end": 20},
            {"name": "AppLab_1", "start": 21, "end": 40},
            {"name": "GameLab", "start": 41, "end": 63},
            {"name": "AppLab_2", "start": 64, "end": 80},
            {"name": "Thunkable", "start": 81, "end": 144},
        ],
    },
    "ADV": {
        "1:1": [
            {"name": "AppLab_1", "start": 1, "end": 36},
            {"name": "GameLab", "start": 10, "end": 16},
            {"name": "AppInventor", "start": 22, "end": 48},
            {"name": "Web", "start": 49, "end": 92},
            {"name": "Firebase", "start": 93, "end": 99},
            {"name": "Teachable_Machine", "start": 100, "end": 112},
            {"name": "p5.js", "start": 113, "end": 144},
        ],
    },
    "PRO": {
        "1:1": [
            {"name": "GameLab", "start": 1, "end": 8},
            {"name": "p5.js", "start": 9, "end": 42},
            {"name": "Web", "start": 49, "end": 52},
            {"name": "ReactNative", "start": 53, "end": 96},
            {"name": "Python", "start": 97, "end": 144},
        ],
    },
}

cls = 65
src = {"curriculum": "INT", "subtype": "1:1"}
dst = {"curriculum": "BEG", "subtype": "1:1"}

src_platform = None
dst_cls = None

for platform in CURRICULUMS[src["curriculum"]][src["subtype"]]:
    if cls in range(platform["start"], platform["end"] + 1):
        src_platform = platform

for platform in CURRICULUMS[dst["curriculum"]][dst["subtype"]]:
    if platform["name"] == src_platform["name"]:
        dst_cls = platform["start"]

dst_cls
