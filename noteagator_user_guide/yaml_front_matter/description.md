---
description: How to add descriptions to notes
---
Notes can include optional YAML front matter, and one of the most useful keys is `description`.  

The `description` value appears when **listing** or **searching** your notes.  It helps you quickly understand what a note is about without opening it.  
 
**Example:**  
```yaml
---
description: This Note has a descripton
---
My note content goes here.
```
**How it appears in listings**  
```console
$ ngt ls -R
Notebook Directory: /
  1 📁 yaml_frontmatter
    2 📄 description.md  - How to add descriptions to notes
  3 📄 copy_code.md  - How to copy code
  4 📄 ngt_getting_started.md  - Adding YAML frontmatter
```
**How it appears in search**  
```console
$ ngt search front      
1 /ngt_getting_started.md  - Adding YAML frontmatter
2 /yaml_frontmatter/description.md  - How to add descriptions to notes
```
Descriptons are optional but highly recommended to keep your notes organized and easy to discover.  