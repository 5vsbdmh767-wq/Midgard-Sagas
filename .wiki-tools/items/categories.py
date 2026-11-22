import re, sys, collections
RULES = [
 ('Scrolls', r'^spell scroll'),
 ('Mounts, Vehicles & Travel', r'horseshoe'),
 ('Dusts, Oils & Consumables', r'perfume|masking clay'),
 ('Containers & Vessels', r'drinking horn|searing safe'),
 ('Gems, Stones & Orbs', r'gem of image'),
 ('Tools, Keys & Curiosities', r'spyhole'),
 ('Boots & Footwear', r'boots|slippers|sandals|shoes|socks|anklet'),
 ('Banners', r'banner|standard|hawking sign'),
 ('Mounts, Vehicles & Travel', r'saddle|bridle|horseshoe|feedbag|blanket of the war|carpet|broom|sail\b|oars|caravan|apparatus of the (crab|avian)|quilted bridge|palisade|instant fortress|rower|vehicular|steed|harness|stirrup|yoke|wagon'),
 ('Instruments', r'bagpipe|drum|flute|horn\b|horn of|lyre|pipes|cymbal|talharpa|harp|kazoo|sitar|fiddle|\blute\b|chime|bell|megaphone|vielle|whistle|ocarina|gong|trumpet'),
 ('Books & Writing', r'book|grimoire|manual|tome|almanac|scroll|quill|parchment|deck|map|libram|codex|journal|ink'),
 ('Headwear & Eyewear', r'helm|hat\b|hat of|circlet|crown|headband|cowl|goggles|eyes of|glasses|mask|veil|diadem|halo|oculus|hood|hair pick|headrest|keffiyeh|earring|monocle|spectacle|lens'),
 ('Cloaks, Robes & Clothing', r'cloak|cape\b|cape of|robe|mantle|fur\b|kerchief|apron|garment|vest|coat|shawl|scarf|sandals|slippers|boots|shoes|socks|clothes|dress|gown|tunic|prayer mat|pillow'),
 ('Belts, Gloves & Bracers', r'belt|gloves|gauntlets|bracers|bracelet|arm ring|anklet|bandolier|buckle|sheath|scabbard|quiver'),
 ('Amulets, Charms & Jewelry', r'amulet|periapt|necklace|medallion|brooch|charm\b|charm of|pendant|talisman|locket|torc|ring\b|rings|stone of good luck|coin|bead\b|beads|comb'),
 ('Gems, Stones & Orbs', r'ioun|gem\b|gem of|pearl|lodestone|orb\b|crystal|stone\b|shard|egg|feather\b|bone\b|marble|sphere|jewel|geode|lens'),
 ('Containers & Vessels', r'bag\b|bag of|sack|haversack|flask|bottle|jug|decanter|pot\b|pot\'?s|goblet|mug|chalice|bowl|brazier|censer|thurible|bucket|safe\b|vault|chest|box\b|hole\b|pouch|vial|cup|teapot|hookah|kettle|cauldron|urn|jar'),
 ('Dusts, Oils & Consumables', r'dust|ointment|salve|token|coal|chalk|glue|solvent|salt\b|pigments|clay|sweat|incense|candle|powder|soap|wax|paint|perfume|seed|beans|pie|butter'),
]
def cat(n):
    l = n.lower()
    for c, p in RULES:
        if re.search(p, l): return c
    return 'Tools, Keys & Curiosities'
if __name__ == '__main__':
    names = [x.strip() for x in open(sys.argv[1]) if x.strip()]
    d = collections.defaultdict(list)
    for n in names: d[cat(n)].append(n)
    for c in sorted(d, key=lambda c: -len(d[c])): print(len(d[c]), c, '|', '; '.join(d[c]))
