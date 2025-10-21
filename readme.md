# BINGYFLEA
A discord bot and associated codebase used to support [bingosync](https://bingosync.com/) and [lockout.live](https://lockout.live/) silksong play.

## Format specs

Types:
"craft", "flea", "key", "tool", "melody", "quest", "locket", "upgrade", "fight", "npc", "location", "collection", "relic", "hardsave"

Progression:
"early", "dash", "cloak", "walljump", "act2", "clawline", "feydown"

For ranges:
"{{X}} Memory Lockets" with a "range" : [1,2,5] can be any of the following goals:
1 Memory Lockets
2 Memory Lockets
5 Memory Lockets
These are automatically exclusive, and the group can be added to an exclusive pool using the string with {{X}} in it.