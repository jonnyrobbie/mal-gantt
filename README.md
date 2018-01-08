# Create Gantt charts from your MyAnimeList anime list.

Usage (most of it can be left default, the only required fields are `--open` and `--fontfile`):

```
$ ./mal_gantt.py --help
usage: mal_gantt.py [-h] [-v] [--bgcolour BGCOLOUR] [--barcolour BARCOLOUR]
                    [--dbarcolour DBARCOLOUR] [--wbarcolour WBARCOLOUR]
                    [--textcolour TEXTCOLOUR] [--glowcolour GLOWCOLOUR]
                    [--glow] [--mincolour MINCOLOUR] [--majcolour MAJCOLOUR]
                    [--lgridcolour LGRIDCOLOUR] -o OPEN [-s SAVE] [-p POINT]
                    [-f FONTFILE]

Render Gantt charts from exported MyAnimeList data...

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Verbose output.
  --bgcolour BGCOLOUR   Background colour.
  --barcolour BARCOLOUR
                        Finished bar colour.
  --dbarcolour DBARCOLOUR
                        Dropped bar colour.
  --wbarcolour WBARCOLOUR
                        Watching bar colour.
  --textcolour TEXTCOLOUR
                        Text colour.
  --glowcolour GLOWCOLOUR
                        Glow colour.
  --glow                Enable text glow.
  --mincolour MINCOLOUR
                        Minor (month) grid colour.
  --majcolour MAJCOLOUR
                        Major (year) grid colour.
  --lgridcolour LGRIDCOLOUR
                        Grid label colour.
  -o OPEN, --open OPEN  XML file downloaded and unpacked from MyAnimeList -
                        https://myanimelist.net/panel.php?go=export
  -s SAVE, --save SAVE  The final PNG file save location
  -p POINT, --point POINT
                        Font pointsize.
  -f FONTFILE, --fontfile FONTFILE
                        TTF or OTF font filename.
```

Example:

![](https://a.pomf.space/rlezmwuaztvi.png)
