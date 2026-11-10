---
publish: false
---
# How to Publish the Wiki

This vault is set up to go online with Obsidian Publish. Everything under **_GM Only** stays private.

## 1. Open this vault

1. Unzip **Midgard Sagas.zip**. You get a folder called **Midgard Sagas**, and that folder *is* the vault: `publish.css`, `Home`, and the `.obsidian` settings sit directly inside it.
2. In Obsidian, click the vault name in the bottom-left corner, choose **Manage vaults**, then **Open folder as vault**, and select **Midgard Sagas** itself.
3. Check the top of the file list: `_GM Only`, `Assets`, `Between Iron & Oak`, `Cosmology`, `Midgard`, `Past Campaigns`, `Rules`, `z_templates`, and `Home`. If you see a single folder with everything inside it, you opened one level too high.

> [!warning] If you use Obsidian Sync
> This counts as a new vault. Connect it to Sync under **Settings → Sync**.

## 2. Connect to your site

Click the paper plane. If it asks for a site, choose your existing **midgard-sagas** site (or click **Switch site** and pick it).

**First time only: remove the old copies.** Your first upload went up under `Tales of the Corsair Coast/...`. Those notes aren't in this vault, so the Publish window should list them as deleted. Select them all and publish to take them down. Then publish everything under **NEW**, including `publish.css`.

## 2b. Or create a new site

1. Click the **paper-plane icon** in the left ribbon (Publish changes).
2. Sign in and subscribe if asked, then **Create a new site**. The site ID you choose becomes your address, like `publish.obsidian.md/your-site-id`.

## 3. Lock away the GM folders (one time)

1. In the Publish changes window, click the **filter icon** (Manage publish filters).
2. Next to **Excluded folders**, click **Manage** and add `_GM Only`, `z_templates`, and `Assets/Excalidraw`.
3. Click **Done**.

Every note in those folders also has `publish: false` in its properties, as a backup.

## 4. Site options

In the Publish changes window, click **Change site options**.

- **Site Name:** Midgard Sagas
- **Homepage File:** `Home`
- **Theme:** Dark. Turn on the **Light/Dark Toggle** if players should be able to switch.
- **Hide page title:** OFF. **Strict line breaks:** OFF. The design and the stat blocks rely on both being off.
- **Show navigation**, **Show search bar**, **Show backlinks**, **Show hover preview:** on.
- **Passwords:** click **Manage**, then **New password**, then **Add this password**. Give the password to your players. This keeps the site to your table, which matters because much of the Midgard lore is copied from Kobold Press books.

## 5. Publish

1. Click the paper-plane icon again.
2. Under **NEW**, select all, and make sure `publish.css` is ticked (it's the site design and isn't shown in the file list). Then click **Publish**.
3. Click **View site** to see it live.

## Updating through GitHub (GitHub Desktop)

The vault lives in a private GitHub repository called **Midgard-Sagas**. Claude makes changes there, and **GitHub Desktop** brings them down to your computer. No more zips.

### One-time setup

1. Install **GitHub Desktop** from desktop.github.com and sign in.
2. Choose **File → Clone repository**, pick **Midgard-Sagas** on the GitHub.com tab, choose a folder you'll remember, and click **Clone**.
3. In Obsidian, **Manage vaults → Open folder as vault**, and pick that cloned folder.

Your Publish site doesn't care which folder the notes come from. Click the paper plane, choose **midgard-sagas** if asked, and publish as usual.

### After Claude makes changes

1. Open GitHub Desktop. Click **Fetch origin**, then **Pull origin**.
2. In Obsidian, click the paper plane. Pages with `publish: true` are already ticked under **NEW** and **CHANGED**. Also tick `publish.css` and anything in `Assets` if they changed.
3. Look at **DELETED** before you click Publish. If it lists pages you still want, untick them and tell Claude.
4. Click **Publish**.

### After you edit pages yourself

