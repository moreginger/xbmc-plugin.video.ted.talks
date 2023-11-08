## TEDTalks video addon for Kodi
# simple Makefile to package the plugin based on addon.xml

DISTRIBUTION = matrix

ADDON_XML = ./addon.xml

# explicitly identify the source files
define SOURCE_FILES
${ADDON_XML}
./LICENSE.txt
./default.py
./resources/settings.xml
./resources/icon.png
./resources/speaker.png
./resources/rss_feeds.opml
./resources/language/resource.language.en_gb/strings.po
./resources/language/resource.language.fi_fi/strings.po
./resources/language/resource.language.hu_hu/strings.po
./resources/language/resource.language.pt_pt/strings.po
./resources/language/resource.language.sv_se/strings.po
./resources/lib/settings.py
./resources/lib/ted_talks.py
./resources/lib/model/arguments.py
./resources/lib/model/fetcher.py
./resources/lib/model/rss_scraper.py
./resources/lib/model/search_scraper.py
./resources/lib/model/series_scraper.py
./resources/lib/model/talk_scraper.py
./resources/lib/model/topics_scraper.py
./resources/lib/model/speakers_scraper.py
endef

# newline character
define NL


endef

_AO = grep -o '<addon[^>]*>' ${ADDON_XML}
ADDONID = $(subst id=",,$(shell ${_AO} | grep -o 'id="[^"]*'))
VERSION = $(subst on=",,$(shell ${_AO} | grep -o 'on="[^"]*'))
SOURCES = $(sort $(SOURCE_FILES)) # hack to remove newlines
PACKAGE = ${ADDONID}-${VERSION}-${DISTRIBUTION}.zip

.PHONY: clean

${PACKAGE} : ${ADDONID} 
	rm -f $@  # force new zip
	zip -r $@ $<

${ADDONID} : $(SOURCES)
	$(foreach f,$^,install -p -D ${f} $@/${f}${NL})

clean :
	rm -fR ${ADDONID}
