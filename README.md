# Notebook Navigator (noteagator)

Notebook Navigator (noteagator) helps you organize, browse, and print collections of plain Markdown notes.  
It's built for zero lock-in and a **keyboard-first** workflow, letting you replace text, copy code, and navigate your notes entirely without the mouse.  

## install

```
# recommended
pipx install noteagator

# or with pip
pip install noteagator

```
Verify:
```
ngt --help
```
### Debian Users Need xclip
Debian based Linux users will also need to install xclip to use `code-copy` feature.  
```
sudo apt-get install xclip
```
## Quick Start (2 minutes)
1) **Open your notebook directory in an editor**  

        code -n "$(ngt show-base)"
  
2) **Create a note (any `.md` file under your notebook base)**  

        ---
        description: This is an example note
        placeholders:
            i: foo
        format: slim
        ---
        My Command
        ```
        echo 'foo'
        ```
3) **List Notes**  

        $ ngt ls
        Notebook Directory: /
        1 📄 example.md  - This is an example note
4) **Print with replacement and copy code**
Replace placeholder `i` with `bar` and copy the first code block to your clipboard: 

        $ ngt print 1 -i 'bar' -c 1
        description: This is an example note
        format: slim
        note: /home/user/.noteagator/notebook/example.md
        placeholders:
        i: foo
        ---
        My Command
        --copy 1 $ echo 'bar'
    Your clipboard now contains:

        echo 'bar'

## Core Concepts
* **Notebook Base** - The root directory Noteagator treats as your notebook.  
Set it:

        ngt set-base /path/to/your/notebook
    Show it:

        ngt show-base
* **Placeholders (YAML front matter)** - Declare keys you can swap at print time:  
Run `ngt print --help` for a list of valid placeholders keys.  

        ---
        placeholders:
          i: foo
          d: world
        ---
    Then:  

        ngt print 3 -i 'bar' -j 'team'
* Formats  
`ngt print` can render "slim" (great for large notes) or "markdown".  

        ngt print 2 --format markdown
* **Copy-Code**  
`-c N` copies the Nth fenced code block from the printed note to your clipboard, no mouse needed.  

## Common Commands (Cheat Sheet)
```
# set / view notebook
ngt set-base /path/to/notebook
ngt show-base

# explore
ngt ls            # list notes in current directory
ngt ls -R         # list recursively
ngt search netcat # Search Notes for netcat

# print & replace
ngt print 7             # print note #7
ngt print 7 -i value    # replace placeholder 'i'
ngt print 7 -i one -j two --format markdown

# copy code
ngt print 7 -c 1        # copy first code block to clipboard

```
## User Guide
This repo includes a full user guide you can use as your notebook while learning.  
```
$ ngt set-base noteagator/noteagator_user_guide 
$ ngt ls -R                                    
Notebook Directory: /
  1 📁 navigation
    2 📄 1.base.md  - How to define your notebook
    3 📄 2.edit.md  - How to create/edit notes
    4 📄 3.ls.md  - How to list notes
    5 📄 4.cd.md  - How to change directories in a notebook.
  6 📁 printing_notes
    7 📄 1.print.md  - How to print notes
    8 📄 2.copy.md  - How to copy code snipts
    9 📄 3.replace.md  - How to replace placeholders
    10 📄 4.format.md  - How to control print format
  11 📁 yaml_front_matter
    12 📄 description.md  - How to add descriptions to notes
    13 📄 format.md  - How to define note format
    14 📄 placeholders.md  - How to use placeholders in notes
```

## Troubleshooting
* "**No Notes Found**"  
Make sure your notebook base is set to a directory that actually contains `.md` files:  

        ngt show-base
        ngt set-base /correct/path
* **Clipboard didn't change with `-c`**  
Re-run with `-c 1` and confirm the printed note actually has a fenced code block.
(If your OS needs clipboard tooling, install one: xclip/xsel on some Linux setups.)
* **Placeholders not replaced**
Ensure your front matter has a `placeholders:` map and the key you're passing (like `-i`) exists.  