1. Open GitHub Desktop. Your changed files are listed on the left.
2. Type a short note in the **Summary** box at the bottom left (anything, like "my edits"), click **Commit to main**, then **Push origin**.

Do this before asking Claude for more changes, so Claude works from your latest version.

> [!warning] If something goes wrong
> Every change is saved in GitHub's history, so nothing is lost for good. If GitHub Desktop reports a conflict (you and Claude changed the same lines), don't fix it by hand. Tell Claude and it will sort it out in the repo.

## Day to day

- **Edit a note** → click the paper plane → changed notes are already ticked → **Publish**.
- **New notes you write** need `publish: true` in their properties, or tick them by hand under NEW.
- **Hide one note:** set its `publish` property to `false`.
- **Show a hidden note:** about 60 empty placeholder notes are hidden. Once you write in one, change `publish: false` to `publish: true` and publish it.
- **GM secrets** go in `_GM Only` or never get typed into a player page. Hidden `%% comments %%` are **not** private. Anyone can read a page's raw text.

## Adding a banner image

1. Save the image into the `Assets` folder as `Banner.webp` (or `.png`/`.jpg`).
2. In `Home`, add `![[Banner.webp]]` as the first line under the properties.

Midjourney prompt:

```
Dark oil painting, chiaroscuro, a brass clockwork city of steep roofs and gear-towers at dusk giving way to a vast ancient black-oak forest, a single road running between them into shadow, shadows creeping from the treeline against the lamplight, heavy impasto brushwork, muted ochre and deep green with ember highlights, moody, painterly, no text --ar 21:9
```

## Adding a Forge link

In `Home`, add these two lines inside the first `[!multi-column]` block, after the `[!recap]` line:

```
>
>> [!vtt] &nbsp; **[Forge VTT](https://YOUR-GAME.forge-vtt.com)**
```

Replace the address with your Forge game link.

## What won't show on the website

Publish shows plain notes, images, tables, and callouts. It does **not** run plugins, so these only work inside Obsidian:
- Dataview queries, Leaflet maps, Fantasy Statblocks, Banners, Meta Bind (the calculators), Kanban, Excalidraw

## How the vault is organized

| Folder | What goes there |
| --- | --- |
| `Home` | The landing page |
| `Between Iron & Oak` | Campaign primer, The Party, Story So Far |
| `Midgard` | The world: Crossroads, Southlands, Wasted West, peoples, calendars, legends |
| `Cosmology` | Gods, cults, and the planes |
| `Rules` | The Player's Guide (character creation, classes, lineages & heritages, backgrounds & talents, equipment, magic items, playing the game, spellcasting, spells, rituals, conditions) plus your house rules, variant rules, crafting & alchemy, and nautical rules |
| `Past Campaigns` | Tales of the Corsair Coast: its player characters and NPCs |
| `_GM Only` | Never published: prep, run sheets, loot, calculators, this guide |
| `Assets` | Images |
| `z_templates` | Templater templates (never published) |

**Hub pages:** each folder has an index page (Midgard, Cosmology, Rules, The Crossroads, Calendars, Legends, People of Midgard, Crafting & Alchemy, Tales of the Corsair Coast, NPCs). The lists on *Cosmology*, *Rules*, *Calendars*, *Legends*, *The Crossroads*, *People of Midgard*, *Crafting & Alchemy*, and the Corsair Coast pages were generated from the folders. When you add a note, add a link to it on its hub page.

## Site look

The site is styled as a Margreve house book. Everything lives at the end of `publish.css`, under `Between Iron & Oak: house book`.

