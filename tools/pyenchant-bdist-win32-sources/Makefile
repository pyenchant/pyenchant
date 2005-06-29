
BUILD_DIR = /home/rfk/pyenchant/tools/pyenchant-bdist-win32-sources/build
ASPELL_DIR = aspell-0.60.2
ENCHANT_DIR = enchant-1.1.6

#XMINGW_CONFIG_OPTS = --target=i386-mingw32msvc --host=i386-mingw32msvc
XMINGW_CONFIG_OPTS =
ASPELL_CONFIG_OPTS = --enable-win32-relocatable --enable-shared --disable-rpath 
ENCHANT_CONFIG_OPTS = --enable-ispell --enable-myspell --disable-aspell --with-aspell-prefix=$(BUILD_DIR)

CFLAGS = -g -Wl,--enable-runtime-pseudo-reloc

all: $(BUILD_DIR)/lib/libenchant-1.dll $(BUILD_DIR)/myspell/en_GB.dic \
	$(BUILD_DIR)/myspell/en_US.dic $(BUILD_DIR)/myspell/de_DE.dic \
	$(BUILD_DIR)/myspell/fr_FR.dic
	# Remove dictionaries that are causing trouble
	rm -f $(BUILD_DIR)/myspell/de_AT.dic

#  Make enchant. Dont build aspell plugin yet
#$(BUILD_DIR)/lib/libenchant-1.dll: $(BUILD_DIR)/lib/libaspell-15.dll
$(BUILD_DIR)/lib/libenchant-1.dll: $(BUILD_DIR)/lib/pkgconfig/glib-2.0.pc \
		$(BUILD_DIR)/lib/pkgconfig/gmodule-2.0.pc \
		$(ENCHANT_DIR)
	cd $(ENCHANT_DIR) && PKG_CONFIG_PATH=$(BUILD_DIR)/lib/pkgconfig ./configure CFLAGS="$(CFLAGS)" $(XMINGW_CONFIG_OPTS) $(ENCHANT_CONFIG_OPTS) && make
	cp $(ENCHANT_DIR)/src/.libs/libenchant-1.dll $(BUILD_DIR)/lib/
	#cp $(ENCHANT_DIR)/src/aspell/.libs/libenchant_aspell-1.dll $(BUILD_DIR)/lib/
	mkdir $(BUILD_DIR)/lib/enchant
	cp $(ENCHANT_DIR)/src/ispell/.libs/libenchant_ispell-1.dll $(BUILD_DIR)/lib/enchant/
	cp $(ENCHANT_DIR)/src/myspell/.libs/libenchant_myspell-1.dll $(BUILD_DIR)/lib/enchant/


#  Make the necessary Aspell libraries and headers
$(BUILD_DIR)/lib/libaspell-15.dll: $(ASPELL_DIR)
	cd $(ASPELL_DIR) && ./configure CFLAGS="$(CFLAGS)" $(XMINGW_CONFIG_OPTS) $(ASPELL_CONFIG_OPTS) && make libaspell.la
	mkdir -p $(BUILD_DIR)/lib
	mkdir -p $(BUILD_DIR)/include
	mkdir -p $(BUILD_DIR)/bin
	mkdir -p $(BUILD_DIR)/include/pspell
	cp $(ASPELL_DIR)/.libs/libaspell-15.dll $(BUILD_DIR)/lib
	cp $(ASPELL_DIR)/interfaces/cc/aspell.h $(BUILD_DIR)/include/
	cp $(ASPELL_DIR)/interfaces/cc/pspell.h $(BUILD_DIR)/include/pspell

#  Make pkg-config files pointing to the right prefix
$(BUILD_DIR)/lib/pkgconfig/%.pc: $(BUILD_DIR)/lib/pkgconfig/%.pc.in
	echo "prefix=$(BUILD_DIR)" > $@
	cat $< >> $@

#  Make the enchant and aspell source dirs
$(ASPELL_DIR): src/$(ASPELL_DIR).tar.gz
	tar -xzvf src/$(ASPELL_DIR).tar.gz
	patch $(ASPELL_DIR)/common/file_util.cpp patches/aspell_file_util.cpp.patch

$(ENCHANT_DIR): src/$(ENCHANT_DIR).tar.gz
	tar -xzvf src/$(ENCHANT_DIR).tar.gz
	patch $(ENCHANT_DIR)/src/enchant.c patches/enchant.c.patch
	patch $(ENCHANT_DIR)/configure patches/enchant_configure.patch

# Ability to extract MySpell dictionary files
$(BUILD_DIR)/myspell/%.dic: $(BUILD_DIR)/myspell/%.zip
	cd $(BUILD_DIR)/myspell && unzip $<


clean:
	rm -fr $(ASPELL_DIR) $(ENCHANT_DIR)

clobber: clean
	rm -f $(BUILD_DIR)/lib/pkgconfig/*.pc
	rm -rf $(BUILD_DIR)/include/aspell.h $(BUILD_DIR)/include/pspell
	rm -f $(BUILD_DIR)/lib/libaspell*
	rm -f $(BUILD_DIR)/lib/libenchant*
	rm -rf $(BUILD_DIR)/lib/enchant
	rm -f $(BUILD_DIR)/myspell/*.dic
	rm -f $(BUILD_DIR)/myspell/*.aff
	rm -f $(BUILD_DIR)/myspell/*.txt

