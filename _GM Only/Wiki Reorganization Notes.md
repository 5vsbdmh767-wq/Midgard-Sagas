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
