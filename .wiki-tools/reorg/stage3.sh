# Stage 3: move pages onto topic shelves. Links are by page name, so moves don't break them.
set -e
cd "$(dirname "$0")/../../Rules"
mv_() { mkdir -p "$(dirname "$2")"; git mv "$1" "$2"; }
E="Expanded or Variant Rules"; BB="Book of Blades"; TS="Trade Secrets"; N="Nautical Rules"
# Characters
for f in "Character Creation" "Leveling Up" "Character Sheet" "Random Names"; do mv_ "Character Creation/$f.md" "Characters/$f.md"; done
for f in Backgrounds "Character Threads" "Backgrounds & Talents"; do mv_ "Backgrounds & Talents/$f.md" "Characters/$f.md"; done
for f in Talents "Magic Talents" "Martial Talents" "Technical Talents"; do mv_ "Backgrounds & Talents/$f.md" "Characters/Talents/$f.md"; done
mv_ "$BB/Battle Tactics.md" "Characters/Talents/Battle Tactics.md"
for f in Lineages Heritages "Lineages & Heritages"; do mv_ "Lineages & Heritages/$f.md" "Characters/$f.md"; done
git mv Classes Characters/Classes
mv_ "$BB/Character Themes.md" "Characters/Character Themes.md"; mv_ "$BB/Heroic Endowments.md" "Characters/Heroic Endowments.md"
mv_ "Reference Tables.md" "Characters/Reference Tables.md"
# Equipment
for f in "Siege Engines" Warframes "Clockwork Extensions"; do mv_ "$BB/$f.md" "Equipment/$f.md"; done
# Crafting
mv_ "$TS/Batch Crafting.md" "Crafting & Alchemy/Batch Crafting.md"; mv_ "$TS/Disenchanting.md" "Crafting & Alchemy/Disenchanting.md"
# Magic
mkdir -p Magic; git mv Spellcasting/Spells Magic/Spells; git mv Spellcasting/Rituals Magic/Rituals
for f in Spellcasting "Spell Lists" "Magic Styles" "Spell Points"; do mv_ "Spellcasting/$f.md" "Magic/$f.md"; done
git mv "Magic Items" "Magic/Magic Items"
mv_ "$BB/Arcanepunk Items.md" "Magic/Magic Items/Arcanepunk Items.md"; mv_ "$BB/Weapons of Legacy.md" "Magic/Magic Items/Weapons of Legacy.md"
# Playing the Game
P="Playing the Game"
mv_ Conditions.md "$P/Conditions.md"
for f in "Called Shot" DOOM Injuries "Parry and Defensive Combat" "Parting Shots"; do mv_ "$E/Combat/$f.md" "$P/Combat/$f.md"; done
for f in "Dirty Tactic" Overrun Pilfer Reposition Shove Tumble; do mv_ "$E/Combat/Expanded Melee Attacks/$f.md" "$P/Combat/$f.md"; done
mv_ "$BB/Single Combat.md" "$P/Combat/Single Combat.md"; mv_ "$BB/Terrain Features.md" "$P/Combat/Terrain Features.md"
for f in "Downtime Expanded" "Rewards Expanded" "Base Building"; do mv_ "$E/$f.md" "$P/Downtime & Rewards/$f.md"; done
mv_ "$E/Miscellaneous/Monster Harvesting.md" "$P/Downtime & Rewards/Monster Harvesting.md"
for f in "Shopping & Markets" "Running a Business" "Creating a Business" "Setting Up Shop" "Trade Goods & Money"; do mv_ "$TS/$f.md" "$P/Trade & Business/$f.md"; done
mv_ "$E/Weather.md" "$P/Travel & Weather/Weather.md"; mv_ "$E/Northlands Rules/Northlands Weather.md" "$P/Travel & Weather/Northlands Weather.md"
mv_ "$N/Waterborne Travel.md" "$P/Travel & Weather/Waterborne Travel.md"
for f in Swimming "Underwater Visibility"; do mv_ "$N/Water Rules/$f.md" "$P/Travel & Weather/$f.md"; done
for f in "Attacking & Damage" "Combat Round - Step by Step" Movement "Shipboard Action"; do mv_ "$N/Combat/$f.md" "$P/Ships & Sea/$f.md"; done
for f in Crew "Ship Statblocks"; do mv_ "$N/Ship Rules/$f.md" "$P/Ships & Sea/$f.md"; done
mv_ "$N/Ships and Sea Combat.md" "$P/Ships & Sea/Ships and Sea Combat.md"; mv_ "$N/Nautical Rules.md" "$P/Ships & Sea/Nautical Rules.md"
mv_ "$BB/Naval Battles.md" "$P/Ships & Sea/Naval Battles.md"; mv_ "$E/Northlands Rules/Raiding.md" "$P/Ships & Sea/Raiding.md"
for f in "Curses, Diseases, and Hazards" "Dread Expanded" "Safety Tools" "Shadow Tokens" "Horror Rules"; do mv_ "$E/Horror Rules/$f.md" "$P/Horror/$f.md"; done
for f in Reputation "Flyting and Kennings" "Prophecies and Omens" "Northlands Rules"; do mv_ "$E/Northlands Rules/$f.md" "$P/Renown & Fate/$f.md"; done
# Variant rules not in play
mv_ "$E/Epic Advancement.md" "Variant Rules/Epic Advancement.md"; mv_ "$E/$E.md" "Variant Rules/$E.md"
# book hubs wait in the Rules root for Stage 5
mv_ "$BB/Book of Blades.md" "Book of Blades.md"; mv_ "$TS/Trade Secrets.md" "Trade Secrets.md"
