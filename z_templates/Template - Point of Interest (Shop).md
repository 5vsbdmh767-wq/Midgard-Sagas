---
tags:
  - Location
  - POI
location:
mapmarker:
art: "[[PlaceholderPointOfInterest.png]]"
aliases:
poiType:
  - Shop
dominion: []
owners: []
assistants: []
organizations: []
currentLocation: []
tradePartners:
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
> | **Type** | `VIEW[{poiType}][text]` |
> | **Dominion** | `VIEW[{dominion}][link]` |
> | **Owners** | `VIEW[{owners}][link]` |
> | **Assistants** | `VIEW[{assistants}][link]` |
> | **Dominion** | `VIEW[{organizations}][link]` |
> | **Location** | `VIEW[{currentLocation}][link]` |
> 
> # [[Travel Calculator]] 
> | |  |
> |---|---|
> | **TBD** | `VIEW[round(52 / (({Travel Calculator#MilesPerHour}*{Travel Calculator#HoursPerDay})*{Travel Calculator#SpeedMultiplier}),1)]` Day(s) |
> | **TBD** | `VIEW[round(0.5 / ({Travel Calculator#MilesPerHour} * {Travel Calculator#SpeedMultiplier}) * 60, 1)]` Minute(s) |

# `=this.file.name`

> [!quote]- Scene Introduction
> A script to read from when the party arrives to the point of interest for the first time to set the scene.

> *<font color="#7f7f7f">Summarize the point of interest, describing what it is, why it stands out, and its importance to the area or story.</font>*

## Database

![[Database - POI Note.base]]

## Map

> [!metadata|map] Map
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

## Goods & Services

### Goods:

| Name    | Price (gp) | Information / Description |
| ------- | ---------- | ------------------------- |
| Example | 0.1        |                           |

### Services:

| Name    | Price (gp) | Information / Description |
| ------- | ---------- | ------------------------- |
| Example | 0.1        |                           |

## Present

### Local Inhabitants (Random Encounter):

| `dice: 1d20\|noform` (Result) | Name    | Information / Description |
| ----------------------------- | ------- | ------------------------- |
| 1                             | Example |                           |

### Trade Deals:

<font color="#ffc000">**Trade Partners:**</font> `VIEW[{tradePartners}][link]`

> *<font color="#7f7f7f">Detail any significant trade deals this shop is currently engaging in. Noting who with, what is being traded, and any important details that may come with it.</font>*

### Current Events:

 - *<font color="#7f7f7f">Example Quest</font>*
    - *<font color="#7f7f7f">Summary of a quest the player can get involved in.</font>*
 -  *<font color="#7f7f7f">Example Event</font>*
     -  *<font color="#7f7f7f">Summary of an event that's going on in the area which may not relate to a specific quest or may relate to multiple.</font>*

## Past

### History:

> *<font color="#7f7f7f">Describe the history of this point of interest, including its origin, past uses, and any significant events that shaped what it is today.</font>*

### Secrets, Rumours & Legends:

> *<font color="#7f7f7f">Detail the secrets, rumors, and legends tied to this point of interest, including hidden truths, whispered stories, and myths that may or may not be believed.</font>*

## Notes

