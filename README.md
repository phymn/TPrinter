# TPrinter: Lexmark Field Repair (v4.4, public edition)

`lexmark-repair-app.html` is a one-file web app for printer field technicians who work on Lexmark printers and MFPs. You paste the text of a service ticket into it. It cleans up the text, pulls out the important details, works out which printer it is, gives each part number its proper name, and suggests a repair flow. It runs in any modern browser on a phone or a computer and needs no server, no installation and no account.

## What it does

- **Ticket clean-up:** paste the raw ticket text (call number, incident number, location, system type, issue and parts). The app tidies it into readable text and shows a summary of the call number, incident, location, hours, system type, model, issue and parts. A "Copy Cleaned Text" button copies the tidy version.
- **System type → model name:** machine type/model numbers such as `4064-430` are shown by their model name (`MS823dn`), with the number in small text underneath. The catalog has 258 system types.
- **Part number → FRU name:** part numbers such as `41X1115` are shown by their FRU name ("Fuser Type 00 115V Letter"), with the number in small text. The catalog has about 2,386 part numbers, mostly 41X and 40X FRUs.
- **Guided repair flows:** step-by-step checklists with a progress bar, currently for the fuser maintenance kit and for vertical streaks. Part numbers inside the steps are shown by name too.
- **Repair videos and online search:** quick links to videos, Google, YouTube and Lexmark Support, filled in from the ticket.
- **Model & Parts Database:** search the whole catalog by model name, system type, part number or part name. For example, "MS821dn", "4064-230", "41X1076" and "transfer roller" all find results.
- **Your own database:** add, edit and delete your own system types and parts. They are saved on your device (browser `localStorage`) and used everywhere in the app straight away.
- **Web lookup for unknown numbers:** if a ticket has a part number that isn't in the catalog and the device is online, the app tries to find its name on the web. The result is labelled "from web, unverified" and has a "Save to local database" button. A "Look up & add" button also searches DuckDuckGo and Wikipedia and pre-fills the add form.
- **Need Help?:** a list of national service contacts.

## How to use it

**Phone (iPhone or Android)**
1. Download `lexmark-repair-app.html` to the phone, for example to the Files app.
2. Open it in Safari or Chrome. On iPhone, you can also serve it locally (for example with `python3 -m http.server` in iSH) and open `http://127.0.0.1:8000/lexmark-repair-app.html`.
3. Paste the ticket text and tap **Normalize & Analyze**. Use the **Ticket**, **Need Help?** and **Database** buttons at the top to switch screens.

**Desktop**
- Double-click the file to open it in any modern browser (Chrome, Edge, Firefox or Safari).

## Offline use

Everything (the app, the catalog and the guided flows) is inside the one HTML file, so after you have downloaded it the app works with no network connection. Only the optional extras need the internet: web lookup, video links and online search. When offline, the app simply doesn't try them.

## Why there are no photos

This public edition has **no part photos, printer photos or service-manual drawings**. Those images are copyrighted by Lexmark or by the third-party parts sellers whose product photos they are, and the drawings come from Lexmark service manuals that are not meant for public redistribution. To respect those rights, they are left out of this edition.

What this means for you:
- Part names and part numbers are still included, and so are model names and system types. Every card shows the name and number. Where a photo would go, the card simply has no picture (there are no empty boxes).
- The code still supports photos. There is a private build (not published) with part photos, printer photos and manual drawings, plus a full-screen zoom viewer. In this edition the image tables are empty, so the viewer can never open.

## Data sources and accuracy

- Model names and system types come from Lexmark product pages, regulatory notices and service-manual model tables.
- Part names come from Lexmark service-manual parts catalogs (short part names only) and from the public product listings of parts sellers (iteminc.com, tonerparts.com, onlineinkdirect.com and fastprinters.com).
- Some entries are marked as unverified. Always confirm the part number and fuser type code on the unit before ordering parts.

This project is not affiliated with or endorsed by Lexmark. "Lexmark" and the product names are trademarks of their owners.

## Files

- `lexmark-repair-app.html`: the app (v4.4 public edition).
- `docs/HOW-IT-WORKS.md`: a detailed technical description.
- `tools/make_public_v44.py`: the script that makes this public edition from the private build by removing all images.
