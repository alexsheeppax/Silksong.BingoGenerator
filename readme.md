# BINGYFLEA
A discord bot and associated codebase used to support [bingosync](https://bingosync.com/) and [lockout.live](https://lockout.live/) silksong play.

The up-to-date lockout.live and bingosync files live in assets/generated/.

## Commands
Add the bot to your user account or server via [this link!](https://discord.com/oauth2/authorize?client_id=1429591758248874105)

- newboard

Very simple command that spits out a Bingosync-formatted list. Set the game to Custom (Advanced) and the variant to "Fixed Board" to use.

- advancedboard

Command that allows exclusion of arbitrary tags (types and/or progression) from goals. Ex: `flea, key, faydown` would generate a board without any flea goals, no simple key requirements, and no faydown cloak requirements.

## Goal contribution
The current list of goals is "categorized_v3.json" in the Assets folder. To add a goal or exclusion, add any necessary lines in the relevant sections in that file.

### Format specs

Types:
"craft", "flea", "key", "tool", "melody", "quest", "locket", "upgrade", "fight", "npc", "location", "collection", "relic", "hardsave"

Progression:
"early", "dash", "cloak", "walljump", "act2", "clawline", "faydown"

Weights:
If not given, a weight is assumed to be 1. A weight of 2 means a goal is twice as likely to be picked. This can be a decimal if you really want that kind of granularity. **Only applies to the /newboard BingyFlea command.**

For ranges:
"{{X}} Memory Lockets" with a "range" : [1,2,5] can be any of the following goals:
1 Memory Lockets
2 Memory Lockets
5 Memory Lockets
These are automatically exclusive, and the group can be added to an exclusive pool using the string with {{X}} in it.