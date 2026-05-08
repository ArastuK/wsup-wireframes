#!/usr/bin/env python3
"""Compile all 48 selected characters from the 5 enriched JSON files."""
import json

SELECTED = [
    # Round 1
    "char-RAPrkxKyfKAchBxx4YaTZ","char-iOo1xzDkorVtBWklhGYz7","char-WVHg8J6mHhOxGkKAGU10p",
    "char-O6Ax6TtMr9GCwOLgfP1XR","char-Z3TDjFPJ0WR4FAVwg34w3","char-fvuszhGivM9mrTGn1TFT0",
    "char-AHn4WsYrcqVMD5PL5eeaN","char-03mGydbs59nUPsp2jPC7G","char-Ix2xvgsk8sjIexKZq6FyO",
    "char-rcRwg52kTkJq6ppFUbSuz","char-ZHbl4JgEIJ3CEZknvmnAy","char-0n5YoV6pzsgMpcIgbmZDo",
    "char-CVhomuW77JTeA5q4Ebyth","char-UWPXuwjyoP04Lb9Trpe3N","char-52ksxLtXjPCsZI3aZfClB",
    # Round 2
    "char-Lu4bUyE6TjMC853ma2wvA","char-VoQgBYAJJWhy3OcNJLY04","char-ysH8PlTm4kpOBv1hCSHWx",
    "char-adDgFVx158h3fuyLyermj","char-qemBvSFFPn5erDniwFGd7","char-FCuR9W4LOmJI0SQFbbSd8",
    "char-gYOa9dGLovy8y254Cw4Cd","char-6KRuKIe0wyCzsPD0sFMZO","char-QqptNUndwwIxkIhvXS7UE",
    "char-caPKg0Z9BUffal3D4JLDR",
    # Round 3
    "char-IGKIOAEiuEqBCi8TeRiTp","char-2iFafhRgZbGhk3c3fafCo","char-5aC1gvMBSlewSickCBI9V",
    "char-fI3VKcGfUjlzVIco1ErMf",
    # Round 4
    "char-GufNAwsFwVN49AF5ppfnQ","char-WuldH2BpbnHtWMgC6GXy7","char-C96hxLSAsVxP9EMGCqMPK",
    "char-dEUzj7upaoO3aDNNxGW7G","char-GnHlBOeFPt50zNAVmTyMg","char-p2BZ4rTBEXfzRdOW0Wij4",
    # Round 5
    "char-os48HomGfgrzy5tbMKYyC","char-GuGIGhBAcIWxRa6T6DFFY","char-S6X6tIx6D59YoZ57qi7Jj",
    "char-vVproCMQMPrfBqmO5gq9c","char-uDHgAI1X8vgmeTs8JU5BX","char-3F8cu5WW3ZJt9JjQH4RI2",
    "char-wAWgkWJvOFMLzy5sbayYy","char-VwM3F17Adk5v3Kl3RalI9","char-qMiy7QhMhgXZ0pUShG3f6",
    "char-bIoVbxPMYCmx8TflRfVYQ","char-MvxkPR3SZ3aoxITaFU9eW","char-Wg9hDEASKC4yWzfpGY3Kf",
    "char-GmjoS4peyfWwISU9CVs4M",
]

# Aggregate from all enriched files
chars_by_id = {}
for path in ["/tmp/ftue_full.json","/tmp/ftue_more.json","/tmp/ftue_helpers.json",
             "/tmp/ftue_gaps.json","/tmp/ftue_photo.json"]:
    for c in json.load(open(path)):
        chars_by_id[c["id"]] = c

