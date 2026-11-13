# Stage 5: rebuild the index pages, retire the book hub pages, turn the "Heroes of..." pages into guides.
import sys, os, re, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *
from relink import retire
CC = split_footer(read('Rules/Equipment/Equipment.md'))[1]
SRCF = '---\n<small>Sources: [[Credits]].</small>'
def rep(rel, a, b, n=1):
    s = read(rel); assert s.count(a) == n, (rel, a[:60], s.count(a)); open(os.path.join(V, rel), 'w', encoding='utf-8').write(s.replace(a, b))
def gitmv(a, b): subprocess.run(['git', 'mv', a, b], cwd=V, check=True)
def gitrm(a): subprocess.run(['git', 'rm', '-qf', a], cwd=V, check=True)

# ---------------- guides (were "Heroes of ...")
def drop_callout(s): return re.sub(r'> \[!note\] Optional Content\n(?:>.*\n)+\n?', '', s)
hn = 'Rules/Heroes of the Northlands.md'; s = drop_callout(read(hn))
s = s.replace('aliases: [Northlands Options, Northlands Worldbook Options]', 'aliases: [Northlands Options, Northlands Rules, Northlands Campaign Rules]')
a = 'The 78 Northlands spells and rituals are mixed into the [[Spells]] and [[Rituals]] pages. The [[Spell Lists]] page marks them, under each source of magic.'; assert a in s
s = s.replace(a, 'The Northlands spells and rituals are in the [[Spells]] and [[Rituals]] lists with all the others, and on the [[Spell Lists]] under each source of magic.')
nr = read('Rules/Playing the Game/Renown & Fate/Northlands Rules.md'); tbl = re.search(r'\| Rules \| What They Cover \|\n(?:\|.*\n)+', nr).group(0).strip()
m = re.search(r'## Campaign Rules\n\n.*?\n', s, re.S); assert m
s = s[:m.start()] + '## Campaign Rules\n\nThese rules deepen the themes of a Northlands campaign.\n\n' + tbl + '\n' + s[m.end():]
open(os.path.join(V, hn), 'w', encoding='utf-8').write(s)
hm = 'Rules/Heroes of the Margreve.md'; s = drop_callout(read(hm))
s = s.replace('aliases: [Old Margreve Options, Tales of the Old Margreve Options]', 'aliases: [Old Margreve Options, Margreve Options]')
i = s.index('[[The Margreve]] Forest is home'); j = s.index('## Where to Find It')
intro = "[[The Margreve]] Forest is home to a variety of peoples, many of whom have been touched by the forest's magic in some way. Whether the creatures live in harmony with the ancient forest or barely scrape a living together, the forest changes its inhabitants over time. These options suit characters born, raised, or residing within the forest.\n\n"
assert s[i:j].startswith(intro[:150]); s = s[:i] + intro + s[j:]
s = s.replace('mixed into the [[Spells]] and [[Rituals]] pages; the [[Spell Lists]] flag them', 'in the [[Spells]] and [[Rituals]] lists with all the others').replace('mixed into the [[Magic Items]] pages', 'in the [[Magic Items]] lists')
open(os.path.join(V, hm), 'w', encoding='utf-8').write(s)
hl = 'Rules/Heroes of the Labyrinth.md'; s = drop_callout(read(hl))
s = s.replace('aliases: [Labyrinth Options, Labyrinth Worldbook Options]', 'aliases: [Labyrinth Options]')
for a, b in (('[[Dragonborn Lineage|Dragonborn (Labyrinth version)]]', '[[Dragonborn Lineage|Dragonborn]]'), ('[[Gearforged Lineage|Gearforged (Labyrinth version)]]', '[[Gearforged Lineage|Gearforged]]'),
             ('mixed into the [[Spells]] and [[Rituals]] pages; the [[Spell Lists]] flag them', 'in the [[Spells]] and [[Rituals]] lists with all the others'), ('mixed into the [[Magic Items]] pages, plus', 'in the [[Magic Items]] lists, plus'), ('six new vehicles on', 'six vehicles on')):
    assert a in s, a; s = s.replace(a, b)