- **Embroidered band:** a cross-stitch border of diamonds and acorns in brass, rust, verdigris, and moss thread. It runs under every page title, and a short piece of it marks each `---` section break.
- **Type:** IM Fell English (a 17th-century printing type) for titles and drop caps, and Alegreya for body text and small-cap headings.
- **Glosses:** sidebars and stat blocks sit on a darker panel with a stitched top edge. Links have a dotted underline, and tables are styled like a ledger.
- **Colors:** dark mode is black oak and light mode is unbleached linen. Both use the brass, rust, verdigris, and moss thread colors.
- **Page tags.** Two settings you can add to a note's properties:
  - `cssclasses: [home]`: hides the page title; only Home uses it.
  - `cssclasses: [lore]`: gives each section a drop cap. Used on the campaign primer, Story So Far, Zobeck, The Margreve, and Great Northern Road. Add it to any lore page you like.
- **Home columns:** use `> [!multi-column]` with nested `>>` boxes. The box types are `world`, `gods`, `rules`, and `archive`.

All of this only changes the website. Your Obsidian app keeps its own theme. If the embroidered band doesn't show under page titles on the live site, tell Claude. Publish's page-title markup couldn't be checked from outside.

## What won't show on the website

Publish shows plain notes, images, tables, and callouts. It does **not** run plugins, so these only work inside Obsidian:
- Dataview queries, Leaflet maps, Fantasy Statblocks, Banners, Meta Bind (the calculators), Kanban, Excalidraw

## How the vault is organized

| Folder | What goes there |
| --- | --- |
| `Home` | The landing page |
| `Between Iron & Oak` | Campaign primer, The Party, Story So Far |
| `Midgard` | The world: Crossroads, Southlands, Wasted West, peoples, calendars, legends |
| `Cosmology` | Gods, cults, and the planes |
| `Rules` | The Player's Guide (character creation, classes, lineages & heritages, backgrounds & talents, equipment, magic items, playing the game, spellcasting, spells, rituals, conditions) plus your house rules, variant rules, crafting & alchemy, and nautical rules |
| `Past Campaigns` | Tales of the Corsair Coast: its player characters and NPCs |
| `_GM Only` | Never published: prep, run sheets, loot, calculators, this guide |
| `Assets` | Images |
| `z_templates` | Templater templates (never published) |

**Hub pages:** each folder has an index page (Midgard, Cosmology, Rules, The Crossroads, Calendars, Legends, People of Midgard, Crafting & Alchemy, Tales of the Corsair Coast, NPCs). The lists on *Cosmology*, *Rules*, *Calendars*, *Legends*, *The Crossroads*, *People of Midgard*, *Crafting & Alchemy*, and the Corsair Coast pages were generated from the folders. When you add a note, add a link to it on its hub page.

## Site look

The colors (aged brass, dark bronze, deep teal, forest green, and verdigris on near-black oak in dark mode, or dark aged parchment in light mode) are in the last block of `publish.css`, marked `palette`. Headings use the Alegreya SC font. Side-by-side boxes on the home page use `> [!multi-column]` with nested `>>` callouts, the same pattern as the Yanis Chronicles site. The custom box types are `campaign`, `party`, `recap`, `vtt`, `world`, `gods`, `rules`, and `archive`.

Visitors can switch between dark and light mode on the site. If you want it to open in dark mode, look for the theme setting in Site options.

All of this only changes the website. Your Obsidian app keeps its own theme. To change a color, edit the `--…-rgb` numbers in the palette block.

## What was changed in this vault

- **Moved to `_GM Only`:** Lazy DM prep, the Rushfens run sheets and fen-crossing encounters, Loot Drops, Uvalius' house, the ToV Info Center.
- **Root clutter filed:** Alkahest and Apothecary moved into *Crafting, Alchemy, etc* (replacing the duplicate notes that only embedded them). The recipe catalogs replaced their embed-only notes. Languages and Blood Kingdom moved into *Midgard*.
- **Deleted (all empty):** `NPC Name`, the old 5-link `Landing Page`, an `Untitled` note, and an empty duplicate of Yuid Tyrnoir under NPCs.
- **Renamed:** `z_templates/NPC's` → `NPC Template`, so it no longer clashes with the `NPC's` index page. The Templater hotkey was updated to match.
- **NPC pages:** unfilled template fields, placeholder "Related" links, and broken Dataview blocks removed.
- **Empty notes:** about 60 hidden with `publish: false`. Empty section pages now list the pages inside them.
- **New pages:** Home, The Party, Story So Far, People of Midgard, Castle Shadowcrag, Niemheim, The Ironcrags, Magdar Kingdom, Blood Kingdom, The Darakhul Imperium, Gnomes, Elfmarked, Centaurs, Baba Yaga, The Shadow Realm.
- **Styling:** layout and palette added to the end of `publish.css`. The layout is also on as a snippet inside Obsidian.