def archetype(c):
    """Derive a hook archetype + emoji + color theme based on tags/categories."""
    cats = set((c.get("categories") or []))
    tags = {t.lower() for t in (c.get("tags") or []) if isinstance(t, str)}
    name_l = (c.get("name") or "").lower()
    desc_l = ((c.get("description") or "") + " " + (c.get("background") or "")).lower()

    rules = [
        # (label, emoji, accent_hex, predicate)
        ("Royalty",     "👑", "#facc15", lambda: ("royalty" in tags or "royalverse" in tags or "prince" in name_l or "princess" in name_l)),
        ("Vampire",     "🩸", "#ef4444", lambda: ("vampire" in tags or "vampire" in cats)),
        ("Fantasy",     "🔮", "#a855f7", lambda: ("fantasy" in cats or tags & {"fantasy","magic","elf","demon","fairy","supernatural","wizard","dragon","mage"})),
        ("Sci-fi",      "🚀", "#3b82f6", lambda: (tags & {"android","robot","sci-fi","scifi","space"})),
        ("Therapist",   "🌿", "#10b981", lambda: ("therap" in desc_l or "psycholog" in desc_l or "dietitian" in desc_l or "counsel" in desc_l)),
        ("Mentor",      "📚", "#f59e0b", lambda: ("teacher" in cats or "mentor" in tags or "professor" in tags or "teacher" in tags)),
        ("Mafia",       "🕴️", "#1f2937", lambda: ("mafia" in cats or "boss" in tags)),
        ("Bully",       "😼", "#ec4899", lambda: ("bully" in cats or "bully" in tags)),
        ("Tsundere",    "💢", "#f472b6", lambda: ("tsundere" in tags or "enemies to lovers" in tags)),
        ("Rockstar",    "🎸", "#8b5cf6", lambda: ("celebrities" in cats or "musician" in tags or "rockband" in desc_l)),
        ("Roommate",    "🏠", "#06b6d4", lambda: ("roommate" in tags)),
        ("Athlete",     "🏆", "#06b6d4", lambda: ("athlete" in tags or "sports" in tags)),
        ("Supernatural","✨", "#a855f7", lambda: (tags & {"supernatural"})),
        ("Boyfriend",   "💕", "#f472b6", lambda: ("boyfriend" in cats or "boyfriend" in tags)),
        ("Girlfriend",  "💕", "#f472b6", lambda: ("girlfriend" in cats or "girlfriend" in tags)),
        ("Best friend", "☕", "#fb923c", lambda: ("best friend" in tags or "friend" in cats)),
        ("Romance",     "💕", "#f472b6", lambda: ("romantic" in cats)),
        ("Comedy",      "😄", "#fb923c", lambda: ("karen" in name_l)),
    ]
    for label, emoji, color, pred in rules:
        if pred(): return {"label": label, "emoji": emoji, "color": color}
    return {"label": "Character", "emoji": "💬", "color": "#6b7280"}

def hook_line(c):
    """First sentence of description, max ~120 chars."""
    desc = (c.get("description") or "").strip()
    if not desc: return c.get("tagline") or ""
    # Take first sentence
    import re
    m = re.match(r"^(.{20,160}?)([.!?](?:\s|$)|$)", desc.replace("\n", " "))
    if m: return m.group(1).strip() + (m.group(2).strip() or "")
    return desc[:140].strip() + ("…" if len(desc) > 140 else "")

out = []
for cid in SELECTED:
    c = chars_by_id.get(cid)
    if not c:
        print(f"MISSING: {cid}")
        continue
    arch = archetype(c)
    out.append({
        "id": cid,
        "name": (c.get("name") or "").strip(),
        "age": c.get("age"),
        "gender": c.get("gender"),
        "imageStyle": c.get("imageStyle"),
        "image": c.get("characterImageUrl"),
        "greeting": (c.get("greetingMsg") or "").strip()[:280],
        "hook": hook_line(c),
        "tags": (c.get("tags") or [])[:4],
        "categories": (c.get("categories") or [])[:2],
        "archetype": arch["label"],
        "archEmoji": arch["emoji"],
        "archColor": arch["color"],
    })

print(json.dumps(out, indent=2, ensure_ascii=False))
import sys
print(f"\nTotal: {len(out)}", file=sys.stderr)
from collections import Counter
print(f"Gender: {Counter(c['gender'] for c in out)}", file=sys.stderr)
print(f"Style: {Counter(c['imageStyle'] for c in out)}", file=sys.stderr)
print(f"Archetypes: {Counter(c['archetype'] for c in out)}", file=sys.stderr)
