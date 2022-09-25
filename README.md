# Notes Master UCM Technology & Photonics.

## Reminder

These notes are relevant with respect to some material and programming part of those courses, they are not reflections of the content of these courses and should not be use to evaluate them in any way.

The courses are in Spanish, so there will be some translation lag to standard technical language in English, and in some parts there may be some Spanish words used.

## External resources

All external resources can't be uploaded here, when possible there will be a reference to it.

## Start

Install [pre-commit](https://pre-commit.com), then run `pre-commit install` on the base of this project. Then, run `pre-commit run --all-files` to make sure it is not throwing errors. (We are using [pre-commit.ci](https://pre-commit.ci) to run these checks when you create a PR)

This project is meant to be carried out within VS Code. It should start by getting `workspace/workspace.code-workspace` opened on vscode.




## Build

The goal is to have some automations run on *individual courses* . For that purpose we will hope to use github actions that only apply when changes are made on a certain folder.`


## Working with LaTeX on VS Code

Latex Workshop uses the latexindent script for formatting. That is a perl script that requires a couple extra packages installed.

You need to install the dependecies it is missing. For that, I am running:

```
 perl -MCPAN -e 'install "File::HomeDir"'
 perl -MCPAN -e 'install "Unicode:GCString"'
```
But on your system it might be different, understand what it is missing by looking at the error through by `latexindent`, which will most likely include something like "Can't locate File/HomeDir.pm in @INC" but, inste

### Too much effort

It takes too much effort to get it to work

These are the settings I arrived at, and they are still useless
```
# From https://ctan.javinator9889.com/support/latexindent/documentation/latexindent.pdf
specialBeginEnd:
  path:
    begin: '\\path'
    end: ";"
  specialBeforeCommand: 1

lookForAlignDelims:
  path:
    delimiterRegEx: '(edge|node\h*\{[0-9,A-Z]+\})'
indentAfterItems:
  tikzpicture: 1
indentAfterItems:
   tikzpicture: 1
itemNames:
    path: 1
    node: 0
    draw: 1
```
