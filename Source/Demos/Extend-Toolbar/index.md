---
layout : Default
---

# Demo : Extend Toolbar

This demo shows how to extend an existing toolbar.

<br/>

## Result

The demo code will add a new command into the `File` 
toolbar that when activated, will log a debug message.

<img height = 30 src = './Media/Toolbar.webp' />

<br/>

## Code

```txt
Source
└─ Manipulator.py   - Manipulator that modifies an existing toolbar.
└─ init_gui.py      - Setup code for creating and registering stuff.
└─ Command.py       - Command that logs a message on activation.
```

<br/>

## Pitfalls

Toolbars don't have Ids, they are addressed only by their name, this is problematic because names may change and thus break your code.

Depending on the toolbar you may have to specify a different names for different versions of FreeCAD.

<br/>