### Second pass (reorganization)

- **New top-level layout:** see the table above. `Campaigns/Between Iron & Oak` → `Between Iron & Oak`. `Crafting, Alchemy, etc` → `Rules/Crafting & Alchemy`. `Calculators` → `_GM Only/Calculators`. `The Mharoti Empire` → `Midgard`. `Wasted West Atlas` → `Wasted West`. `NPC's/Legends` → `Midgard/Legends`.
- **Corsair Coast PCs and NPCs** → `Past Campaigns/Tales of the Corsair Coast`. The Corsair Coast *places* stay in `Midgard/Southlands`.
- **Shallower folders:** about 45 folders that held a single note were removed, and the note moved up a level. For example, `People of Midgard/Kobolds/Kobolds` is now `People of Midgard/Kobolds`. The `Locations` level under Southlands is gone. Links are unaffected, since Obsidian links by note name.
- **Links fixed:** about 30 links with stray spaces, plus 13 typo or variant links (e.g. `[[Mharoti Empire]]` → *The Mharoti Empire*, `[[Istagal Raiders]]` → *The Istagal Raiders*).
- **Headings:** ALL-CAPS headings on 10 pages changed to normal capitalization.
- **Hidden:** Cornelius (a blank character-sheet template that would have shown raw code).
- **New pages:** Sarastra, Perun, Volund, Lada, House Stross, Arcane Collegium, King Lucan, Krakovar, Kariv, plus hub pages for The Crossroads, Calendars, Legends, Crafting & Alchemy, and Tales of the Corsair Coast.
- **Orphans linked:** every published page can now be reached from a hub. That includes the 12 calendars, the Ravatet locations, Weather, Swimming, Qamari, and Coastal Ruins.

### Third pass (style)

- Rewrote every added page to match the vault's own formats: the italic title list and ==highlighted== sections on god pages, the ruler table on nation pages, plain prose elsewhere, and no repeated title line at the top.
- Hub pages are plain lists now.
- Home page rebuilt around `[!multi-column]` boxes. The centered banner and hover cards are gone.
- Storros is published again. Alchemists' Association links became plain text. `Meghal Yuhatar` was renamed `Meghal Yuhatara`.

### Fourth pass (Player's Guide)

- Added the Tales of the Valiant Player's Guide rules as 69 pages under `Rules`: 13 class pages (with subclasses), lineages, heritages, backgrounds, three talent pages, eight equipment pages, magic items grouped by type, six Playing the Game pages, spellcasting rules, spell lists, spells by circle, rituals in three groups, and conditions. The historical pantheons went into `Cosmology/Religion`.
- Spell and magic item names in italics link to their entries. The spell lists were rebuilt from the spell entries, so each spell shows its school and one-line summary.
- Not included: the introduction and safety tools, "Player Advice" sidebars, the Labyrinthian Pantheon, the creatures appendix, art, and the index.
- Credit: every rules page ends with the required Black Flag Reference Document 1.2 (CC BY 4.0) notice, and Home and Rules carry it too. Keep these lines if you edit the pages.
- The Kobolds page's copied lineage traits were replaced with a link to the Kobold section of Lineages. Dwarves, Elves, and Humans also link to their lineage rules.
