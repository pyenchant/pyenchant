#
#  Makefile for building pyenchant win32 dependencies.
#
BUILD_DIR = /Users/rfk/software/pyenchant/tools/pyenchant-bdist-osx-sources/build
MACPORTS_DIR = /opt/local/
ENCHANT_DIR = enchant-1.6.0
GLIB_DIR = glib-2.24.1
GETTEXT_DIR = gettext-0.18.1.1
ICONV_DIR = libiconv-1.13.1

BUILD_SDK = /Developer/SDKs/MacOSX10.4u.sdk

CC = gcc-4.0
CXX = g++-4.0
CFLAGS = -isysroot $(BUILD_SDK) -mmacosx-version-min=10.4 -fexceptions -I$(BUILD_DIR)/include
CXXFLAGS = $(CFLAGS)
105_CFLAGS = -isysroot /Developer/SDKs/MacOSX10.5.sdk -mmacosx-version-min=10.5 -fexceptions -I$(BUILD_DIR)/include
105_CXXFLAGS = $(105_CFLAGS)
ENCHANT_CONFIG_OPTS = --enable-ispell --enable-myspell --disable-aspell --with-system-myspell=no
ENCHANT_CFLAGS = `pkg-config --cflags gmodule-2.0` -fexceptions
ENCHANT_LIBS = `pkg-config --libs gmodule-2.0`
LDFLAGS = -L$(BUILD_DIR)/lib

all: $(BUILD_DIR)/lib/libenchant.1.dylib $(BUILD_DIR)/share/enchant/myspell/en_GB.dic \
	$(BUILD_DIR)/share/enchant/myspell/en_US.dic $(BUILD_DIR)/share/enchant/myspell/de_DE.dic \
	$(BUILD_DIR)/share/enchant/myspell/en_AU.dic $(BUILD_DIR)/share/enchant/myspell/fr_FR.dic

#  Make enchant as a universal binary.
$(BUILD_DIR)/lib/libenchant.1.dylib: $(ENCHANT_DIR).i386/src/.libs/libenchant.1.dylib $(ENCHANT_DIR).ppc/src/.libs/libenchant.1.dylib $(ENCHANT_DIR).x86_64/src/.libs/libenchant.1.dylib
	lipo -create -arch i386 $(ENCHANT_DIR).i386/src/.libs/libenchant.1.dylib -arch ppc $(ENCHANT_DIR).ppc/src/.libs/libenchant.1.dylib -arch x86_64 $(ENCHANT_DIR).x86_64/src/.libs/libenchant.1.dylib -output $(BUILD_DIR)/lib/libenchant.1.dylib
	mkdir -p $(BUILD_DIR)/lib/enchant
	lipo -create -arch i386 $(ENCHANT_DIR).i386/src/ispell/.libs/libenchant_ispell.so -arch ppc $(ENCHANT_DIR).ppc/src/ispell/.libs/libenchant_ispell.so -arch x86_64 $(ENCHANT_DIR).x86_64/src/ispell/.libs/libenchant_ispell.so -output $(BUILD_DIR)/lib/enchant/libenchant_ispell.so
	lipo -create -arch i386 $(ENCHANT_DIR).i386/src/myspell/.libs/libenchant_myspell.so -arch ppc $(ENCHANT_DIR).ppc/src/myspell/.libs/libenchant_myspell.so -arch x86_64 $(ENCHANT_DIR).x86_64/src/myspell/.libs/libenchant_myspell.so -output $(BUILD_DIR)/lib/enchant/libenchant_myspell.so


$(ENCHANT_DIR).%/src/.libs/libenchant.1.dylib: $(ENCHANT_DIR).%/Makefile
	cp $(BUILD_DIR)/lib/glib-2.0/include/glibconfig.$*.h $(BUILD_DIR)/lib/glib-2.0/include/glibconfig.h
	cd $(ENCHANT_DIR).$* && MACOSX_DEPLOYMENT_TARGET=10.4 make

$(ENCHANT_DIR).%/Makefile:  $(BUILD_DIR)/lib/libglib-2.0.0.dylib
	rm -rf $(ENCHANT_DIR).$*
	tar -xzvf src/$(ENCHANT_DIR).tar.gz
	patch $(ENCHANT_DIR)/src/enchant.c < patches/relocatable.patch
	patch $(ENCHANT_DIR)/src/enchant.c < patches/prefixdir_c.patch
	patch $(ENCHANT_DIR)/src/enchant.h < patches/prefixdir_h.patch
	cd $(ENCHANT_DIR) && if [ $* = "x86_64" ]; then export PKG_CONFIG_PATH=$(BUILD_DIR)/lib/pkgconfig && ./configure CC=$(CC) CXX=$(CXX) CFLAGS="$(105_CFLAGS) -arch $*" CXXFLAGS="$(105_CXXFLAGS) -arch $*" LDFLAGS=$(LDFLAGS) ENCHANT_CFLAGS="$(ENCHANT_CFLAGS) -arch $*" ENCHANT_LIBS="$(ENCHANT_LIBS) -arch $*" $(ENCHANT_CONFIG_OPTS) --prefix=$(BUILD_DIR); else export PKG_CONFIG_PATH=$(BUILD_DIR)/lib/pkgconfig && ./configure CC=$(CC) CXX=$(CXX) CFLAGS="$(CFLAGS) -arch $*" CXXFLAGS="$(CXXFLAGS) -arch $*" LDFLAGS=$(LDFLAGS) ENCHANT_CFLAGS="$(ENCHANT_CFLAGS) -arch $*" ENCHANT_LIBS="$(ENCHANT_LIBS) -arch $*" $(ENCHANT_CONFIG_OPTS) --prefix=$(BUILD_DIR); fi
	mv $(ENCHANT_DIR) $(ENCHANT_DIR).$*