open(os.path.join(V, hl), 'w', encoding='utf-8').write(s)
hh = 'Rules/Heroes of Horror.md'; s = drop_callout(read(hh))
s = s.replace('aliases: [Night Hunters Options, Horror Options, Building Backstories]', 'aliases: [Horror Options, Building Backstories, Horror Rules, Horror Campaign Rules]')
a = ' This page also holds the book\'s advice for buil'; i = s.index(a); j = s.index('\n', i); s = s[:i] + ' This page also holds advice for building a character with a horror backstory.' + s[j:]
hr = read('Rules/Playing the Game/Horror/Horror Rules.md'); tbl = re.search(r'\| Rules \| What They Cover \|\n(?:\|.*\n)+', hr).group(0).strip()
body_, ft = split_footer(s); s = body_.rstrip('\n') + '\n\n## Campaign Rules\n\nThese rules support horror campaigns.\n\n' + tbl + '\n\n' + ft + '\n'
open(os.path.join(V, hh), 'w', encoding='utf-8').write(s)
for f in ('Heroes of the Northlands', 'Heroes of the Margreve', 'Heroes of the Labyrinth', 'Heroes of Horror'): gitmv(f'Rules/{f}.md', f'Rules/Characters/{f}.md')

# ---------------- retire hub pages
n = 0
n += retire('Northlands Rules', 'Heroes of the Northlands', 'Campaign Rules', aliases=('Northlands Campaign Rules', 'Running Northlands Campaigns'))
n += retire('Horror Rules', 'Heroes of Horror', 'Campaign Rules', aliases=('Night Hunters Rules', 'Horror Campaign Rules'))
n += retire('Book of Blades', 'Rules', aliases=('Book of Blades Options',)); n += retire('Trade Secrets', 'Rules'); n += retire("Player's Guide 2", 'Rules', aliases=('PG2', "Player's Guide 2 Options"))
n += retire('Backgrounds & Talents', 'Rules', 'Make a Character'); n += retire('Lineages & Heritages', 'Lineages')
n += retire('Expanded or Variant Rules', 'Variant Rules')
for f in ('Playing the Game/Renown & Fate/Northlands Rules', 'Playing the Game/Horror/Horror Rules', 'Book of Blades', 'Trade Secrets', "Player's Guide 2", 'Characters/Backgrounds & Talents', 'Characters/Lineages & Heritages', 'Variant Rules/Expanded or Variant Rules'):
    gitrm(f'Rules/{f}.md')
print('links repointed', n)

