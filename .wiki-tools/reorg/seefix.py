# Hand-resolved "(see Player's Guide)" notes that seelinks.py could not place. Each rule must hit the stated number of times.
import sys, os, re, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *
PGN = r" ?\*?\((?:see|See) (?:the )?\*?Player[’']s\*? ?\*?Guide\*?(?: and \*Player’s Guide 2\*)?(?: for [a-z ]+)?\.?\)"
R = [  # (file, regex, replacement, count)
 ('Rules/Book of Blades/More Weapon Options.md', r"special Ready action \(see \*\*Chapter 6\*\* of \*Player’s Guide\*\)", "special [[Encounter Gameplay#Ready|Ready]] action", 1),
 ('Rules/Classes/Paladin.md', r"your Divine Smite feature or the Radiant Strikes boon" + PGN, "your [[#Divine Smite|Divine Smite]] feature or the Radiant Strikes boon (see [[#Heroic Boon|Heroic Boon]])", 2),
 ('Rules/Classes/Rogue.md', r"charlatan tools" + PGN, "[[Tools#Charlatan Tools|charlatan tools]]", 1),
 ('Rules/Classes/Theurge.md', r"choose Scholar and Ritualist" + PGN, "choose [[Backgrounds#Scholar|Scholar]] and [[Magic Talents#Ritualist|Ritualist]]", 1),
 ('Rules/Classes/Theurge.md', r"the magic talents list" + PGN, "the [[Magic Talents|magic talents]] list", 1),
 ('Rules/Classes/Theurge.md', r" \(see full spell description in \*Player’s Guide\*\)", "", 1),
 ('Rules/Classes/Vanguard.md', r"choose Courtier and Mental Fortitude" + PGN, "choose [[Backgrounds#Courtier|Courtier]] and [[Magic Talents#Mental Fortitude|Mental Fortitude]]", 1),
 ('Rules/Classes/Vanguard.md', r"the martial talents list" + PGN, "the [[Martial Talents|martial talents]] list", 1),
 ('Rules/Classes/Warlock.md', r"the Echoes of Power boon" + PGN, "the Echoes of Power boon (see [[#Heroic Boon|Heroic Boon]])", 1),
 ('Rules/Classes/Witch.md', r"choose Adherent and Mental Fortitude" + PGN, "choose [[Backgrounds#Adherent|Adherent]] and [[Magic Talents#Mental Fortitude|Mental Fortitude]]", 1),
 ('Rules/Classes/Witch.md', r"the magic talents list" + PGN, "the [[Magic Talents|magic talents]] list", 1),
 ('Rules/Equipment/Vehicles.md', r"just like tool proficiency" + PGN, "just like [[Tools|tool proficiency]]", 1),
 ('Rules/Expanded or Variant Rules/Base Building.md', r"the \*raise dead\* spell \*\(see Player’s Guide\)\*?", "the *[[Rituals 4th–6th Circle#Raise Dead|raise dead]]* spell", 1),
 ('Rules/Expanded or Variant Rules/Rewards Expanded.md', r"Use the charms listed here \(see \*Player’s Guide\* for all listed spells\)", "Use the charms listed here", 1),
 ('Rules/Expanded or Variant Rules/Rewards Expanded.md', r"wish\]\]\* spell \*\(see Player’s Guide\)\*?", "wish]]* spell", 1),
 ('Rules/Lineages & Heritages/Heritages.md', r"the diaspora heritage" + PGN, "the [[#Diaspora Heritage|diaspora heritage]]", 1),
 ('Rules/Lineages & Heritages/Lineages.md', r"a Natural Adaption" + PGN, "a [[#Natural Adaptation|Natural Adaptation]]", 2),
 ('Rules/Lineages & Heritages/Lineages.md', r"Extreme Cold hazard" + PGN, "[[Encounter Gameplay#Extreme Cold|Extreme Cold]] hazard", 1),
 ('Rules/Magic Items/Fabled Magic Items.md', r"standard attunement rules" + PGN, "standard [[Using Magic Items#Attunement|attunement rules]]", 1),
 ('Rules/Magic Items/Fabled Magic Items.md', r"\*heroes’\*? ?\*?feast\* spell" + PGN, "*[[Rituals 4th–6th Circle#Heroes’ Feast|heroes’ feast]]* spell", 1),
 ('Rules/Magic Items/Fabled Magic Items.md', r"instead of one" + PGN, "instead of one", 1),
 ('Rules/Magic Items/Fabled Magic Items.md', r"as described in the spell" + PGN, "as described in the spell", 1),
 ('Rules/Magic Items/Magic Tattoos.md', r"\*clone, reincarnate, true resurrection,?\*?,? or similar magic" + PGN, "*[[Rituals 7th–9th Circle#Clone|clone]]*, *[[Rituals 4th–6th Circle#Reincarnate|reincarnate]]*, *[[Rituals 7th–9th Circle#True Resurrection|true resurrection]]*, or similar magic", 1),
 ('Rules/Spellcasting/Rituals/Rituals 4th–6th Circle.md', r"\*protection from evil and good\* spell" + PGN, "*[[1st-Circle Spells#Protection from Evil and Good|protection from evil and good]]* spell", 1),
 ('Rules/Spellcasting/Rituals/Rituals 7th–9th Circle.md', r"\*protection from evil and good\* spell" + PGN, "*[[1st-Circle Spells#Protection from Evil and Good|protection from evil and good]]* spell", 1),
 ('Rules/Spellcasting/Rituals/Rituals 7th–9th Circle.md', r"\*unseen servant\* ritual spell" + PGN, "*[[Rituals 1st–3rd Circle#Unseen Servant|unseen servant]]* ritual spell", 1),
 ('Rules/Trade Secrets/Running a Business.md', r"Group Check\]\] rules" + PGN, "Group Check]] rules", 1),
 ('Rules/Trade Secrets/Running a Business.md', r"can make group checks" + PGN, "can make [[Rolling the Dice#Group Checks|group checks]]", 1),
 ('Rules/Trade Secrets/Trade Goods & Money.md', r"special properties" + PGN, "special properties (see [[Weapons#Weapon Materials|Weapon Materials]] and [[Armor#Armor Materials|Armor Materials]])", 1),
]
bad = 0
for f, pat, rep, n in R:
    s = read(f); new, k = re.subn(pat, lambda m: rep, s)
    if k != n: print('MISS', f, pat[:50], k); bad += 1; continue
    if '--write' in sys.argv: open(os.path.join(V, f), 'w', encoding='utf-8').write(new)
print('rules', len(R), 'missed', bad)
