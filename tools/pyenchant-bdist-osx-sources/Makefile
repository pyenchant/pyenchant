#
#  Makefile for building pyenchant win32 dependencies.
#
BUILD_DIR = ./build
MACPORTS_DIR = /opt/local/
ENCHANT_DIR = enchant-1.6.0

CFLAGS = -mmacosx-version-min=10.4 -fexceptions
CXXFLAGS = -mmacosx-version-min=10.4 -fexceptions
ENCHANT_CONFIG_OPTS = --enable-ispell --enable-myspell --disable-aspell --with-system-myspell=no --disable-binreloc
ENCHANT_CFLAGS = `pkg-config --cflags gmodule-2.0` -fexceptions -DENABLE_BINRELOC
ENCHANT_LIBS = `pkg-config --libs gmodule-2.0` -L`pwd`/$(BUILD_DIR)

all: $(BUILD_DIR)/lib/libenchant.1.dylib $(BUILD_DIR)/share/enchant/myspell/en_GB.dic \
	$(BUILD_DIR)/share/enchant/myspell/en_US.dic $(BUILD_DIR)/share/enchant/myspell/de_DE.dic \
	$(BUILD_DIR)/share/enchant/myspell/en_AU.dic $(BUILD_DIR)/share/enchant/myspell/fr_FR.dic

#  Make enchant as a universal binary.
$(BUILD_DIR)/lib/libenchant.1.dylib: $(ENCHANT_DIR).i386/src/.libs/libenchant.1.dylib $(ENCHANT_DIR).x86_64/src/.libs/libenchant.1.dylib $(ENCHANT_DIR).ppc/src/.libs/libenchant.1.dylib
	lipo -create -arch i386 $(ENCHANT_DIR).i386/src/.libs/libenchant.1.dylib -arch x86_64 $(ENCHANT_DIR).x86_64/src/.libs/libenchant.1.dylib -arch ppc $(ENCHANT_DIR).ppc/src/.libs/libenchant.1.dylib -output $(BUILD_DIR)/lib/libenchant.1.dylib
	mkdir -p $(BUILD_DIR)/lib/enchant
	lipo -create -arch i386 $(ENCHANT_DIR).i386/src/ispell/.libs/libenchant_ispell.so -arch x86_64 $(ENCHANT_DIR).x86_64/src/ispell/.libs/libenchant_ispell.so -arch ppc $(ENCHANT_DIR).ppc/src/ispell/.libs/libenchant_ispell.so -output $(BUILD_DIR)/lib/enchant/libenchant_ispell.so
	lipo -create -arch i386 $(ENCHANT_DIR).i386/src/myspell/.libs/libenchant_myspell.so -arch x86_64 $(ENCHANT_DIR).x86_64/src/myspell/.libs/libenchant_myspell.so -arch ppc $(ENCHANT_DIR).ppc/src/myspell/.libs/libenchant_myspell.so -output $(BUILD_DIR)/lib/enchant/libenchant_myspell.so
	PYTHONPATH=../../ python -c "import enchant.utils; enchant.utils.osx_make_dist_libraries('$(BUILD_DIR)/lib')"


$(ENCHANT_DIR).%/src/.libs/libenchant.1.dylib: $(ENCHANT_DIR).%/Makefile
	cd $(ENCHANT_DIR).$* && MACOSX_DEPLOYMENT_TARGET=10.4 make

$(ENCHANT_DIR).%/Makefile: 
	rm -rf $(ENCHANT_DIR).$*
	tar -xzvf src/$(ENCHANT_DIR).tar.gz
	patch $(ENCHANT_DIR)/src/enchant.c < patches/relocatable.patch
	patch $(ENCHANT_DIR)/src/enchant.c < patches/prefixdir_c.patch
	patch $(ENCHANT_DIR)/src/enchant.h < patches/prefixdir_h.patch
	cd $(ENCHANT_DIR) && ./configure CFLAGS="$(CFLAGS) -arch $*" CXXFLAGS="$(CXXFLAGS) -arch $*" ENCHANT_CFLAGS="$(ENCHANT_CFLAGS) -arch $*" ENCHANT_LIBS="$(ENCHANT_LIBS) -arch $*" $(ENCHANT_CONFIG_OPTS)
	mv $(ENCHANT_DIR) $(ENCHANT_DIR).$*


# Ability to extract MySpell dictionary files
$(BUILD_DIR)/share/enchant/myspell/%.dic: $(BUILD_DIR)/share/enchant/myspell/%.zip
	cd $(BUILD_DIR)/share/enchant/myspell && unzip -n `basename $<` '*.dic' '*.aff'


clean:
	rm -fr $(ENCHANT_DIR).*

clobber: clean
	rm -f $(BUILD_DIR)/lib/*.dylib
	rm -rf $(BUILD_DIR)/lib/enchant
	rm -f $(BUILD_DIR)/share/enchant/myspell/*.dic
	rm -f $(BUILD_DIR)/share/enchant/myspell/*.aff
	rm -f $(BUILD_DIR)/share/enchant/myspell/*.txt

