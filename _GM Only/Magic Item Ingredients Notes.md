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
- 29 items can't be crafted: the 28 fabled items (the core rules put fabled items beyond mortal crafting) and [[Anuraag’s Crucible]] (an artifact).

## Humanoid parts in the item text

The harvesting rules treat harvesting Humanoids as evil and the parts as unusable. These items say they are made from Humanoid parts (or might be). I listed monster parts instead; say if you want it the other way.

| Item | Rarity | Note |
|---|---|---|
| [[Baba Yaga’s Cinderskull]] | Rare | The item only says a white, dry skull. In the folk tale her fence skulls are human (my reading), so I left the skull out; these give the heat and light. |
| [[Blood-Soaked Hide]] | Very Rare | Text says it's tanned humanoid skins, which the harvesting rules treat as evil and unusable. Listed monster parts instead. |
| [[Bone Whip]] | Very Rare | Text says it's humanoid vertebrae and skin, which the harvesting rules rule out. Listed monster parts instead. |
| [[Book of Ebon Tides]] | Very Rare | Text says it's bound in shadow goblin hide. If your table counts shadow goblins as Humanoids, leave that out; these cover the magic. |
| [[Broth of Needful Fortitude]] | Very Rare | Text says it's brewed from humanoid flesh and bone, which the harvesting rules treat as evil and unusable. Listed undead parts instead. |
| [[Burning Skull]] | Very Rare | Text says the skull is human, which the harvesting rules rule out. Listed monster parts instead. |
| [[Centaur Wrist-Wraps]] | Uncommon | Text credits centaur shamans. If your table counts centaurs as Humanoids for harvesting, keep centaur parts out of it. |
| [[Consuming Rod]] | Very Rare | Text says it's carved from a humanoid femur, which the harvesting rules rule out. Listed monster parts instead. |
| [[Corpsehunter’s Medallion]] | Rare | Text offers grave rat skulls or the bones of the ignoble dead. The second is humanoid bone, which the harvesting rules rule out, so only the rats are listed. |
| [[Craven’s Heart]] | Uncommon | Text says it's a dried humanoid heart, which the harvesting rules rule out. Listed a monster part instead. |
| [[Oracle Charm]] | Common | Text says it's a human finger bone, which the harvesting rules rule out. Listed a monster part instead. |

## Named source under the floor

The item text names its own source, and that creature is too weak for the item's rarity. I kept the named source because the item is built on it. Options: let these stand as exceptions, or swap in a stronger main ingredient.

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

The item names a creature whose CR I couldn't confirm from Monster Vault or the Field Guide tables.

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

## Odd origins

The item text says it was given, not made. I listed what a crafter would need anyway.

| Item | Rarity | Note |
|---|---|---|
| [[Clockwork Hare]] | Legendary | Text says it's a god's gift. Listed what a crafter would need; you may rule it can't be made. |
| [[Talisman of the Snow Queen]] | Very Rare | Text says the Snow Queen grants these. Listed what a crafter would need; you may rule only she can make them. |
| [[Void-Touched Buckler]] | Very Rare | Text gives an accidental origin (it sat beside a tear into the Void for decades). Listed what a crafter would use instead. |

## No monster parts

These say they're made from something that isn't a monster. Their line says so instead of listing ingredients.

| Item | Rarity | Note |
|---|---|---|
| [[Blue Rose Tea]] | Uncommon | Brewed from blue rose petals, per its own text. |
| [[Blue Rose]] | Rare | It's the blue rose itself, a flower. |
| [[Breathing Reed]] | Common | It's a magic river reed. |
| [[Honey of Ancient Meadows]] | Rare | Spirit honey from flowers in ancient meadows, per its own text. |
| [[Honey of Dead Fields]] | Uncommon | Spirit honey from graveyard and battlefield flowers, per its own text. |
| [[Honey of Gloomy Flowers]] | Rare | Spirit honey from Shadow Realm flowers, per its own text. |
| [[Honey of Warped Wildflowers]] | Very Rare | Spirit honey from magic-warped wildflowers, per its own text. |
| [[Memory Philter]] | Rare | It's a mortal's memory, traded to the fey. |
| [[White Dandelion]] | Common | It's a magic flower. |

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
