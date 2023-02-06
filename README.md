# gtk-app-builder
Distribute your Gtk app on Mac as an App

# Requirements
* **working binary** -- already compiled
* **Info.plist** -- for your app
* **Python3** -- this tool is written in Python3
* **Mac Pro** -- not sure if this will work on Mac Air

# How to use gtp-app-builder
As of current, I only have the script that will copy all dependencies of your working binary.

on Terminal, type in:

`python3 copylib.py yourapp`

This will create `copylib_yourapp.sh`, which has to be run at a specific folder (for no reason other than script is WIP):

<pre>APP
 +-> MacOS/yourapp
 +-> Resources
   +-> bin/copylib_yourapp.sh
   +-> lib/{gtk_libs_will_be_copied_here}</pre>

With above directory structure, run **copylib_yourapp.sh** on Terminal.

All dependency libraries should be copied to `Resources/lib/{here}`

# Conclusion
It's not a lot for now but I plan to update the script into one click App builder for Mac, that would make it easy to integrate in CI/CD pipeline
