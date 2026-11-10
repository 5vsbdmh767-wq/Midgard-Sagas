---
tags:
  - Location
  - Settlement
location:
mapmarker: Settlement
art: "[[PlaceholderSettlement.png]]"
aliases:
settlementType:
defence:
currentLocation: []
rulers: []
leaders: []
organizations: []
population:
tradePartners:
imports:
exports:
publish: false
---

> [!infobox | no-blending black]+ <font color="#ffffff">Infobox</font>
> 
> `VIEW[!{art}][text(renderMarkdown)]`
> 
> # Info
> |  |  |
> |---|---|
> | **Aliases** | `VIEW[{aliases}][text]` |
> | **Type** | `VIEW[{settlementType}][text]` |
> | **Defences** | `VIEW[{defence}]` |
> | **Location** | `VIEW[{currentLocation}][link]` |
> 
> # Demographics
> |  |  |
> |---|---|
> | **Rulers** | `VIEW[{rulers}][link]` |
> | **Leaders** | `VIEW[{leaders}][link]` |
> | **Dominion** | `VIEW[{organizations}][link]` |
> | **Population** | `VIEW[{population}][text]` |
> 
> # [[Travel Calculator]] 
> | |
> |---|---|
> | **TBD** | `VIEW[round(0 / (({Travel Calculator#MilesPerHour}*{Travel Calculator#HoursPerDay})*{Travel Calculator#SpeedMultiplier}),1)]` Day(s) |

# `=this.file.name`

> [!quote]- Scene Introduction
> A script to read from when the party arrives to the area for the first time to set the scene.

> *<font color="#7f7f7f">Summarize the settlement by describing its size, purpose, and defining features, along with what makes it stand out from others.</font>*

## Database

![[Database - Settlement Note.base]]

## Map

> [!kirk|map] Map
> ```leaflet
> ### TUTORIAL: INSERT VIDEO LINK HERE
> ### Lines that start with ### are commented out, meaning they will not effect the code. Used to offer guidance. Feel free to remove these.
> ### Uncomment (Remove the ### ) height and width if you would like to manually set the height and width of the leaflet display.
> ### height: 600px
> ### width: 640px
> ### id: vallue will be replaced each time you create a new note.
> id: {{VALUE}}
> image: 
> - [[PlaceholderImage.png|Map 1]]
> lock: true
> recenter: true
> noScrollZoom: false
> ### Leave the first [0,0], then replace the second [5000,5000] with [HEIGHT, WIDTH] of your image.
> bounds: [[0,0], [5000, 5000]]
> ### Use lat & long to set center point of the map.
> lat: 0
> long: 0
> ### Set min, max and default zoom to your desired zooms levels.
> minZoom: -3.5
> maxZoom: 6.5
> defaultZoom: -3.5
> zoomDelta: 0.5
> unit: miles
> ### Measure between two points you know the distance of, then scale up and down util you have your desired distance.
> scale: 0.0404
> ### MapIt is the tag we apply to notes we want to mark on the map. Replace "TBD" with whatever you like WITHOUT spaces.
> ### To add a marker to the map, include the MapIt- tag, and the location and mapmarker property within said note.
> markerTag: 
> - "#MapIt-TBD"
> ```

## Overview

### Description:

> *<font color="#7f7f7f">What is the settlement's environment, architecture, culture, and overall atmosphere? Describe its look and feel, what it's known for, who lives there, and how it fits into the surrounding region.</font>*

### Society & Culture:

> *<font color="#7f7f7f">What is daily life like in the settlement? How do its people think, behave, and interact? Describe customs, traditions, beliefs, social structure, and any notable values or taboos.</font>*

## Commerce

> [!grid|col-2]
> <font color="#9bbb59">**Imported Goods:**</font> `VIEW[{imports}][text]`
>
> <font color="#c0504d">**Exported Goods:**</font> `VIEW[{exports}][text]`

### Trade Agreements:

- [[Template - Settlement]]
   - <font color="#9bbb59">Example Import</font> - Why do they import this from here?
- [[Template - Settlement]]
   - <font color="#c0504d">Example Export</font> - Why do they export to here?

## Present

### Current Events:

- *<font color="#7f7f7f">Example Quest</font>*
    -  *<font color="#7f7f7f">Summary of a quest the player can get involved in.</font>*
- *<font color="#7f7f7f">Example Event</font>*
    - *<font color="#7f7f7f">Summary of an event that's going on on this settlement which may not relate to a specific quest or may relate to multiple.</font>*

## Past

### History:

> *<font color="#7f7f7f">Describe the history of the settlement, including its founding, key events, and how it developed into what it is today.</font>*

### Secrets, Rumours & Legends:

> *<font color="#7f7f7f">Describe the secrets, rumors, and legends tied to the settlement, including hidden truths, whispered stories, and myths that shape how it is perceived.</font>*

## Notes

