#
#  Makefile for building pyenchant win32 dependencies.
#
BUILD_DIR = /s/software/pyenchant/tools/pyenchant-bdist-win32-sources/build
ENCHANT_DIR = enchant-1.5.0

ENCHANT_CONFIG_OPTS = --enable-ispell --enable-myspell --disable-aspell
ENCHANT_CFLAGS = -I$(BUILD_DIR)/include/glib-2.0
ENCHANT_LIBS = -L$(BUILD_DIR)/lib -lglib-2.0-0 -lgmodule-2.0-0

all: $(BUILD_DIR)/lib/libenchant.dll $(BUILD_DIR)/myspell/en_GB.dic \
	$(BUILD_DIR)/myspell/en_US.dic $(BUILD_DIR)/myspell/de_DE.dic \
	$(BUILD_DIR)/myspell/en_AU.dic $(BUILD_DIR)/myspell/fr_FR.dic

#  Make enchant.
$(BUILD_DIR)/lib/libenchant.dll: $(ENCHANT_DIR)/Makefile
	cd $(ENCHANT_DIR) && make
	cp $(ENCHANT_DIR)/src/.libs/libenchant-1.dll $(BUILD_DIR)/lib/
	mkdir -p $(BUILD_DIR)/lib/enchant
	cp $(ENCHANT_DIR)/src/ispell/.libs/libenchant_ispell.dll $(BUILD_DIR)/lib/enchant/
	cp $(ENCHANT_DIR)/src/myspell/.libs/libenchant_myspell.dll $(BUILD_DIR)/lib/enchant/

$(ENCHANT_DIR)/Makefile: src/$(ENCHANT_DIR).tar.gz
	rm -rf $(ENCHANT_DIR)
	tar -xzvf src/$(ENCHANT_DIR).tar.gz
	patch $(ENCHANT_DIR)/src/pwl.c < patches/pwl.patch
	cd $(ENCHANT_DIR) && ./configure CFLAGS="$(CFLAGS)" ENCHANT_CFLAGS="$(ENCHANT_CFLAGS)" ENCHANT_LIBS="$(ENCHANT_LIBS)" $(ENCHANT_CONFIG_OPTS)


# Ability to extract MySpell dictionary files
$(BUILD_DIR)/myspell/%.dic: $(BUILD_DIR)/myspell/%.zip
	cd $(BUILD_DIR)/myspell && unzip -n $< '*.dic' '*.aff'


clean:
	rm -fr $(ENCHANT_DIR)

clobber: clean
	rm -f $(BUILD_DIR)/lib/libenchant*
	rm -rf $(BUILD_DIR)/lib/enchant
	rm -f $(BUILD_DIR)/myspell/*.dic
	rm -f $(BUILD_DIR)/myspell/*.aff
	rm -f $(BUILD_DIR)/myspell/*.txt

