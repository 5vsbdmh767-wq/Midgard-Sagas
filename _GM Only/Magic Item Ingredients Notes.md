---
publish: false
---
Notes on the "Made with" lines added to every *Vault of Magic* item page on 24 November 2026. The rule itself is on [[Crafting Magic Items]] and in the bible (v5.32). Everything here is for your call; nothing has been resolved silently.

## What was done

- 849 Vault of Magic item pages got one "Made with" line, just above the "Part of" footer. The line links to [[Crafting Magic Items]].
- New player page: [[Crafting Magic Items]] (the rule, in my words). Linked from [[Crafting & Alchemy]] and [[Monster Harvesting]].
- [[Monster Harvesting]]: the "Flawed System" callout said magic item crafting wasn't covered yet. That sentence now points to the new page instead.
- [[Credits]]: added the *Field Guide to Monster Harvesting*, volumes 1 and 2.
- Every ingredient choice is mine, matched to what the item does and checked by script: named materials exist in the Field Guide, ingredient counts match rarity (consumables one fewer), and the main ingredient can come from a creature at the rarity's floor. Where it can't, the item is flagged below.
- The data lives in `.wiki-tools/items/ingredients.json` and `.wiki-tools/items/ingredients.py` writes the lines. To change an item, edit its entry in the JSON and rerun the script; it replaces the old line rather than adding a second one.
- 32 items can't be crafted: the 28 fabled items (the core rules put fabled items beyond mortal crafting), [[Anuraag’s Crucible]] (an artifact), and the three given-not-made items below.

## Humanoid parts in the item text

**Ruled 24 Nov: kept as written.** These items name humanoid parts. The harvesting rules make those parts unusable, so players normally can't craft them, but the items stay as they are.