#  Make glib as a universal binary.
$(BUILD_DIR)/lib/libglib-2.0.0.dylib: $(GLIB_DIR).i386/glib/.libs/libglib-2.0.0.dylib $(GLIB_DIR).ppc/glib/.libs/libglib-2.0.0.dylib $(GLIB_DIR).x86_64/glib/.libs/libglib-2.0.0.dylib
	lipo -create -arch i386 $(GLIB_DIR).i386/glib/.libs/libglib-2.0.0.dylib -arch ppc $(GLIB_DIR).ppc/glib/.libs/libglib-2.0.0.dylib -arch x86_64 $(GLIB_DIR).x86_64/glib/.libs/libglib-2.0.0.dylib -output $(BUILD_DIR)/lib/libglib-2.0.0.dylib
	lipo -create -arch i386 $(GLIB_DIR).i386/gmodule/.libs/libgmodule-2.0.0.dylib -arch ppc $(GLIB_DIR).ppc/gmodule/.libs/libgmodule-2.0.0.dylib -arch x86_64 $(GLIB_DIR).x86_64/gmodule/.libs/libgmodule-2.0.0.dylib -output $(BUILD_DIR)/lib/libgmodule-2.0.0.dylib


$(GLIB_DIR).%/glib/.libs/libglib-2.0.0.dylib: $(GLIB_DIR).%/Makefile
	cd $(GLIB_DIR).$* && MACOSX_DEPLOYMENT_TARGET=10.4 make
	cd $(GLIB_DIR).$* && MACOSX_DEPLOYMENT_TARGET=10.4 make install
	cp $(BUILD_DIR)/lib/glib-2.0/include/glibconfig.h $(BUILD_DIR)/lib/glib-2.0/include/glibconfig.$*.h

$(GLIB_DIR).%/Makefile: $(BUILD_DIR)/lib/libintl.8.dylib $(BUILD_DIR)/lib/libiconv.2.dylib 
	rm -rf $(GLIB_DIR).$*
	tar -xjvf src/$(GLIB_DIR).tar.bz2
	cd $(GLIB_DIR) && if [ $* = "x86_64" ]; then ./configure CC=$(CC) LDFLAGS="$(LDFLAGS)" CFLAGS="$(105_CFLAGS) -arch x86_64" --prefix=$(BUILD_DIR); else ./configure CC=$(CC) LDFLAGS="$(LDFLAGS)" CFLAGS="$(CFLAGS) -arch $*" --prefix=$(BUILD_DIR); fi
	mv $(GLIB_DIR) $(GLIB_DIR).$*


#  Make libiconv as a universal binary.
$(BUILD_DIR)/lib/libiconv.2.dylib: $(ICONV_DIR)/Makefile
	cd $(ICONV_DIR) && MACOSX_DEPLOYMENT_TARGET=10.4 make
	cd $(ICONV_DIR) && MACOSX_DEPLOYMENT_TARGET=10.4 make install

$(ICONV_DIR)/Makefile: 
	rm -rf $(ICONV_DIR)
	tar -xzvf src/$(ICONV_DIR).tar.gz
	cd $(ICONV_DIR) && ./configure CC=$(CC) CXX=$(CXX) LDFLAGS="$(LDFLAGS)" CFLAGS="$(CFLAGS) -arch i386 -arch ppc -arch x86_64" CXXFLAGS="$(CXXFLAGS) -arch i386 -arch ppc -arch x86_64" --prefix=$(BUILD_DIR)


#  Make libintl as a universal binary.
$(BUILD_DIR)/lib/libintl.8.dylib: $(GETTEXT_DIR)/Makefile
	cd $(GETTEXT_DIR) && MACOSX_DEPLOYMENT_TARGET=10.4 make
	cd $(GETTEXT_DIR) && MACOSX_DEPLOYMENT_TARGET=10.4 make install

$(GETTEXT_DIR)/Makefile: 
	rm -rf $(GETTEXT_DIR)
	tar -xzvf src/$(GETTEXT_DIR).tar.gz
	cd $(GETTEXT_DIR) && ./configure CC=$(CC) CXX=$(CXX) LDFLAGS="$(LDFLAGS)" CFLAGS="$(CFLAGS) -arch i386 -arch ppc -arch x86_64" CXXFLAGS="$(CXXFLAGS) -arch i386 -arch ppc -arch x86_64" --prefix=$(BUILD_DIR)


# Ability to extract MySpell dictionary files
$(BUILD_DIR)/share/enchant/myspell/%.dic: $(BUILD_DIR)/share/enchant/myspell/%.zip
	cd $(BUILD_DIR)/share/enchant/myspell && unzip -n `basename $<` '*.dic' '*.aff'


clean:
	rm -fr $(ENCHANT_DIR)*
	rm -fr $(ICONV_DIR)*
	rm -fr $(GETTEXT_DIR)*
	rm -fr $(GLIB_DIR)*

clobber: clean
	rm -rf $(BUILD_DIR)/lib
	rm -rf $(BUILD_DIR)/bin
	rm -rf $(BUILD_DIR)/include
	for FN in `ls $(BUILD_DIR)/share`; do if [ $$FN != "enchant" ]; then rm -r $(BUILD_DIR)/share/$$FN; fi; done;
	rm -f $(BUILD_DIR)/share/enchant/myspell/*.dic
	rm -f $(BUILD_DIR)/share/enchant/myspell/*.aff
	rm -f $(BUILD_DIR)/share/enchant/myspell/*.txt

