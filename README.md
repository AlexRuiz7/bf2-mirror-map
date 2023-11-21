#  Battlefield 2 map mirroring tool

Battlefield 2 modding tool. Mirrors objects inside a .con file

This program mirrors the objects in the map (flips content vertical and horizontally).

The algorithm procedure is the following:

```python
   reads filename from commandline
   if file exists, then
       creates file: filename_mirror
       for line in file
           if (line contains ".absolutePosition"), then
               mirror (line)
           elif (line contains ".rotation"), then
               line.X += 180
           endif
           write line into filename_mirror
       endfor


   func mirror(string line)
       line.X = -line.X
       line.Z = -line.Z
```

It can process several files in a time:
```python
python __mirror.py StaticObjects.con AmbientObjects.con Editor\Splines.con Editor\GamePlayObjects.con
```
