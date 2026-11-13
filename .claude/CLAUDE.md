# Midgard Sagas wiki: working rules

This repo is Bryant's Obsidian vault for the player wiki *Midgard Sagas* (Obsidian Publish). The vault root is the repo root. Bryant is not technical and prefers clarifying questions before full answers.

## Source of truth

- The campaign bible lives in the separate private repo `5vsbdmh767-wq/between-iron-and-oak` (`campaign-bible.md`). Read it before any campaign-facing change. It never goes into this repo.
- Order of authority: Bryant's word, then the bible, then my inference. Flag conflicts instead of resolving them silently.
- Sourcebooks (Midgard Worldbook, Southlands, Northlands, Labyrinth, Zobeck, Ebon Tides, Old Margreve, Warlock Grimoires, Tales from the Shadows, Pirates & Plunder, Trade Secrets) are checked by reading them, never from recall.

## What can go on the wiki

- Anything at least one player knows is fine. Hold back only what no player knows. The bible's "Who currently knows what" table is the filter.
- Never on the wiki (no player knows): Qeldar = the Weft, the Weft as primary antagonist, Derende = the Tender, the Night Cauldron and Dariska, Czarizeby, the name Hallisar, Kled, Zondera, Binia, the Sanguine Path, Cylentha's plans, the Moonlit King's escape, the Stross Library portals, the Weft holding the hollow Summer Court, Allia's patron, Vizorakh and the Voidreach secret.
- GM-only material goes in `_GM Only/` with `publish: false`. `%% comments %%` are not private.
- Player pages carry `publish: true` in frontmatter.
- The Publish site is password-protected (private table reference).

## Writing style

- Change only what was asked. List every change. Never delete on uncertainty. Label anything invented as mine.
- Match the existing page formats. No H1 headings (the page title is the H1). No em dashes in new prose. No bold lead-in label lists, except god pages, which use `**Domains:**` lines and `==**Heading**==` labels.
- No crosses or Christian imagery anywhere.
- Paraphrase sourcebook text; don't paste it. Rules pages from the Black Flag Reference Document keep their CC BY 4.0 notice.
- Link names wiki-wide. Inside tables, escape the pipe: `[[Page\|Text]]`.
- Party: three PCs, Lesshy, Rozen and Sidious. Allia and Msshka are off-screen guests; M3L0-D is in Zobeck.
- System: Tales of the Valiant (Black Flag), Foundry VTT v14 on The Forge.

## Organization (Bryant's ruling, 13 Nov 2026)

- The wiki is one rules and lore database, organized by what a reader is trying to do. Nothing is organized by book: no book-named folders, hub pages, "More X (Book)" sections, or "Optional, from X" labels.
- Anything optional is allowed at the table, so nothing is marked "ask your GM".
- Where each thing came from is kept as an invisible note, `%% source: Book Name %%`, on the line under its heading. Add one to anything new. Never show a book name in a heading or label.
- Books are credited only on the `Credits` page. Pages with Black Flag Reference Document text end with the small CC BY footer; other rules pages end with `<small>Sources: [[Credits]].</small>`.
- New material goes where its topic lives: items into the one alphabetical list or table for that kind of thing, rules into Characters, Equipment, Magic, or Playing the Game.
- Two versions of the same thing: if they clearly differ, keep both under one heading as named variants (named for the place or people, not the book). If they are nearly the same, flag it for Bryant.
- Variant systems: Injuries (tied to Called Shots) and DOOM are in play. Spell Points are optional for players. Epic Advancement is an alternate rule not in play. Ship combat and weather each have more than one system and still need reconciling.

## Security

- The *Book of Ebon Tides* PDF carries another person's purchaser watermark. No text from it that includes the watermark may ever be committed. `check.sh` scans for it and the pre-commit hook blocks the commit.
- Never put Bryant's email or other private details in pages, commits or external requests.

## Tools (`.wiki-tools/`, hidden from Obsidian and Publish)

- `sh .wiki-tools/check.sh`: watermark scan, missing links, bad anchors, unescaped table pipes. Run after every batch. Bad anchors and the watermark count must be 0.
- `python3 -I .wiki-tools/autolink.py <copy-of-vault>`: links the first plain mention of each page name. Always run on a copy, read `.wiki-tools/linklog.json`, copy changed files back, then fix bad links by hand. The never-link list is `NOLINK` near the top of the script.
- `linknames.json`: the name list autolink uses.
- `pre-commit-hook`: the watermark guard. In a fresh clone, install it first: `cp .wiki-tools/pre-commit-hook .git/hooks/pre-commit && chmod +x .git/hooks/pre-commit`.

## Workflow

- Pitch the shape in chat first; build after Bryant rules on it. One batch at a time.
- After each batch: run `check.sh`, write review notes in `_GM Only/` (`publish: false`), commit with a plain message, push.
- Bryant pulls and pushes by hand with GitHub Desktop (he chose not to use the Obsidian Git plugin), then publishes from Obsidian. Remind him to pull after a batch, and to push his own edits before asking for more. If his edits conflict with mine, resolve in the repo and keep his wording.
