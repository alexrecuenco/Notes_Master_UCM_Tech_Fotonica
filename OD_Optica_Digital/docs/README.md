# Notes 

- Note Author: Alejandro Gonzalez Recuenco



- Course by  (UCM)

## Requirements

It requires a full tex live installation, or similar.

It additionally requires that you install the tools required by the `minted` package, that is, `Pygments.`

For that, install python3 and run:

    $	pip install pygments

## How to build

**Careful,** *the build process requires `shell-escape`, that allows arbitrary code execution. Do that at your own risk. (If someone modifies these files, they could execute malicious software on your computer)*

Building the document is achieved by going to the folder where build is and running:

    $	./build 
    
In mac you can then open the file with 

    $	open main.pdf