| Item | Rarity | Note |
|---|---|---|
| [[Baba Yaga’s Cinderskull]] | Rare | Kept as written (GM, 24 Nov): the text says only a white, dry skull. In the folk tale her fence skulls are human (my reading, not the item's). |
| [[Blood-Soaked Hide]] | Very Rare | Humanoid parts, kept as written (GM, 24 Nov). The harvesting rules make these parts unusable, so this normally can't be crafted. |
| [[Bone Whip]] | Very Rare | Humanoid parts, kept as written (GM, 24 Nov). The harvesting rules make these parts unusable, so this normally can't be crafted. |
| [[Book of Ebon Tides]] | Very Rare | Kept as written (GM, 24 Nov): shadow goblin hide. If your table counts shadow goblins as Humanoids, it normally can't be crafted. |
| [[Broth of Needful Fortitude]] | Very Rare | Humanoid parts, kept as written (GM, 24 Nov). The harvesting rules make these parts unusable, so this normally can't be crafted. |
| [[Burning Skull]] | Very Rare | Humanoid parts, kept as written (GM, 24 Nov). The harvesting rules make these parts unusable, so this normally can't be crafted. |
| [[Consuming Rod]] | Very Rare | Humanoid parts, kept as written (GM, 24 Nov). The harvesting rules make these parts unusable, so this normally can't be crafted. |
| [[Corpsehunter’s Medallion]] | Rare | Kept as written (GM, 24 Nov): grave rat skulls or the bones of the ignoble dead. The rat version can be crafted; the humanoid-bone version normally can't. |
| [[Craven’s Heart]] | Uncommon | Humanoid parts, kept as written (GM, 24 Nov). The harvesting rules make these parts unusable, so this normally can't be crafted. |
| [[Oracle Charm]] | Common | Humanoid parts, kept as written (GM, 24 Nov). The harvesting rules make these parts unusable, so this normally can't be crafted. |

## Named source under the floor

**Ruled 24 Nov: named sources are honored**, even under the floor.

| Item | Rarity | Note |
|---|---|---|
| [[Badger Hide]] | Uncommon | Text says badger hide. A giant badger is far under the Uncommon floor. Kept because the item is built on it. |
| [[Bezoar of the Dire Owlbear]] | Very Rare | The bezoar is the item, so the dire owlbear is the source. A dire owlbear (Harvest DC 13) is under the Very Rare floor. Kept because the item is built on it. |
| [[Bezoar of the Hippogriff]] | Rare | The bezoar is the item, so the hippogriff is the source. A hippogriff is far under the Rare floor. Kept because the item is built on it. |
| [[Bezoar of the Manticore]] | Rare | The bezoar is the item, so the manticore is the source. A manticore (Harvest DC 12) is under the Rare floor. Kept because the item is built on it. |
| [[Cinch of the Wolfmother]] | Uncommon | Text says dire wolf intestines. A dire wolf is far under the Uncommon floor. Kept because the item is built on it. |
| [[Crocodile Armor]] | Rare | Text says crocodile skin. A giant crocodile (Harvest DC 13) is under the Rare floor. Kept because the item is built on it. |
| [[Devil's Barb]] | Rare | Text names a barbed devil's quill (CR 5), under the Rare floor. Kept because the item is built on it. |
| [[Dire Bacon]] | Uncommon | Text names a giant boar (CR 2), under the Uncommon floor. Kept because the item is built on it. |
| [[Extract of Dual-Mindedness]] | Legendary | Text says it's distilled from a two-headed giant of genius intellect. An ettin is the nearest (CR 4), far under the Legendary floor. Kept because the item is built on it. |
| [[Gloomflower Corsage]] | Very Rare | Text names a gloomflower. No gloomflower in your books reaches the Very Rare floor. Kept because the item is built on it. |
| [[Hallucinatory Dust]] | Rare | Text says gloomflower pollen. No gloomflower in your books reaches the Rare floor. Kept because the item is built on it. |
| [[Holy Verdant Bat Droppings]] | Rare | Text says green bat guano gathered by derro. The bats are far under the Rare floor. Kept because the item is built on it. |
| [[Honey of Planar Flora]] | Very Rare | Text says nectar from planar flora. Planar flora (Harvest DC 12) is under the Very Rare floor. Kept because the item is built on it. |
| [[Manticore’s Tail]] | Uncommon | Text says manticore spikes. A manticore (Harvest DC 12) is under the Uncommon floor. Kept because the item is built on it. |
| [[Phoenix Ember]] | Legendary | Text says it's a fossilized phoenix egg. A phoenix (Harvest DC 15) is under the Legendary floor. Kept because the item is built on it. |
| [[Pickled Aboleth Brain]] | Very Rare | Text names an aboleth (Harvest DC 14), under the Very Rare floor. Kept because the item is built on it. |
| [[Potion of Troll Blood, Greater]] | Rare | No troll in your books reaches this rarity's floor, but troll blood is plainly the source. |
| [[Potion of Troll Blood, Superior]] | Very Rare | No troll in your books reaches this rarity's floor, but troll blood is plainly the source. |
| [[Potion of Troll Blood, Supreme]] | Legendary | No troll in your books reaches this rarity's floor, but troll blood is plainly the source. |
| [[Potion of Worg Form]] | Rare | Text says worg hair floats in it. A worg is far under the Rare floor. Kept because the item is built on it. |
| [[Purified Phoenix Tear]] | Legendary | Text names a phoenix (Harvest DC 15), under the Legendary floor. Kept because the item is built on it. |
| [[Rust Monster Shell]] | Rare | Text says rust monster shell. A rust monster is far under the Rare floor. Kept because the item is built on it. |
| [[Troll Skin Armor]] | Rare | Text says troll skin. A troll (Harvest DC 13) is under the Rare floor. Kept because the item is built on it. |
| [[Trollsblood Elixir]] | Very Rare | No troll in your books reaches the Very Rare floor, but a troll is plainly the source. |

## Named source, CR not in your books

The item names a creature whose CR I couldn't confirm from Monster Vault or the Field Guide tables. **Bryant to confirm.** Named sources are honored either way, so this only matters for your own sense of each item.

| Item | Rarity | Note |
|---|---|---|
| [[Akaasit Blade]] | Rare | Text says it's made from an akaasit's arm blade. Check the akaasit's CR against the Rare floor; kept because the item is built on it. |
| [[Angelic Earrings]] | Uncommon | Text says chamrosh claws, freely given. Check the chamrosh's CR against the Uncommon floor; kept because the item is built on it. |
| [[Armor of the Ngobou]] | Rare | Text names a ngobou. Check its CR against the Rare floor; kept because the item is built on it. |
| [[Bezoar of the Bespectacled Owlbear]] | Uncommon | The bezoar is the item, so the bespectacled owlbear is the source. Check its CR against the Uncommon floor (an ordinary owlbear is CR 3). Kept because the item is built on it. |
| [[Bezoar of the Great Horned Owlbear]] | Rare | The bezoar is the item, so the great horned owlbear is the source. Check its CR against the Rare floor. Kept because the item is built on it. |
| [[Bezoar of the Hoary Owlbear]] | Rare | The bezoar is the item, so the hoary owlbear is the source. Check its CR against the Rare floor. Kept because the item is built on it. |
| [[Bezoar of the Screech Owlbear]] | Rare | The bezoar is the item, so the screech owlbear is the source. Check its CR against the Rare floor. Kept because the item is built on it. |
| [[Frost Pellet]] | Rare | Text says it's made from a devil shark's stomach lining. Check the devil shark's CR against the Rare floor; kept because the item is built on it. |
| [[Pact Paper]] | Rare | Text says it's made from a pact drake's cast-off scales. Check the pact drake's CR against the Rare floor; kept because the item is built on it. |
| [[White Ape Hide]] | Very Rare | Text says it's made from a white ape. Check its CR against the Very Rare floor; kept because the item is built on it. |

## Given, not made

**Ruled 24 Nov: uncraftable**, like artifacts and fabled items.

| Item | Rarity | Note |
|---|---|---|
| [[Clockwork Hare]] | Legendary | Uncraftable (GM, 24 Nov): it's a god's gift. |
| [[Talisman of the Snow Queen]] | Very Rare | Uncraftable (GM, 24 Nov): only the Snow Queen grants them. |
| [[Void-Touched Buckler]] | Very Rare | Uncraftable (GM, 24 Nov): it became what it is by accident, beside a tear into the Void. |

## No monster parts

These say they're made from something that isn't a monster. Their line says so instead of listing ingredients.

| Item | Rarity | Note |
|---|---|---|
| [[Blue Rose Tea]] | Uncommon | brewed from blue rose petals, per its own text |
| [[Blue Rose]] | Rare | it's the blue rose itself, a flower |
| [[Breathing Reed]] | Common | it's a magic river reed |
| [[Honey of Ancient Meadows]] | Rare | spirit honey from flowers in ancient meadows, per its own text |
| [[Honey of Dead Fields]] | Uncommon | spirit honey from graveyard and battlefield flowers, per its own text |
| [[Honey of Gloomy Flowers]] | Rare | spirit honey from Shadow Realm flowers, per its own text |
| [[Honey of Warped Wildflowers]] | Very Rare | spirit honey from magic-warped wildflowers, per its own text |
| [[Memory Philter]] | Rare | it's a mortal's memory, traded to the fey |
| [[White Dandelion]] | Common | it's a magic flower |

## Other notes

Smaller judgment calls.

| Item | Rarity | Note |
|---|---|---|
| [[Ashes of the Fallen]] | Rare | Text says it's the powdered remains of a celestial. The harvesting rules let a table treat sacred creatures as off-limits; your call whether celestials are. |
| [[Black Dragon Oil]] | Rare | Text says it's a black dragon boiled in its own acid; any black dragon of young age or older meets the floor. |
| [[Brawn Armor]] | Rare | Text says the hide of an ancient grizzly bear. Your books have no such creature; a CR 9+ bear-kind beast or monstrosity would fit. |
| [[Sand Suit]] | Very Rare | Text says it's made from the treated body of a destroyed apaxrusl. That body is the base; these go on top. |
| [[Staff of the Unhatched]] | Uncommon | Text names an unhatched dragon's skull, which has no CR. Treated as meeting the floor. |

## Things I noticed

- Named Field Guide materials thin out at the top. In Monster Vault, very few creatures of CR 13 and up drop named materials, so many Very Rare and Legendary items lean on Elemental Gemstone, Celestial Feather, Aberrant Brain, Throat Scales and generic parts.
- Players won't know what a named material like Voltaic Organ does or who drops it. If you want them able to plan, a player page listing the materials (in my words) would fix that. Not built; your call.
- Three materials appear in the Field Guide's tables with no entry in either book: Chaos Fruit, Psychic Shard and Tough Hide.