# ---------------- index pages
write('Rules/Rules.md', '''---
publish: true
---
The rules of the game, arranged by what you are trying to do. Everything here is available at the table unless a page says otherwise.

## Make a Character
- [[Character Creation]] walks through the steps. [[Leveling Up]] and the [[Character Sheet]] come after.
- [[Classes]]: all sixteen classes. Every subclass is on its class page.
- [[Lineages]]: forty lineages, each on its own page with its variants.
- [[Heritages]] and [[Backgrounds]]
- [[Talents]]: [[Magic Talents]], [[Martial Talents]], [[Technical Talents]], and [[Battle Tactics]]
- [[Character Threads]], [[Character Themes]], and [[Heroic Endowments]]
- [[Random Names]] and the [[Reference Tables]] for beast forms, familiars, and steeds
- Guides to the options that fit a place or a kind of story: [[Heroes of the Margreve]], [[Heroes of the Northlands]], [[Heroes of the Labyrinth]], and [[Heroes of Horror]]

## Gear Up
- [[Equipment]]: [[Weapons]], [[Armor]], [[Adventuring Gear]], [[Tools]], [[Mounts & Services]], [[Vehicles]], and [[Currency & Trade]]
- [[Magic Items]]
- [[Crafting & Alchemy]]

## Use Magic
- [[Spellcasting]] and the [[Spell Lists]]
- [[Spells]] and [[Rituals]]
- [[Magic Styles]]
- [[Spell Points]], an optional way to cast for players who want it

## Play the Game
- [[Playing the Game]]: [[Rolling the Dice]], [[Adventuring]], [[Encounter Gameplay]], [[Life and Death]], [[Between Adventures]], [[Planes of Existence]], and [[Conditions]]
- Combat: [[Called Shot]], [[Injuries]], [[DOOM]], [[Parry and Defensive Combat]], [[Parting Shots]], [[Single Combat]], and [[Terrain Features]]
- Special melee attacks: [[Dirty Tactic]], [[Overrun]], [[Pilfer]], [[Reposition]], [[Shove]], and [[Tumble]]
- Downtime and rewards: [[Downtime Expanded]], [[Rewards Expanded]], [[Base Building]], and [[Monster Harvesting]]
- Trade and business: [[Shopping & Markets]], [[Running a Business]], [[Creating a Business]], [[Setting Up Shop]], and [[Trade Goods & Money]]
- Travel and weather: [[Weather]], [[Northlands Weather]], [[Waterborne Travel]], [[Swimming]], and [[Underwater Visibility]]
- Ships and the sea: [[Nautical Rules]], [[Ships and Sea Combat]], [[Naval Battles]], and [[Raiding]]
- Horror: [[Dread Expanded]], [[Shadow Tokens]], [[Curses, Diseases, and Hazards]], and [[Safety Tools]]
- Renown and fate: [[Reputation]], [[Flyting and Kennings]], and [[Prophecies and Omens]]

## At This Table
- [[House Rules]]
- [[Variant Rules]]: rules that are written up here but not in play
- [[Credits]]

''' + CC)
write('Rules/Variant Rules/Variant Rules.md', '''---
publish: true
---
Rules that are written up on the wiki but are not in play in this campaign.

- [[Epic Advancement]]: advancing past 20th level

''' + SRCF)
rep('Rules/Equipment/Equipment.md', 'Optional gear from *[[Rules|Book of Blades]]*: [[Clockwork Extensions]], [[Arcanepunk Items]], and [[Siege Engines]].',
    '- [[Clockwork Extensions]]\n- [[Siege Engines]]\n- [[Warframes]]\n\nSee also [[Magic Items]], [[Crafting & Alchemy]], and [[Trade Goods & Money]].')
