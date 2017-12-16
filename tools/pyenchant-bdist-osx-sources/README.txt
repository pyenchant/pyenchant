
This directory contains a hacky little build script for the binary enchant
dependencies on OSX.  It compiles enchant with some patches to make it
better support relocatable execution.

In addition to enchant, we also ship some dependencies:

  * glib
  * gettext
  * pcre

These must be installed onto the build host using e.g. homebrew, and will be
copied into place as required.  You might like to do something like:

   brew reinstall glib gettext pcre --universal --build-bottle

In strict compliance with the LGPL, I will provide copies of the source for
these dependencies on request.  But I'm pretty sure everyone these days knows
how to find them on the internet...

