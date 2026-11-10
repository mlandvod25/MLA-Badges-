#!/usr/bin/env python3
"""
Restyle nuvio-badge-kit line.json with the kingsize "mono white" look.

Keeps line.json's groups, ids, names and regex patterns.
Swaps in kingsize's colors, tag style and black badge images.

Filters kingsize has no badge for use the custom badges in badge-images/custom/
(make_badges.py), which you host in your own GitHub repo.

Usage:  python3 kingsize_restyle.py line.json GITHUB_USER REPO [out.json]
"""
import json, os, sys

BASE = "https://raw.githubusercontent.com/kingsizew/badges/main/badge-images/"
REV = "?rev=b67572f"

CUSTOM_DIR = "badge-images/custom"   # folder of PNGs made by make_badges.py

# line.json id -> kingsize image path
IMG = {
    # special tags
    "hybrid": "special-tags/hybrid", "criterion": "special-tags/criterion",
    "proper": "special-tags/proper", "repack": "special-tags/repack",
    "remastered": "special-tags/remastered", "open-matte": "special-tags/open-matte",
    "directors-cut": "special-tags/directors-cut", "extended": "special-tags/extended",
    "uncensored": "special-tags/uncensored", "theatrical": "special-tags/theatrical",
    "bw": "special-tags/black-and-white",
    # resolution
    "4k": "resolution/4k", "1440p": "resolution/1440p", "1080p": "resolution/1080p",
    "720p": "resolution/720p", "576p": "resolution/576p", "480p": "resolution/480p",
    # hdr / visual
    "dolby-vision": "visual/dolby-vision", "hdr10plus": "visual/hdr10-plus",
    "hdr10": "visual/hdr10", "hdr": "visual/hdr", "hlg": "visual/hlg",
    "sdr": "visual/sdr", "10bit": "visual/10bit",
    # imax
    "imax-enhanced": "imax/imax-enhanced", "imax": "imax/imax",
    # audio
    "atmos": "audio/dolby-atmos", "dtsx": "audio/dts-x", "truehd": "audio/dolby-truehd",
    "dts-hd-ma": "audio/dts-hd-ma", "dts-hd": "audio/dts-hd", "flac": "audio/flac",
    "ddp": "audio/dolby-digital-plus", "dd": "audio/dolby-digital",
    "dts-es": "audio/dts-es", "dts": "audio/dts", "aac": "audio/aac", "opus": "audio/opus",
    # channels
    "7.1": "channels/7-1", "6.1": "channels/6-1", "5.1": "channels/5-1", "2.0": "channels/2-0",
    # source / quality
    "remux": "quality/remux", "bluray": "quality/bluray", "webdl": "quality/web-dl",
    "webrip": "quality/webrip", "hdrip": "quality/hdrip", "hdtv": "quality/hdtv",
    "dvdrip": "quality/dvdrip", "cam": "quality/cam", "telesync": "quality/ts",
    "telecine": "quality/tc", "screener": "quality/scr",
    # codec / encoder
    "av1": "encoder/av1", "hevc": "encoder/hevc", "avc": "encoder/avc", "xvid": "encoder/xvid",
    # streaming
    "netflix": "streaming/netflix", "amazon": "streaming/prime-video",
    "disney": "streaming/disney-plus", "appletv": "streaming/apple-tv-plus",
    "hbo": "streaming/hbo-max", "hulu": "streaming/hulu", "peacock": "streaming/peacock",
    "paramount": "streaming/paramount-plus", "crunchyroll": "streaming/crunchyroll",
}
# languages: id -> kingsize file stem
for lid in ("english japanese chinese russian arabic portuguese spanish french german "
            "italian korean hindi bengali punjabi marathi gujarati tamil telugu kannada "
            "malayalam thai vietnamese indonesian turkish hebrew persian ukrainian greek "
            "lithuanian latvian estonian polish czech slovak hungarian romanian bulgarian "
            "serbian croatian slovenian dutch danish finnish swedish norwegian malay latino").split():
    IMG[lid] = f"language/{lid}"
IMG["brazilian"] = "language/portuguese-brazil"

WHITE, BLACK = "#FFFFFF", "#000000"


def main(src, user, repo, dst):
    custom = {f[:-len("-black.png")] for f in os.listdir(CUSTOM_DIR) if f.endswith("-black.png")} \
        if os.path.isdir(CUSTOM_DIR) else set()
    own = f"https://raw.githubusercontent.com/{user}/{repo}/main/{CUSTOM_DIR}/"

    with open(src, encoding="utf-8") as f:
        data = json.load(f)

    for g in data["groups"]:
        c = BLACK if g["id"] == "language" else WHITE   # same as kingsize
        g["color"] = g["borderColor"] = c

    kings = mine = left = 0
    for flt in data["filters"]:
        flt.update(tagColor=WHITE, borderColor=WHITE, textColor=BLACK, tagStyle="filled")
        fid = flt["id"]
        if fid in IMG:
            suffix = "" if IMG[fid].startswith("language/") else REV
            flt["imageURL"] = f"{BASE}{IMG[fid]}-black.png{suffix}"
            kings += 1
        elif fid in custom:
            flt["imageURL"] = f"{own}{fid}-black.png"
            mine += 1
        else:
            flt.pop("imageURL", None)   # text fallback
            left += 1

    with open(dst, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"{len(data['filters'])} filters | {kings} kingsize | {mine} custom | {left} text-only")


if __name__ == "__main__":
    if len(sys.argv) < 4:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2], sys.argv[3],
         sys.argv[4] if len(sys.argv) > 4 else "line_kingsize_mono.json")