rep('Rules/Magic/Magic Items/Magic Items.md', '- [[Fabled Magic Items]]\n', '- [[Fabled Magic Items]]\n- [[Arcanepunk Items]]\n- [[Weapons of Legacy]]\n')
rep('Rules/Playing the Game/Playing the Game.md', '- [[Between Adventures]]\n', '''- [[Between Adventures]]
- [[Conditions]]

## Combat
- [[Called Shot]] and [[Injuries]]
- [[DOOM]]
- [[Parry and Defensive Combat]]
- [[Parting Shots]]
- [[Single Combat]]
- [[Terrain Features]]
- Special melee attacks: [[Dirty Tactic]], [[Overrun]], [[Pilfer]], [[Reposition]], [[Shove]], [[Tumble]]

## Downtime & Rewards
- [[Downtime Expanded]]
- [[Rewards Expanded]]
- [[Base Building]]
- [[Monster Harvesting]]

## Trade & Business
- [[Shopping & Markets]]
- [[Running a Business]]
- [[Creating a Business]]
- [[Setting Up Shop]]
- [[Trade Goods & Money]]

## Travel & Weather
- [[Weather]]
- [[Northlands Weather]]
- [[Waterborne Travel]]
- [[Swimming]]
- [[Underwater Visibility]]

## Ships & Sea
- [[Nautical Rules]]
- [[Ships and Sea Combat]]
- [[Naval Battles]]
- [[Raiding]]

## Horror
- [[Dread Expanded]]
- [[Shadow Tokens]]
- [[Curses, Diseases, and Hazards]]
- [[Safety Tools]]

## Renown & Fate
- [[Reputation]]
- [[Flyting and Kennings]]
- [[Prophecies and Omens]]
''')
rep('Rules/Crafting & Alchemy/Crafting & Alchemy.md', '- [[Apothecary]]\n', '- [[Apothecary]]\n- [[Batch Crafting]]\n- [[Disenchanting]]\n')
s = read('Rules/Characters/Classes/Classes.md'); i = s.index('The Barbarian, Bard, Cleric, Druid, Ranger, Rogue, Sorcerer, Warlock, and Wizard pages also carry optional subclasses'); j = s.index('\n', i)
open(os.path.join(V, 'Rules/Characters/Classes/Classes.md'), 'w', encoding='utf-8').write(s[:i] + 'Every subclass is on its class page, in one alphabetical list.' + s[j:])
rep('Rules/Characters/Character Creation.md', '- [[Lineages|Lineages & Heritages]]\n- [[Rules#Make a Character|Backgrounds & Talents]]\n', '- [[Lineages]] and [[Heritages]]\n- [[Backgrounds]] and [[Talents]]\n')
rep('Home.md', '>> - [[Lineages|Lineages & Heritages]]', '>> - [[Lineages]] & [[Heritages]]')
# ---------------- small book mentions
rep('Rules/House Rules/Void Taint.md', '*From the Labyrinth Worldbook, in use in this campaign.*', '*In use in this campaign.*\n\n%% source: Labyrinth Worldbook %%')
rep('Rules/House Rules/Void Taint.md', '\n---\n*Void taint rules from the Labyrinth Worldbook by Kobold Press.*', '\n' + SRCF)
rep('Rules/Playing the Game/Horror/Curses, Diseases, and Hazards.md', 'aliases: [Curses, Diseases, and Hazards (Night Hunters), ', 'aliases: [')
rep('Rules/Playing the Game/Horror/Curses, Diseases, and Hazards.md', 'Despite the dark nature of *Night Hunters*,', 'Despite the dark nature of horror campaigns,')
rep('Rules/Playing the Game/Horror/Shadow Tokens.md', 'the dread villains of *Night Hunters* each', 'the dread villains each')
rep('Rules/Playing the Game/Ships & Sea/Ships and Sea Combat.md', 'These naval combat rules from the *Northlands Worldbook* are meant', 'These naval combat rules are meant')
rep('Rules/Playing the Game/Combat/Terrain Features.md', 'aliases: [Weather Effects (Book of Blades)]', 'aliases: [Weather Effects in Battle]')
rep('Rules/Playing the Game/Trade & Business/Trade Goods & Money.md', '(see *Labyrinth Worldbook* and [[The Labyrinth]])', '(see [[The Labyrinth]])')
rep('Rules/Equipment/Clockwork Extensions.md', 'for gearforged (see *Labyrinth Worldbook*)', 'for [[Gearforged Lineage|gearforged]]')
# ---------------- Recommended Magic Items: drop the book column
p = 'Rules/Magic/Magic Items/Recommended Magic Items by Class.md'; s = read(p)
a = '\n\nEach item notes the book it comes from. Items from the *Player’s Guide*, *Player’s Guide 2*, the *Labyrinth Worldbook*, and *Trade Secrets* are linked where the wiki has them.'; assert a in s; s = s.replace(a, '')
out = []; k = 0
for l in s.split('\n'):
    if l.startswith('|'):
        c = re.split(r'(?<!\\)\|', l)
        if len(c) == 7: del c[3]; l = '|'.join(c); k += 1
    out.append(l)
open(os.path.join(V, p), 'w', encoding='utf-8').write('\n'.join(out)); print('table rows trimmed', k)
