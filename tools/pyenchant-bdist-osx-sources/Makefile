#
#  Makefile for building pyenchant OSX dependencies.
#
BUILD_DIR = /Users/rfk/repos/pyenchant/tools/pyenchant-bdist-osx-sources/build
ENCHANT_DIR = enchant-1.6.0

CC = clang
CXX = clang++ 
CFLAGS =
CXXFLAGS = $(CFLAGS)
ENCHANT_CONFIG_OPTS = --enable-ispell --enable-myspell --disable-aspell --with-system-myspell=no
ENCHANT_CFLAGS = `pkg-config --cflags gmodule-2.0`
ENCHANT_LIBS = `pkg-config --libs gmodule-2.0`
LDFLAGS = -L$(BUILD_DIR)/lib


all: $(BUILD_DIR)/lib/libenchant.1.dylib $(BUILD_DIR)/share/enchant/myspell/en_GB.dic \
	$(BUILD_DIR)/share/enchant/myspell/en_US.dic $(BUILD_DIR)/share/enchant/myspell/de_DE.dic \
	$(BUILD_DIR)/share/enchant/myspell/en_AU.dic $(BUILD_DIR)/share/enchant/myspell/fr_FR.dic


$(BUILD_DIR)/lib/libenchant.1.dylib: $(ENCHANT_DIR)/Makefile
	cd $(ENCHANT_DIR) && make
	cd $(ENCHANT_DIR) && make install


$(ENCHANT_DIR)/Makefile:
	rm -rf $(ENCHANT_DIR)
	tar -xzvf src/$(ENCHANT_DIR).tar.gz
	patch $(ENCHANT_DIR)/src/enchant.c < patches/relocatable.patch
	patch $(ENCHANT_DIR)/src/enchant.c < patches/prefixdir_c.patch
	patch $(ENCHANT_DIR)/src/enchant.h < patches/prefixdir_h.patch
	cd $(ENCHANT_DIR) && ./configure CC=$(CC) CXX=$(CXX) CFLAGS="$(CFLAGS)" CXXFLAGS="$(CXXFLAGS)" LDFLAGS=$(LDFLAGS) ENCHANT_CFLAGS="$(ENCHANT_CFLAGS)" ENCHANT_LIBS="$(ENCHANT_LIBS)" $(ENCHANT_CONFIG_OPTS) --prefix=$(BUILD_DIR);


$(BUILD_DIR)/share/enchant/myspell/%.dic: $(BUILD_DIR)/share/enchant/myspell/%.zip
	cd $(BUILD_DIR)/share/enchant/myspell && unzip -n `basename $<` '*.dic' '*.aff'


clean:
	rm -fr $(ENCHANT_DIR)*

clobber: clean
	rm -rf $(BUILD_DIR)/lib
	rm -rf $(BUILD_DIR)/bin
	rm -rf $(BUILD_DIR)/include
	for FN in `ls $(BUILD_DIR)/share`; do if [ $$FN != "enchant" ]; then rm -r $(BUILD_DIR)/share/$$FN; fi; done;
	rm -f $(BUILD_DIR)/share/enchant/enchant.ordering
	rm -f $(BUILD_DIR)/share/enchant/myspell/*.dic
	rm -f $(BUILD_DIR)/share/enchant/myspell/*.aff
	rm -f $(BUILD_DIR)/share/enchant/myspell/*.txt

