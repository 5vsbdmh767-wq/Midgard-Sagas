# Second pass: book mentions that are not "(see Player's Guide)" notes. Every rule must hit its stated count.
import sys, os, re, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *
E = re.escape
G = r"\*?Player[’']s Guide\*?"
R = [
 ('Rules/Reference Tables.md', E("(available to druids with the Shifter subclass described in *Player’s Guide)*"), "(available to druids with the [[Druid#Shifter|Shifter]] subclass)", 1),
 ('Rules/Trade Secrets/Running a Business.md', E("[[Mounts & Services#Services|Services]] in the *Player’s Guide* describes"), "[[Mounts & Services#Services|Services]] describes", 1),
 ('Rules/Trade Secrets/Running a Business.md', E("As explained in the *Player’s Guide*, the"), "As explained under [[Mounts & Services#Services|Services]], the", 1),
 ('Rules/Trade Secrets/Setting Up Shop.md', E("the **Tools** rules in **Chapter 5** of *Player’s Guide*"), "the [[Tools]] rules", 1),
 ('Rules/Trade Secrets/Trade Goods & Money.md', E("Tool sets have their own highly varying prices in the *Player’s Guide*."), "Tool sets have their own highly varying prices (see [[Tools]]).", 1),
 ('Rules/Magic Items/Wondrous Items A–L.md', E("See *Figurine of Wondrous Power* in **Chapter 5** of *Player’s Guide* for full information"), "See *[[#Figurine of Wondrous Power|Figurine of Wondrous Power]]* for full information", 1),
 ('Rules/Magic Items/Magic Item Pricing.md', E("The *Player’s Guide* provides basic guidance for the pricing of magic items"), "[[Using Magic Items#Buying and Selling Magic Items|Buying and Selling Magic Items]] provides basic guidance for the pricing of magic items", 1),
 ('Rules/Magic Items/Magic Item Pricing.md', E("simply use the basic guidelines in the *Player’s Guide*."), "simply use [[Using Magic Items#Pricing Consumable Magic Items|the basic guidelines]].", 1),
 ('Rules/Magic Items/Magic Item Pricing.md', E("winged boots]]* from the *Player’s Guide*."), "winged boots]]*.", 1),
 ('Rules/Magic Items/Magic Tattoos.md', E("pricing guidelines found in the *Player’s Guide*."), "pricing guidelines found under [[Using Magic Items]].", 1),
 ('Rules/Spellcasting/Spell Points.md', E("(see class progression tables in the *Player’s Guide* or **Chapter 1** of this book)"), "(see the progression table on each [[Classes|class]] page)", 1),
 ('Rules/Spellcasting/Spell Points.md', E("the Spell Blade fighter subclass in the *Player’s Guide or the Con Arcanist rogue subclass in* **Chapter 1** of this book*.*"), "the [[Fighter#Spell Blade|Spell Blade]] fighter subclass or the [[Rogue#Con Arcanist|Con Arcanist]] rogue subclass.", 1),
 ('Rules/Spellcasting/Magic Styles.md', E("This section lists spells from the *Player’s Guide* and new spells presented later in this book that work well"), "This section lists spells that work well", 1),
 ('Rules/Spellcasting/Rituals/Rituals 4th–6th Circle.md', E("see the **war wagon** in **Chapter 5** of the *Player’s Guide*."), "see the [[Vehicles#War Wagon|war wagon]].", 1),
 ('Rules/Spellcasting/Rituals/Rituals 7th–9th Circle.md', E("see the **galley** in **Chapter 5** of the *Player’s Guide*."), "see the [[Vehicles#Galley|galley]].", 1),
 ('Rules/Spellcasting/Rituals/Rituals 7th–9th Circle.md', E("cast the suggestion spell (see Player’s Guide, spell save DC equal to your own)"), "cast the *[[2nd-Circle Spells#Suggestion|suggestion]]* spell (spell save DC equal to your own)", 1),
 ('Rules/Lineages & Heritages/Lineages.md', E(" in the *Player’s Guide.*"), ".", 1),
 ('Rules/Backgrounds & Talents/Magic Talents.md', E("**Volatile Spell Effect** table in the Player’s Guide"), "[[Sorcerer#Volatile Magic|Volatile Spell Effect]] table", 1),
 ('Rules/Expanded or Variant Rules/Downtime Expanded.md', E("See the *Player’s Guide for the general downtime rules.*"), "See [[Between Adventures]] for the general downtime rules.", 1),
 ('Rules/Expanded or Variant Rules/Downtime Expanded.md', E("see carousing downtime activity in the Player’s Guide."), "see the [[Between Adventures#Carousing|carousing]] downtime activity.", 1),
 ('Rules/Expanded or Variant Rules/Rewards Expanded.md', E("(in addition to those presented in this chapter), see the *Player’s Guide*."), "(in addition to those presented in this chapter), see [[Between Adventures]].", 1),
 ('Rules/Expanded or Variant Rules/Base Building.md', E("See the *Game Master’s Guide and Player’s Guide* for the rules for downtime activities."), "See [[Between Adventures]] for the rules for downtime activities.", 1),
 ('Rules/Expanded or Variant Rules/Base Building.md', E("see **Between Adventures** in **Chapter 6** of the *Player’s Guide*."), "see [[Between Adventures]].", 1),
 ('Rules/Expanded or Variant Rules/Base Building.md', E("other vehicle repair restrictions specified in the *Player’s Guide.*"), "other [[Vehicles#Vehicle Repairs|vehicle repair]] restrictions.", 1),
 ('Rules/Expanded or Variant Rules/Base Building.md', E("(see attitude in either *Game Master’s Guide or Player’s Guide*)"), "(see [[Encounter Gameplay#Attitude|Attitude]])", 1),
 ('Rules/Expanded or Variant Rules/Base Building.md', E("Standard pricing for such items can be found in the *Player’s Guide*."), "Standard pricing for such items can be found under [[Equipment]].", 1),
 ('Rules/Expanded or Variant Rules/Base Building.md', E("like the crafting activity description in the Player’s Guide."), "like the [[Between Adventures#Crafting|crafting]] activity description.", 1),
 ('Rules/Expanded or Variant Rules/Base Building.md', E("see the **Magic Item** section of the *Player’s Guide.*"), "see [[Using Magic Items]].", 1),
 ('Rules/Expanded or Variant Rules/Base Building.md', E("command]]* spell (DC 15, see *Player’s Guide*)"), "command]]* spell (DC 15)", 1),
 ('Rules/Expanded or Variant Rules/Base Building.md', E("as per the tongues spell (see Player’s Guide ),"), "as per the *[[3rd-Circle Spells#Tongues\\|tongues]]* spell,", 1),
 ('Rules/Expanded or Variant Rules/Base Building.md', E("hallow]]* spell (see *Player’s Guide*, GM’s discretion)"), "hallow]]* spell (GM’s discretion)", 1),
 ('Rules/Expanded or Variant Rules/Base Building.md', E("(GM’s discretion, see Game Master’s Guide and Player’s Guide for more on poisons)"), "(GM’s discretion, see [[Life and Death#Poisons\\|Poisons]])", 1),
 ('Rules/Expanded or Variant Rules/Base Building.md', E("Magic item descriptions can be found in the *Player’s Guide*, and"), "Magic item descriptions can be found under [[Magic Items]], and", 1),
 ('Rules/Expanded or Variant Rules/Horror Rules/Safety Tools.md', E(" For more details on safety tools, see the *Player’s Guide*."), "", 1),
 ('Rules/Classes/Mechanist.md', E("See the Augment class feature in the *Player’s Guide* for"), "See the [[#Augment|Augment]] class feature for", 1),
 ('Rules/Classes/Mechanist.md', E("**Mechanist Progression** table in the *Player’s Guide*."), "**Mechanist Progression** table.", 1),
 ('Rules/Classes/Fighter.md', E("See the Martial Action class feature in the *Player’s Guide* for"), "See the [[#Martial Action|Martial Action]] class feature for", 1),
 ('Rules/Classes/Rogue.md', E("See **Spell Rules** in the *Player’s Guide* for"), "See [[Spellcasting]] for", 1),
 ('Rules/Classes/Rogue.md', E("See the Player's Guide for the general rules of spellcasting"), "See [[Spellcasting]] for the general rules of spellcasting", 1),
 ('Rules/Classes/Monk.md', E("(see **Chapter 7** in the *Player’s Guide*)"), "(see [[Spellcasting#Concentration|Concentration]])", 1),
 ('Rules/Classes/Druid.md', E("table found in the Player's Guide."), "table under [[#Wild Shape|Wild Shape]].", 1),
 ('Rules/Book of Blades/Terrain Features.md', E("*Player’s Guide* and *Game Master’s Guide* both contain sections on weather and weather-related hazards you can apply to a scene. To augment those existing rules, this section"), "The core rules cover [[Encounter Gameplay#Hazards|weather-related hazards]] you can apply to a scene. To augment those rules, this section", 1),
 ('Rules/Book of Blades/Martial Gear.md', E("See *Player’s Guide* for rules on suffocating."), "See [[Life and Death#Suffocating|Suffocating]].", 1),
 ('Rules/Book of Blades/Martial Gear.md', E("See *Player’s Guide* and *Game Master’s Guide* for a vehicle’s statistics."), "See [[Vehicles]] for a vehicle’s statistics.", 1),
 ('Rules/Book of Blades/Martial Arms.md', E("These armor options augment what can be found in *Player’s Guide*."), "These armor options add to the [[Armor]] list.", 1),
 ('Rules/Book of Blades/More Weapon Options.md', E("the **Weapons** table in **Chapter 5** of *Player’s Guide* in addition"), "the [[Weapons]] table in addition", 1),
 ('Rules/Book of Blades/Warframes.md', E("see the **Initiative** section in **Chapter 6** of *Player’s Guide*."), "see [[Encounter Gameplay#Initiative|Initiative]].", 1),
 ('Rules/Book of Blades/Naval Battles.md', E("The **Tales of the Valiant** *Player’s Guide* and *Game Master’s Guide* contain rules for vehicle movement and combat."), "The [[Vehicles]] page has the core rules for vehicle movement and combat.", 1),
 ('Rules/Book of Blades/Naval Battles.md', E("The **Typical Difficulty Class** table in **Chapter 6** of *Player’s Guide* has"), "The [[Rolling the Dice|Typical Difficulty Class]] table has", 1),
 ('Rules/Nautical Rules/Water Rules/Swimming.md', E("uses the forced march rules from the Player’s Guide."), "uses the forced march rules (see [[Adventuring]]).", 1),
]
SUB = re.compile(r"See the \*{0,2}(\w+) Subclass\*{0,2} (?:class )?feature in the \*Player’s Guide\* for how these spells work\.")
bad = 0; nsub = 0
for f in sorted({r[0] for r in R} | {'Rules/Classes/' + os.path.basename(p) for p in glob.glob(V + '/Rules/Classes/*.md')}):
    s = read(f); new = s
    for ff, pat, rep, n in R:
        if ff != f: continue
        new, k = re.subn(pat, lambda m: rep, new)
        if k != n: print('MISS', f, pat[:60], k); bad += 1
    def sb(m):
        global nsub; nsub += 1; return f'See the [[#{m.group(1)} Subclass|{m.group(1)} Subclass]] feature for how these spells work.'
    new = SUB.sub(sb, new)
    if new != s and '--write' in sys.argv: open(os.path.join(V, f), 'w', encoding='utf-8').write(new)
print('rules', len(R), 'missed', bad, 'subclass notes', nsub)
