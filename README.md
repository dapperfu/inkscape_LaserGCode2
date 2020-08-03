# Inkscape Laser GCode

[J Tech Photonics, Inc's Inkscape Laser Plug-in Updated](https://jtechphotonics.com/?page_id=2012) for Inkscape v1.0 & Targeting GRBL.

GCodetools (included with Inkscape) is more full featured. This is a quick way to 

Toolchain/Stack for laserin stuff:

1. Inkscape.
1. [inkscape_HatchFill2](https://github.com/dapperfu/inkscape_HatchFill2/)
1. [inkscape_LaserGCode2](https://github.com/dapperfu/inkscape_LaserGCode2)
1. [python_grbl](https://github.com/dapperfu/python_grbl)
    ```grblcli run <example.ngc>```


# Installation:

## Generic

1. Download https://github.com/dapperfu/inkscape_HatchFill2/archive/master.zip
2. Extract to Directory in ```Edit > Preferences > System: User``` (Shift-Ctrl-P)
  ![](.img/extension_dir.png)

### Linux

    mkdir -p ~/.config/inkscape/extensions/
    git clone https://github.com/dapperfu/inkscape_HatchFill2.git ~/.config/inkscape/extensions/inkscape_HatchFill2
    
### MacOS

**TODO**

### Windows

**TODO**

## Usage:

- Launch Inkscape v1.0>
- Extensions > gh:dapperfu > Laser GCode 2
   - Alt-n + d + l

# Debugging / Development

Clone [inkscape_ExtensionDevTools](https://github.com/dapperfu/inkscape_ExtensionDevTools/) into the inkscape_LaserGCode2 folder.

    git clone https://github.com/dapperfu/inkscape_ExtensionDevTools.git ~/.config/inkscape/extensions/inkscape_HatchFill2/

1. Open "inkscape_LaserGCode2" in Inkscape & Run the extension.
2. A ```debug``` directory will be created in the Hatch Fill 2 extension directory.
   1. ```laser2.debug``` - Summary of how the extension was called
   2. ```laser2.sh``` - Shell script to programmatically run the extension.
   3. ```laser2_run.py``` - Python script to programmatically run the extension.
     (Useful for debugging in Spyder3/VSCode)
   4. ```input_file.svg``` - Copy of the input SVG file.


# Issues 

https://github.com/dapperfu/inkscape_LaserGCode2/issues

Tested on Ubuntu 20.04 & ```inkscape 1.0+r73+1~ubuntu20.04.1```
