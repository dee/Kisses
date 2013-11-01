Kisses
======

Sublime Text 3 plugin for Hugs98. 

Supports the following functions:

* `ctrl+h, ctrl+t` - Type information for symbol under cursor or selected text; similar to `:t` interpreter command;
* `ctrl+h, ctrl+i` - History of the "Type information" command;
* `ctrl+h, ctrl+h` - Query Hoogle about symbol under cursor or selected text;
* More to come...

It also includes popup menu extension.

Installation
------------

Simply copy this directory contents to <sublime_package_directory>/Data/Packages/Kisses.

Configuration
-------------

At this point plugin supports the following settings:

* `hugs_root` - on Windows, set this to the base Hugs98 directory, e.g. C:\Program Files (x86)\WinHugs. Plugin tries to find a Hugs installation automatically, and if fails, it uses this setting.
