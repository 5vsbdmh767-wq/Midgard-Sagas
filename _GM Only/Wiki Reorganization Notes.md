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
