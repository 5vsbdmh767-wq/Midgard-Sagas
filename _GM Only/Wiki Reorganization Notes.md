---
publish: false
---
## Wiki Reorganization Notes

Bryant's brief (13 Nov 2026): no organization by book, and no book references except somewhere small and out of the way. One rules and lore database that flows intuitively.

Rulings:
- Anything optional is allowed, so every "Optional" label goes.
- Duplicate versions: obvious variants become named variants; near-identical ones get flagged.
- Injuries are in (tied to called shots). DOOM is in. Spell points are optional. Epic advancement is an alternate rule, not in play. Ship combat and weather systems need reconciling later.
- The "Heroes of…" pages become region guides.
- Hidden source notes are fine.

The state before the reorganization is commit `d9014ef` on GitHub.

### Stage 1: labels and credits (done)

- 1,299 "Optional, from …" lines replaced with invisible source notes (`%% source: … %%`). They don't show on the site.
- 712 "(optional, …)" tags removed, almost all from the spell lists.
- 132 page footers replaced with one small line: the Black Flag license note where it applies, otherwise "Sources: Credits".
- New `Credits` page at the top level: the license statement and the list of books.
- The "ask your GM" boxes on Theurge, Vanguard, and Witch are removed.
- Sentences that explained the labels (Spell Lists, Spells) are removed. Two "Optional, from Trade Secrets:" pointers (Between Adventures, Currency & Trade) are reworded without the label.
- Western Wastes: the label on the wild magic rule is now a hidden note.

Still to come: the book hub pages and the Rules index still talk about books until Stage 5 rebuilds them.

### Stage 2, part 1: one list per kind of thing (done)

Every page below used to have a core section followed by "More X (Book)" sections. Each is now one list or table. Nothing was removed except the items listed under "Removed".

- Weapons: one table of 84 weapons in four categories, one alphabetical list each for descriptions, properties, options, and materials.
- Adventuring Gear: one table by kind of gear, one set of descriptions, 21 equipment packs together.
- Armor: one table (light, medium, heavy, shields), one list each for descriptions, properties, and materials.
- Tools: each tool has one section. The extra goods, concoctions, and tasks sit under the tool they belong to, and each tool has one Example Tasks table. "Big Projects" is its own section. The price table moved to the top.
- Mounts & Services: one Mounts table (common, unusual, northern). The "Magical Mounts" note moved here from the Tools page, where it had been misfiled.
- Vehicles: one price table (air, land, water), every vehicle in one alphabetical run, and a short "Vehicles by Region" section for the Labyrinth and the Northlands.
- Backgrounds: all 52 in one alphabetical run, with a new index table (skills and where each fits).
- Heritages: all 64 in one alphabetical run, one language section, one "Common Heritages by Lineage" table covering 39 lineages, and a new index table.
- All 16 class pages: every subclass in one alphabetical run with a small index table. Added boons are folded into the Heroic Boon and Epic Boon lists, added metamagic into Metamagic, and all 22 added invocations into Eldritch Invocations.
- Fabled Magic Items: 38 entries in one alphabetical run, with the attunement rules first.

Mine (my wording or my judgement, not from a book):
- The "Suits" columns in the Backgrounds, Heritages, and subclass tables. They are drawn from which region or theme each option was written for.
- The "Often chosen by" column on the Heritages table is the lineage table turned around.
- Armor: the Northlands armors listed Strength and Stealth in separate columns; I converted them to the Cumbersome and Noisy properties the core table uses.
- Vehicles: the five longships are on the price table with no price, because the book gives none.
- Mounts: northern mounts have no speed in the book, so that cell is a dash. I restored one missing word ("At the GM's discretion") where a sentence was broken across a page.
- Bloodhound has two different spells with one name. The forest version is now "Bloodhound (Margreve)".
- Heritages: Hiveheim and Moonlit each appeared twice with identical traits and different descriptions. Each is now one entry, with the second description in a note named for the place (Björnrike, the Moonlit Glades).

