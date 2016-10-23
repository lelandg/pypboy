pypboy
======

***Warning:*** This project is non-functional and requires special hardware.<br>
***However:*** The drop-in replacement for RPi.GPIO (pypboy.gpio) is working with two multiplexers, giving (at least)
16 additional "GPIO pins" that you can use at the cost of between 6 and 8 actual pins. (Depending on how many channels
you use.<br>
You can pull this module out and use it by itself if you'd prefer. Please just give me and the other authors credit
(by branching this project, or simply giving credit in the files).
Channel addressing pins are binary, so with 3 pins you can go 3^2 or 9 multiplexed pins and only multiplexed 4 pins for
2-channel addressing (2^2 = 4)<br>
You may have an easier time if you start with the original project here:
 https://github.com/sabas1080/pypboy

---
Remember that one Python Pip-Boy 3000 project? Neither do we!<br>
Python/Pygame interface, emulating that of the Pipboy-3000.<br> 
* Uses OSM for map data and has been partially tailored to respond to physical switches over Raspberry Pi's GPIO<br>
* Note: Boogieman (lelandg) changed everything around to get this to run on an RPi 2 **and**
to add support for multiplexers (up to two at this time)
* Works with Screen TFT 2.8" Capacitive of Adafruit<br>


* By Boogieman of Section9.space Hackerspace - added support for multiplexer and "GPIO HAL".<br> My changes are completely unsupported and require custom hardware.
* By Sabas of The Inventor's House Hackerspace modifications of GPS and Mapillary<br>
* By grieve work original<br>

Contribuyendo a este programa se da la bienvenida con gusto.<br>

Contributing to this software is warmly welcomed. You can do this basically by<br>

Please consider forking from the original repository if you do not need a multiplexer.
 The most current (as-of this writing) is located here:
 https://github.com/sabas1080/pypboy
 Changes made by aBoogieman are suspect, at best, and highly contagious, at worst!

 [forking](https://help.github.com/articles/fork-a-repo), committing modifications and then [pulling requests](https://help.github.com/articles/using-pull-requests) (follow the links above<br>
 for operating guide). Adding change log and your contact into file header is encouraged.

Thanks for your contributions!

Enjoy!
