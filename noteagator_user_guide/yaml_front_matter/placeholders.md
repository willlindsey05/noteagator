---
description: How to use placeholders in notes
---
Placeholders let you define values in a note that can be dynamically replaced when printing the note.  

Placeholders are defined in the YAML frontmatter under the `placeholders` key.  Each placeholder is mapped to a short flag `i`, `j`, etc (run `ngt print --help` for full list).  
**Example**  
```yaml
---
description: Example using placeholders
placeholders:
  i: NAME
  j: ACTION
---
Hello, my name is NAME.
Today I will ACTION.

```
**Replacing placeholders at print time**  
```console
$ ngt print 2 -i Alice -j "learn Noteagator"
Hello, my name is Alice.
Today I will learn Noteagator.

```