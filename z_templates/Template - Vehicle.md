---
tags:
  - Vehicle
art: "[[PlaceholderVehicle.png]]"
aliases:
vehicleType:
rarity:
owners:
assistants:
organizations:
currentLocation:
publish: false
---

> [!infobox | no-blending black]+ <font color="#ffffff">Infobox</font>
> 
> `VIEW[!{art}][text(renderMarkdown)]`
> 
> ###### Details
> |  |  |
> | --- | --- |
> | **Aliases** | `VIEW[{aliases}][text]` |
> | **Type** | `VIEW[{vehicleType}]` |
> | **Rarity** | `VIEW[{rarity}]` |
> | **Owners** | `VIEW[{owners}][link]` |
> | **Assistant** | `VIEW[{assistants}][link]` |
> | **Organization** | `VIEW[{organization}][link]` |
> | **Location** | `VIEW[{location}][link]` |

# `=this.file.name`

> [!quote]- Scene Introduction
> A script to read from when the party arrives to the area for the first time to set the scene.

## Overview 

### Description:

> *<font color="#7f7f7f">Describe the vehicle’s appearance, noting its size, construction, materials, and any unique or distinctive features.</font>*

## Database

![[Database - Vehicle Note.base]]

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

## Present

### Crew:

| Name    | Information / Description |
| ------- | ------------------------- |
| Example |                           |

### Cargo:

| Name    | Price (gp) | Information / Description |
| ------- | ---------- | ------------------------- |
| Example | 0.1        |                           |

### Current Events:

- *<font color="#7f7f7f">Example Quest</font>*
    - *<font color="#7f7f7f">Summary of a quest the player can get involved in.</font>*
- *<font color="#7f7f7f">Example Event</font>*
    - *<font color="#7f7f7f">Summary of an event that's going on surrounding this vehicle and its crew which.</font>*

## Past

### History:

> *<font color="#7f7f7f">Summarize the vehicle’s history, including its origin, past owners, notable events, and how it gained its current reputation or role.</font>*

### Secrets, Rumours & Legends:

> *<font color="#7f7f7f">Detail the secrets, rumours, and legends surrounding this vehicle, including whispered stories, superstitions, or hidden truths that may or may not be real.</font>*

## Notes

