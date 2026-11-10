"""Add a link at the first plain-text mention of each wiki page on every published page."""
import os, re, sys, json
V = sys.argv[1]
DRY = "--dry" in sys.argv
names = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"linknames.json")))
EXCLUDE = set("""Adventuring Alchemy Armor Attunement Background Backgrounds Bases Calendars Cantrips Classes Combat Condition
Conditions Crafting Crew Currency DOOM Equipment Facilities Familiars Festivals Gods Grandmother Heritage Heritages History
Holidays Home Injuries Imperatrix Languages Legends Leveling Lineage Lineages Luck Months Mounts Movement Multiclassing
Mysteries NPCs Overrun PG2 Party Personnel Pilfer Planes Potions Recap Regions Religion Reposition Rings Rituals Rules
Services Shove Spellcasting Spells Steeds Swimming Talent Talents Tattoos Tools Tumble Vehicles Weapons Weather Hod Bast
Cosmology Midgard""".split())
EXCLUDE |= {"Wormwood", "Keepers", "The North", "The Wall", "The Wastes", "The Plain", "Landing Page", "Player Characters", "Trade Fairs",
            "Free Cities", "Lady Luck", "Grand Duchy", "Green Duchy", "Great Library", "The Party", "Lord of Fire",
            "Magic Style", "Spell Point", "Ley Lines", "Shadow Roads", "Deep Void", "Near Void", "The Abyss",
            "Variant Rules", "House Rules", "Life and Death", "Between Adventures", "Labyrinth Options", "Wind Lords",
            "The Wind Lords", "Sky Stairs", "Great Gatherings", "Death Knights", "Recap", "The Concord", "The Keepers",
            "The Elders", "Elders", "The Dreamers", "The Infernals", "The Chantry", "Ghost Folk", "Ivy", "People", "The Sage", "Starless", "Ever River", "Status", "Places", "Primer", "Campaign Primer", "The Fingers", "Finger-Fortress", "Places We've Been"}
PAGE_EXCLUDE = {"Corremel": {"Keepers"}, "Nuria Natal": {"Corremel"}, "Random Names": {"Merrymead"}, "Valera": {"Loki"}, "Santerr Marossa": {"Lady of Light"}, "Legendary Places of the North": {"Vanguard"}, "Heritages": {"Goblin", "Old Ways"}, "Sarastra": {"Labyrinth"}, "Major Gods of the Southlands": {"Labyrinth"}, "Ptah": {"Labyrinth"}, "Spell Lists": {"Margreve", "Labyrinth", "Northlands"}, "Dread Expanded": {"Indefinite Dread"}}
SKIP_PAGES = {"Home", "Gods", "Cults", "The Planes", "Midgard", "Rules", "Cosmology"}
targets = {k: v for k, v in names.items() if k not in EXCLUDE and not k[0].islower() and len(k) >= 3}
# drop names that are just sentence starters / spell names collisions: require first char uppercase (done)
keys = sorted(targets, key=len, reverse=True)
pat = re.compile(r"(?<![\w\[|#/-])(" + "|".join(re.escape(k) for k in keys) + r")(?![\w\]-])(?!'s\w)")
NOLINK = ["Witch Tree", "Wormwood Forest", "Pale Witch", "Rogue's Court", "Court Sorcerer", "Goblin Court", "Collegium Elemental", "Misto Tilla", "Trickster's Road", "or just Keepers", "Keepers serve", "Emperor Loki", "Master of Shades", "The Hunter in Darkness", "Scribes, and Dreamers", "Keepers of the Tides", "Holy Keepers", "Witch lights", "Dominion Orb", "Bard's Chronology", "Cults and ancient powers", "Skadi's Sisters", "Skadi's Sons", "Skadi's Daughters", "Warlock's trumpetblossoms", "Labyrinth of Carreult", "Salzby Armorers", "Bloodsworn Oaths", "Moaning Monk", "Monk's Harbor", "Book of Ebon Tides", "Northlands Worldbook", "Labyrinth Worldbook", "Midgard Worldbook", "Tales of the Old Margreve", "Labyrinth Options", "Crossroads Souk", "Margreve Knights", "Harbingers of the Yawning Void", "Loki's Bridge", "making that choice: Fenris", "Naval Combat in Chapter 7", "Dead Druid's Run", "Tamasheq Climb", "Sun Witch", "Singing Warlock", "(optional, Northlands)", "Cults rise", "Silver Witch", "on the North Wind", "Goblin sharks"]
PROTECT = re.compile("|".join(re.escape(x) for x in NOLINK) + "|" + r"\*\*\*[^*\n]+\*\*\*|\*\*[^*\n]+\*\*|!?\[\[[^\]]*\]\]|\[[^\]]*\]\([^)]*\)|`[^`]*`|https?://\S+|<[^>]+>")
total = 0; per = {}; LOG = []
for dp, dn, fn in os.walk(V):
    rel = os.path.relpath(dp, V)
    dn[:] = [d for d in dn if not d.startswith(".")]
    if rel.startswith((".", "_GM Only", "z_templates", "Assets")) and rel != ".": continue
    for f in fn:
        if not f.endswith(".md"): continue
        page = f[:-3]
        if page in SKIP_PAGES: continue
        p = os.path.join(dp, f); s = open(p, encoding="utf-8").read()
        if re.search(r"^publish: false", s, re.M): continue
        m = re.match(r"^---\n.*?\n---\n", s, re.S)
        head, body = (s[:m.end()], s[m.end():]) if m else ("", s)
        linked = set()
        for l in re.findall(r"\[\[([^\]|#]+)", body):
            t = l.strip().rstrip("\\").split("/")[-1]; linked.add(names.get(t, t))
        out = []; incode = False; cnt = [0]
        for line in body.split("\n"):
            st = line.lstrip("> ").strip()
            if line.startswith("```"): incode = not incode
            if incode or re.match(r"^\s*(>\s*)*#", line) or st.startswith(("[!", "*This page includes", "*Material", "|---", "| ---", "*Optional, from")) or re.match(r"^\s*\|?\s*-{3}", st):
                out.append(line); continue
            intable = line.lstrip().startswith("|")
            # split into protected and free segments
            segs = []; last = 0
            for pm in PROTECT.finditer(line):
                segs.append((False, line[last:pm.start()])); segs.append((True, pm.group(0))); last = pm.end()
            segs.append((False, line[last:]))
            newline = ""
            for prot, text in segs:
                if prot: newline += text; continue
                def rep(mm):
                    name = mm.group(1); t = targets[name]
                    if t == page or t in linked or name in PAGE_EXCLUDE.get(page, ()): return name
                    linked.add(t); cnt[0] += 1; LOG.append((page, name, t))
                    if name == t: return f"[[{t}]]"
                    return f"[[{t}\\|{name}]]" if intable else f"[[{t}|{name}]]"
                newline += pat.sub(rep, text)
            out.append(newline)
        n = cnt[0]
        if n:
            per[os.path.join(rel, f)] = n; total += n
            if not DRY: open(p, "w", encoding="utf-8").write(head + "\n".join(out))
print("links added", total, "pages", len(per))
for k, v in sorted(per.items(), key=lambda x: -x[1])[:25]: print(v, k)
json.dump(LOG, open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"linklog.json"),"w"))
