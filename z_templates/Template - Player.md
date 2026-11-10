---
tags:
  - Character
  - Player
art: "[[PlaceholderCharacter.png]]"
playedBy: 
pronounced: 
aliases: 
titles: 
ancestry: 
heritage: 
gender: 
pronouns: 
sexuality: 
languages: 
occupation: []
organizations: []
religions: []
condition:
  - Healthy
currentLocation: []
whichParty: []
fc-date:
  year: "[null-*]"
birthday: -28
year: 
age: 836
publish: false
---

> [!infobox | no-blending black]+ <font color="#ffffff">Infobox</font>
> 
> `VIEW[!{art}][text(renderMarkdown)]`
> 
> ###### **Played By:** <font color="#ffc000">`VIEW[{playedBy}][text]`</font>
> 
> # Bio
> |  |  |
> |---|---|
> | **Aliases** | `VIEW[{aliases}][text]` |
> | **Titles** | `VIEW[{titles}][text]` |
> | **Ancestry** | `VIEW[{ancestry}][link]` |
> | **Heritage** | `VIEW[{heritage}][link]` |
> | **Gender** | `VIEW[{gender}]` |
> | **Pronouns** | `VIEW[{pronouns}]` |
> | **Sexuality** | `VIEW[{sexuality}]` |
> | **Age** | `VIEW[floor(({Vault Hub#time}-{birthday})/{Vault Hub#dpy})][:age]` yrs |
> 
> # Details
> |  |  |
> |---|---|
> | **Languages** | `VIEW[{languages}][link]` |
> | **Occupations** | `VIEW[{occupation}][text]` |
> | **Organizations** | `VIEW[{organizations}][link]` |
> | **Religions** | `VIEW[{religions}][link]` |
> | **Condition** | `VIEW[{condition}]` |
> | **Current Location** | `VIEW[{currentLocation}][link]` |

# `=this.file.name`

** *<center>"`VIEW[{pronounced}][text]`"</center>* **

## Database
 ![[Database - Character Note.base]]

## Ideals
### <font color="#9bbb59">Loves:</font>

### <font color="#c0504d">Hates:</font>

## Traits
### <font color="#9bbb59">Perks:</font>

### <font color="#c0504d">Flaws:</font>

## Present

### Goals

#### Short-Term:

#### Long-Term:

## Past
### Birth:

**Day** `INPUT[inlineSelect(option(1), option(2), option(3), option(4), option(5), option(6), option(7), option(8), option(9), option(10), option(11), option(12), option(13), option(14), option(15), option(16), option(17), option(18), option(19), option(20), option(21), option(22), option(23), option(24), option(25), option(26), option(27), option(28)):fc-date.day]` **Month** `INPUT[inlineSelect(option(1, Aurora),option(2, Novus), option(3, Iter), option(4, Florera), option(5, Tersus), option(6, Solis), option(7, Calor), option(8, Caelum), option(9, Visus), option(10, Messis), option(11, Cedrus), option(12, Tornu), option(13, Parago)):fc-date.month]` **Year** `INPUT[number(class(nb-mb-55)):year]` `VIEW[\[{year}-*\]][text(hidden):fc-date.year]` `VIEW[{Vault Hub#dpy}*{year}+{Vault Hub#dpm}*({fc-date.month}-1)+{fc-date.day}][math(hidden):birthday]`
- Birth Location: 
- Mother: | Father: 

### Childhood:

### Journey:

### Worship:

## Notes

[Player Handout](https://docs.google.com/document/d/1_eFTuK3teRJSAVbd2QSZxjDTgE_RZH54zZg-3Eoo4Hk/edit?usp=sharing)

