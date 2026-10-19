# How TPrinter v4.4 works (public edition)

TPrinter is one self-contained HTML file (`lexmark-repair-app.html`, about 400 KB) with inline CSS and JavaScript. It has no build step, no framework and no server. This document describes everything in v4.4.

## 1. Screens

There are four screens, switched with the top buttons by `showView()`:

| Screen | Element | What it shows |
|---|---|---|
| Ticket (paste) | `#screen-paste` | A text area for the ticket and the Normalize & Analyze button |
| Ticket (results) | `#screen-results` | Cleaned text, extracted information, printer, parts, guided flow, videos and online search |
| Need Help? | `#screen-help` | National service contacts |
| Database | `#screen-db` | Search, results, the add/edit form and the "Not in catalog?" web search |

The **Ticket** button shows the results screen if a ticket has already been analyzed, and otherwise the paste screen. (v4.4 fixed a crash here when no ticket had been analyzed yet: the app read `lastExtracted.parts.length` while `lastExtracted` was still `{}`.)

A footer at the bottom of every screen shows the version: `v4.4 public edition`.

## 2. Ticket processing

1. **`normalizeText(raw)`** joins broken lines, collapses spaces and puts each field on its own line, giving the "Cleaned Text".
2. **`extractInfo(text)`** uses regular expressions to find:
   - `systemType`: `SYSTEM TYPE: nnnn-nnn`, or the first `nnnn-nnn` in the text
   - `callNumber` (`CAS-…`) and `incident` (`INC…`)
   - `location` from `PHYLOC1-3` and `CONTACT LOCATION`
   - `modelHint` from `LEXMARK: …` or an MS/MX model in the text
   - `hours` (for example `8 AM TO 5 PM`)
   - `issue` and `issueKey` (fuser, streak and so on) from the ISSUE line
   - `parts`: every `41X…`, `40X…` and `58D0Z0E` number
   - special notes, such as the ICR / web deployment reminder after a system board or whole-unit swap
3. **`processText()`** builds the results screen:
   - **Extracted Information:** the system type is shown by its model name with the number in small text, and each part is shown by its FRU name with the number in small text.
   - **Printer card:** the model name, system type, family and notes, plus Lexmark product page and image search links. If the system type is unknown, buttons let you add it or search the web for it.
   - **Parts cards:** for a kit (for example `41X2233`), `kitParts()` lists every part in the kit with a role tag (PRIMARY / KIT). For a known part, the card shows its name, number and description. For an unknown part, it shows Google, How to replace, YouTube and Look up & add buttons, and runs the automatic web name lookup (section 6).
   - **Guided flow:** `buildFlow()` picks the fuser-kit flow or the vertical-streaks flow. `labelPNs()` then replaces every part number in the flow text with "**Name** (number)". Each step has checkboxes, and `checkFlow()` updates the progress bar and marks steps as done.
   - **Videos and online search:** links built from the system type, model and parts.

## 3. Catalog data

All data is inline JavaScript:

- **`knowledge.systems`**: the built-in system types, each `{model, family, notes}`. **`EXTRA_SYS`** adds more types, taken from service-manual model tables and Lexmark notices. Together there are 258 system types.
- **`knowledge.parts`**: the hand-curated core parts (about 87), each `{name, desc, used, issue}`. **`EXTRA_PARTS`** adds about 2,300 more. Their names come from short service-manual part names and from parts-seller listings, and each entry's `desc` says where its name came from. Together there are about 2,386 parts.
- At start-up, `EXTRA_SYS` and `EXTRA_PARTS` are merged into `knowledge`. `getSystems()` and `getParts()` then merge in the user's custom database, and custom entries win.

Name helpers:
- `sysName(key)` returns the model name, or the number if the model is unknown.
- `partName(pn)` returns the FRU name, or `null`.
- `sysLabelHtml()` and `partLabelHtml()` format "**Name** `number`" for display.

## 4. Database search

`searchDb(q)` matches the lower-case query against `number + name + family/notes` for system types and `number + name + description + used-in` for parts. It shows up to 80 results. Each result shows the name first and the number small, with a kind chip and a CUSTOM chip for your own entries. Custom entries have Edit and Delete buttons. Before v4 the search read only the built-in list and crashed when a custom entry existed; it now reads the merged list.

## 5. Your own database

- The custom database is stored in `localStorage` under the key `lexmark_custom_db_v1` as `{systems:{}, parts:{}}`.
- `openAddForm()`, `editCustom()`, `saveAddForm()` and `deleteCustom()` add, edit and delete entries. They check the format of system types (`nnnn-nnn…`) and part numbers, and ask before replacing a built-in entry.
- After any change, `refreshAfterSave()` re-renders the current screen, so a saved part is named straight away on the open ticket.

## 6. Web lookup

- **Automatic name for an unknown part** (`autoNamePart`): only runs when `navigator.onLine` is true.
  1. It first asks the fastprinters.com product-search JSON, through the `api.allorigins.win` CORS proxy, for a product whose title contains the part number.
  2. If that finds nothing, it searches DuckDuckGo Lite through the same proxy and parses the results with `parseLiteDdg`.
  3. A name it finds is shown as "from web, unverified", with its source and a **Save to local database** button (`saveWebPart`).
  4. Offline, nothing is fetched and the card looks as it did before.
- **Look up & add** (`smartLookup`): queries the DuckDuckGo Instant Answer API, the Wikipedia search API and DuckDuckGo Lite, shows up to 7 findings, and can pre-fill the add form (`prefillFromLookup`, `guessModel`).
- **Privacy note:** these lookups send the part number or system type to the proxy and the search services. Nothing else from the ticket is sent.

## 7. Pictures (not in this edition)

The private build embeds printer-family photos, part photos (including "representative" photos shared by voltage or language variants), service-manual exploded-view drawings, and larger images for a full-screen viewer with pinch, pan and double-tap zoom. In this public edition the tables `FAM_IMG`, `PART_IMG`, `PART_REP`, `ILL_IMG`, `PART_ILL` and `CALLOUT` are empty, so:

- `imgFor()`, `partImg()`, `partThumbHtml()` and `miniThumb()` return nothing, and cards show only names and numbers, with no empty box.
- The viewer code (`openViewer`) is still in the file, but no element calls it.

`tools/make_public_v44.py` makes this edition from the private file by emptying those tables, removing the large-image `<script type="text/plain">` blocks and changing the footer and title. It also checks that no embedded photo data is left.

## 8. Need Help?

A static list of national service contacts, shown on its own screen.

## 9. Browser support

The app works in current Safari (iOS 14 and later), Chrome, Edge and Firefox. It uses no external scripts or fonts. The phone layout is built for a screen about 390 px wide and adapts to larger screens.
