#!/usr/bin/env python3
"""Render black-on-transparent text badges (kingsize mono style) for filters
that kingsize has no artwork for. Output: badge-images/custom/<id>-black.png"""
import os, sys
from PIL import Image, ImageDraw, ImageFont

# Matched to kingsize's theatrical-black.png: 175x80 canvas, Calibri-style bold,
# ~46px cap height, ~10px side padding. Carlito Bold is the metric-compatible Calibri.
FONT = "/usr/share/fonts/truetype/crosextra/Carlito-Bold.ttf"   # change if needed
H, SIZE, PAD, MAX_W, STROKE = 80, 69, 10, 380, 1   # STROKE thickens to match their heavier weight

LABELS = {
 # delivery
 "cached":"CACHED","uncached":"UNCACHED","realdebrid":"REAL-DEBRID","torbox":"TORBOX",
 "alldebrid":"ALLDEBRID","premiumize":"PREMIUMIZE","usenet":"USENET","p2p":"P2P",
 "direct":"DIRECT","bigfile":"50 GB+",
 # resolution / hdr / picture
 "8k":"8K","lowres":"LOW RES","dv-only":"DV ONLY","dv-p7":"DV P7","dv-p8":"DV P8",
 "fake-hdr":"FAKE HDR","12bit":"12BIT","8bit":"8BIT","3d":"3D","3d-hsbs":"3D HSBS",
 "3d-fsbs":"3D FSBS","3d-ou":"3D OU","3d-mvc":"3D MVC","anaglyph":"ANAGLYPH",
 "hfr":"HFR","upscaled":"UPSCALED",
 # audio / channels
 "dts-hd-hra":"DTS-HD HRA","lpcm":"LPCM","mp3":"MP3","1.0":"1.0",
 # source / codec
 "full-disc":"FULL DISC","uhd-bluray":"UHD BLU-RAY","dvd-remux":"DVD REMUX",
 "tvrip":"TVRIP","hardsub":"HARDSUB","vvc":"VVC","vp9":"VP9","vc1":"VC-1","mpeg2":"MPEG-2",
 # subtitles / edition / flags
 "esub":"ESUB","msubs":"MSUBS","sdh":"SDH","vostfr":"VOSTFR","forced":"FORCED",
 "unrated":"UNRATED","special":"SPECIAL","internal":"INTERNAL","limited":"LIMITED",
 "season-pack":"SEASON PACK","version":"V2 / BATCH","sample":"SAMPLE",
 # streaming services
 "jiohotstar":"JIOHOTSTAR","zee5":"ZEE5","sonyliv":"SONYLIV","sunnxt":"SUN NXT","aha":"AHA",
 "hoichoi":"HOICHOI","hidive":"HIDIVE","viki":"VIKI","iqiyi":"IQIYI","tving":"TVING",
 "iplayer":"IPLAYER","itvx":"ITVX","nowtv":"NOW","stan":"STAN","roku":"ROKU",
 "googleplay":"GOOGLE PLAY","crave":"CRAVE","cbc":"CBC","discovery":"DISCOVERY+",
 "shudder":"SHUDDER","mubi":"MUBI","starz":"STARZ","showtime":"SHOWTIME","amcplus":"AMC+",
 "mxplayer":"MX PLAYER","erosnow":"EROS NOW","hungama":"HUNGAMA","altbalaji":"ALTBALAJI",
 "viu":"VIU","wetv":"WETV","youku":"YOUKU","wavve":"WAVVE","unext":"U-NEXT","tver":"TVER",
 "coupang":"COUPANG","itunes":"ITUNES","movies-anywhere":"MOVIES ANYWHERE",
 # live tv
 "live":"LIVE","247":"24/7","ppv":"PPV","hd-feed":"HD","sd-feed":"SD","raw":"RAW",
 "live-hfr":"50/60 FPS","backup":"BACKUP","catchup":"CATCH-UP","region-in":"IN",
 "region-uk":"UK","region-us":"US","hls":"HLS","mpegts":"MPEG-TS",
 # containers
 "mkv":"MKV","mp4":"MP4","m2ts":"M2TS","avi":"AVI",
 # language tags
 "line-audio":"LINE AUDIO","dual":"DUAL","multi":"MULTI","original":"ORIGINAL","dubbed":"DUBBED",
}
for lid in ("urdu nepali sinhala cantonese filipino khmer lao burmese bosnian macedonian albanian "
            "icelandic catalan basque galician irish welsh belarusian kurdish pashto georgian "
            "armenian azerbaijani kazakh uzbek mongolian swahili amharic afrikaans yoruba hausa "
            "zulu odia assamese bhojpuri").split():
    LABELS[lid] = lid.upper()


def render(text, font):
    probe = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    l, t, r, b = probe.textbbox((0, 0), text, font=font, stroke_width=STROKE)
    if (r - l) + 2 * PAD > MAX_W:            # long labels: shrink to fit
        font = ImageFont.truetype(FONT, int(font.size * (MAX_W - 2 * PAD) / (r - l)))
        l, t, r, b = probe.textbbox((0, 0), text, font=font, stroke_width=STROKE)
    w = max(H, (r - l) + 2 * PAD)
    img = Image.new("RGBA", (w, H), (0, 0, 0, 0))
    ImageDraw.Draw(img).text(((w - (r - l)) / 2 - l, (H - (b - t)) / 2 - t),
                             text, font=font, fill=(0, 0, 0, 255), stroke_width=STROKE, stroke_fill=(0, 0, 0, 255))
    return img


def main(out="badge-images/custom"):
    os.makedirs(out, exist_ok=True)
    font = ImageFont.truetype(FONT, SIZE)
    for fid, text in LABELS.items():
        render(text, font).save(os.path.join(out, f"{fid}-black.png"))
    print(f"wrote {len(LABELS)} badges to {out}")


if __name__ == "__main__":
    main(*sys.argv[1:2])
