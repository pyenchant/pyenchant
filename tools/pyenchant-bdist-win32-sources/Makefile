
BUILD_DIR = /home/rfk/pyenchant/tools/pyenchant-bdist-win32-sources/build
ENCHANT_DIR = enchant-1.4.0

ENCHANT_CONFIG_OPTS = --enable-ispell --enable-myspell --disable-aspell

CFLAGS = -Wl,--enable-runtime-pseudo-reloc

all: $(BUILD_DIR)/lib/libenchant.dll $(BUILD_DIR)/myspell/en_GB.dic \
	$(BUILD_DIR)/myspell/en_US.dic $(BUILD_DIR)/myspell/de_DE.dic \
	$(BUILD_DIR)/myspell/en_AU.dic $(BUILD_DIR)/myspell/fr_FR.dic

#  Make enchant.
$(BUILD_DIR)/lib/libenchant.dll: $(BUILD_DIR)/lib/pkgconfig/glib-2.0.pc \
		$(BUILD_DIR)/lib/pkgconfig/gmodule-2.0.pc \
		$(ENCHANT_DIR)
	cd $(ENCHANT_DIR) && PKG_CONFIG_PATH=$(BUILD_DIR)/lib/pkgconfig ./configure CFLAGS="$(CFLAGS)" $(ENCHANT_CONFIG_OPTS) && make
	cp $(ENCHANT_DIR)/src/.libs/libenchant.dll $(BUILD_DIR)/lib/
	mkdir -p $(BUILD_DIR)/lib/enchant
	cp $(ENCHANT_DIR)/src/ispell/.libs/libenchant_ispell.dll $(BUILD_DIR)/lib/enchant/
	cp $(ENCHANT_DIR)/src/myspell/.libs/libenchant_myspell.dll $(BUILD_DIR)/lib/enchant/


#  Make pkg-config files pointing to the right prefix
$(BUILD_DIR)/lib/pkgconfig/%.pc: $(BUILD_DIR)/lib/pkgconfig/%.pc.in
	echo "prefix=$(BUILD_DIR)" > $@
	cat $< >> $@

#  Make the enchant source dir
$(ENCHANT_DIR): src/$(ENCHANT_DIR).tar.gz
	tar -xzvf src/$(ENCHANT_DIR).tar.gz
	# Upgrade hunspell to latest version
	tar -xzvf src/hunspell-1.1.12-2.tar.gz
	cp hunspell-1.1.12/src/hunspell/*.cxx $(ENCHANT_DIR)/src/myspell/
	cp hunspell-1.1.12/src/hunspell/*.hxx $(ENCHANT_DIR)/src/myspell/
	cp hunspell-1.1.12/src/hunspell/*.h $(ENCHANT_DIR)/src/myspell/
	cp hunspell-1.1.12/src/hunspell/*.dsp $(ENCHANT_DIR)/src/myspell/
	cd $(ENCHANT_DIR)/src/ && patch < ../../patches/pwl.c.patch
	cd $(ENCHANT_DIR)/src/ && patch < ../../patches/enchant.c.patch
	cd $(ENCHANT_DIR)/src/myspell && patch < ../../../patches/myspell_checker.cpp.patch
	cd $(ENCHANT_DIR)/ && patch < ../patches/configure.patch
	cp patches/compile-resource $(ENCHANT_DIR)/compile-resource
	rm -rf hunspell-1.1.12

# Ability to extract MySpell dictionary files
$(BUILD_DIR)/myspell/%.dic: $(BUILD_DIR)/myspell/%.zip
	cd $(BUILD_DIR)/myspell && unzip $< '*.dic' '*.aff'


clean:
	rm -fr $(ENCHANT_DIR)

clobber: clean
	rm -f $(BUILD_DIR)/lib/pkgconfig/*.pc
	rm -f $(BUILD_DIR)/lib/libenchant*
	rm -rf $(BUILD_DIR)/lib/enchant
	rm -f $(BUILD_DIR)/myspell/*.dic
	rm -f $(BUILD_DIR)/myspell/*.aff
	rm -f $(BUILD_DIR)/myspell/*.txt