Fixed while merging (conversion damage, checked against the Player's Guide):
- Tools: the Clothier, Construction, Gaming Set, and Herbalist example task tables were scrambled together. Task rows broken across two lines are rejoined.
- Backgrounds: the Wanderer's motivation table was sitting in the wrong section, twice.
- Mounts: the core Mounts table was sitting under Services.

Removed:
- Introductions that only said "these come from Book X" or listed the names that followed (many were my own sentences).
- Player's Guide 2 and Labyrinth both restate Vehicle Proficiency and Vehicle Resilience in nearly the same words. One copy is kept.
- The "Source" column on the Labyrinth vehicle table, and the book column on the unusual mounts table. Both are kept as hidden notes.

Flags for Bryant:
- Bladed Wings appears twice (4th circle). The two are nearly word for word; the second leaves out that the wings are magical weapons. Both are still on the page as "Bladed Wings" and "Bladed Wings (Labyrinth)".
- Judicial Champion (background) grants "Sense Motive", which is not a Tales of the Valiant skill. Probably Insight. Left as printed.
- Visionary (background) lists four skills with no "choose two". Left as printed.
- The armor "Gunpowder" property is still undefined.
- Text still says "see the Player's Guide" in many places inside rules. Not touched yet.

Still to come in Stage 2: the Book of Blades equipment pages (Martial Arms, More Weapon Options, Martial Gear, Martial Magic Items) have not been merged into these lists yet.

### Rulings applied, 13 Nov 2026 (second round)

- Bladed Wings: the Labyrinth copy is removed; the fuller version stays. Rule for the future: when two versions are essentially the same, keep the one from the more recently published book.
- Judicial Champion: "Sense Motive" changed to Insight.
- Visionary: "Choose two from" added. It has nothing else in place of the choice.
- "See the Player's Guide" notes are replaced with links to the wiki's own pages. About 320 notes across 57 pages: class features link to their heading on the class page, spells and rituals to their entries, downtime activities to Between Adventures, and so on. Where the thing was already linked, the note is simply removed.
- Magic Item Pricing: "Player's Guide 2 Items by Rarity" is now "Items by Rarity"; the footnote that sorted potions by book is gone.

Not changed:
- Mentions of the *Monster Vault* and *Game Master's Guide* (about 45). Those books are not on the wiki, so there is nothing to link to. They tell a player where a stat block or GM rule lives.
- Recommended Magic Items by Class still has a column naming each item's book. To be handled in Stage 5.
- The Lineages page keeps its book sections until Stage 4 splits it.

### Stage 2, part 2: Book of Blades equipment merged (done)

Four pages are gone because everything on them now lives in the main lists: Martial Arms, More Weapon Options, Martial Gear, Martial Magic Items.

- Weapons: 12 weapons added to the table and descriptions (butterfly sword, hook sword, ji, lasso, nunchaku, rope dart, sai, shuriken, tonfa, umbrella, and two renamed below). Two properties (Hooked, Shielding) and 9 weapon options added. New section "Magic Weapon Options" (9 options that need a magic weapon).
- Armor: lantern shield and a second spiked shield under Shields; dragonscale and winged armor under a new "Special Armor" group.
- Adventuring Gear: ether, garrote, smokeball.
- Mounts & Services: 14 pieces of mount gear in the one table, plus a line linking the 13 magic items for mounts.
- Magic items: 19 items placed alphabetically in Magic Armor, Magic Weapons, and the two Wondrous Items pages. 11 fabled items added to Fabled Magic Items, each with its story and its rules joined into one entry.
- Rogue: new "Rogue Tricks" section before the subclasses.
- A GM advice box ("Challenges for the Well-Equipped Adventurer") moved to `_GM Only/Book of Blades GM Notes`.

Mine (names I chose because two different things shared a name):
- "Boomerang, rebounding" (5 sp, range 20/60, bounces back) beside the existing Boomerang (1 gp, range 60/120).
- "Scythe, war" (1 sp, 1d12) beside the existing Scythe (20 gp, 2d4).
- "Spiked shield, large" (100 gp, +2, usable as a weapon) beside the existing Spike shield (10 gp, +1).

Fixed: two weapon descriptions (butterfly sword, sai) had table fragments in the middle of a sentence. Two fabled items had lost the first word of their story.

Flags for Bryant:
- Dragonscale armor (Special Armor) and Dragonhide (Armor Materials) are two takes on armor made from a dragon. Different prices and slightly different rules. Both kept.
- Scythe, war costs 1 sp for 1d12 damage, as printed. That looks like a misprint in the book.

### Stage 3: pages moved onto topic shelves (done)

The Rules section now has these shelves. No page was renamed, so no links changed.

- Characters: character creation, leveling, backgrounds, heritages, lineages, character themes, heroic endowments, the beast form and familiar tables. Inside it: Classes, and Talents (including Battle Tactics).
- Equipment: as before, plus siege engines, warframes, clockwork extensions.
- Crafting & Alchemy: as before, plus batch crafting and disenchanting.
- Magic: spellcasting, spell lists, magic styles, spell points, Spells, Rituals, and Magic Items (which now also holds arcanepunk items and weapons of legacy).
- Playing the Game: the core chapters and Conditions, plus six groups:
  - Combat: called shots, injuries, DOOM, the six special melee attacks, parry, parting shots, single combat, terrain features.
  - Downtime & Rewards: downtime, rewards, base building, monster harvesting.
  - Trade & Business: shopping, running and creating a business, setting up shop, trade goods and money.
  - Travel & Weather: weather, Northlands weather, waterborne travel, swimming, underwater visibility.
  - Ships & Sea: Bryant's ship combat pages, the Northlands sea combat page, naval battles, raiding.
  - Horror: dread, shadow tokens, curses and diseases, safety tools.
  - Renown & Fate: reputation, flyting, prophecies and omens.
- House Rules: unchanged.
- Variant Rules: epic advancement (not in play).

Gone: the folders Book of Blades, Trade Secrets, Expanded or Variant Rules, Nautical Rules, Backgrounds & Talents, Lineages & Heritages, Character Creation, Spellcasting.

Class option pages folded into class pages (Stage 2 follow-up):
- Fighter: all extra martial actions are in the one Martial Action list (13 actions).
- Mechanist: all extra augment effects are in the one Augment Effects list.
- Monk: Technique Forms is a section on the Monk page.
- Ranger: Tracking in Combat and Booby Traps are sections on the Ranger page.

Removed: the "Luck" page under variant rules. It was a word-for-word copy of the Luck rule in Rolling the Dice. The one link to it now goes there.

Still to reconcile (Bryant's call, later): three ship combat systems sit side by side in Ships & Sea, and three weather systems in Travel & Weather and Combat (Terrain Features).

### Stage 4: one page per lineage (done)

The single Lineages page (2,100 lines, nine book sections) is now an index plus 40 lineage pages in `Rules/Characters/Lineages/`. Each page is named "X Lineage" (for example "Dwarf Lineage") so it does not collide with the people pages ("Dwarves").

- Each lineage page has the base lineage first, then any regional versions, then variants in alphabetical order, then extra Natural Adaptation options.
- Each page links to its people page ("For who they are in Midgard, see…") and lists its common heritages. Eight people pages that had no link to the rules now have a "See also" line.
- The Lineages page keeps "Elements of a Lineage", the rule on choosing a variant, and a table of all 40 lineages with their variants.
- 79 links across the wiki were repointed to the new pages.

Named versions (same lineage, clearly different rules, named for the place):
- Northlands Bearfolk, Northlands Trollkin, Midgard Dhampir, Midgard Goblin.

Merged as near-identical (one entry; the other book's description kept in a note named for the place):
- Bearfolk (forest and Midgard versions have the same traits).
- Dragonborn and Gearforged (the Labyrinth versions have the same traits, reworded).

Flags for Bryant:
- Syderean has "spellborn" twice: once in "More Natural Adaptations" and once as "Natural Adaptation: Spellborn (Labyrinth)". Both kept.
- Five people pages (Alseid, Bearfolk, Erina, Gearforged, Piney) carry their own copy of the lineage traits. Left alone; the rules pages are now the place for traits.

### Stage 5: index pages, guides, last book mentions (done)

- `Rules` is rebuilt as one index in five parts: Make a Character, Gear Up, Use Magic, Play the Game, At This Table.
- Removed hub pages: Book of Blades, Trade Secrets, Player's Guide 2, Horror Rules, Northlands Rules, Backgrounds & Talents, Lineages & Heritages, Expanded or Variant Rules. Links to them now go to the right place.
- New `Variant Rules` page (rules not in play: Epic Advancement).
- The four "Heroes of…" pages are now guides under Characters. The "optional, ask your GM" boxes are gone, and the Northlands and Horror guides each gained a "Campaign Rules" table (from the two removed hub pages).
- Playing the Game, Equipment, Magic Items, Crafting & Alchemy, Classes, Character Creation, and Home have updated link lists.
- Recommended Magic Items by Class: the column naming each item's book is gone. Every item is linked.
- Last visible book names removed from Void Taint, Curses Diseases and Hazards, Shadow Tokens, Ships and Sea Combat, Trade Goods & Money, Clockwork Extensions.

Left on purpose:
- Bryant's Nautical Rules page and his ship combat pages are untouched apart from moving folders.
- Converting 5e Material names books because that is what the page is about.
- Mentions of the Monster Vault and Game Master's Guide (stat blocks and GM rules that are not on the wiki), and one pointer to the Northlands book for the fenrikyn stat block (Druid, Fenris).
- The world and campaign sections were not reorganized.

Open items for Bryant:
1. Reconcile the three ship combat systems (Ships & Sea) and the three weather systems (Weather, Northlands Weather, Terrain Features).
2. Names I chose for clashes: Boomerang, rebounding; Scythe, war; Spiked shield, large; Bloodhound (Margreve); Northlands Bearfolk; Northlands Trollkin; Midgard Dhampir; Midgard Goblin.
3. Dragonscale armor and Dragonhide are both kept. Syderean "spellborn" appears twice.
4. Scythe, war is 1 sp for 1d12 as printed, probably a misprint. The armor "Gunpowder" property is undefined.
5. Five people pages carry their own copy of lineage traits.
6. Pirates & Plunder is still waiting on three answers (ship combat as a system, guns, ratfolk).
