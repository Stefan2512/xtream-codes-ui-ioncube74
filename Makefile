VERSION := v1.0
BUILD_NUMBER := $(shell date +%Y%m%d%H%M%S)
SOURCE_DIR := /home/xtreamcodes/iptv_xtream_codes
RELEASE_DIR := ./releases
TEMP_DIR := ./temp
RELEASE_ARCHIVE := release_22f_$(BUILD_NUMBER).zip
GITHUB_REPO := Stefan2512/xtream-codes-ui-ioncube74

help:
	@echo "Xtream Codes Auto-Release System"
	@echo "Commands:"
	@echo "  release      - Build update archive"
	@echo "  auto-release - Build + GitHub release"

release: $(RELEASE_DIR) $(TEMP_DIR)
	@echo "Building release..."
	@mkdir -p $(TEMP_DIR)/XtreamUI-master
	@cp -r $(SOURCE_DIR)/admin $(TEMP_DIR)/XtreamUI-master/ 2>/dev/null || true
	@echo "Version: $(VERSION)" > $(TEMP_DIR)/XtreamUI-master/RELEASE_INFO
	@cd $(TEMP_DIR) && zip -r ../$(RELEASE_DIR)/$(RELEASE_ARCHIVE) XtreamUI-master/ > /dev/null
	@echo "Archive created: $(RELEASE_ARCHIVE)"

$(RELEASE_DIR) $(TEMP_DIR):
	@mkdir -p $@

.PHONY: help release github-release auto-release clean

github-release: release
	@echo "Creating GitHub release..."
	@cd $(RELEASE_DIR) && sha256sum *.zip > SHA256SUMS
	@echo "# Xtream Codes UI $(VERSION) - Build $(BUILD_NUMBER)" > $(RELEASE_DIR)/RELEASE_NOTES.md
	@echo "Auto-generated release with latest updates" >> $(RELEASE_DIR)/RELEASE_NOTES.md
	@cd $(RELEASE_DIR) && gh release create $(VERSION)-$(BUILD_NUMBER) *.zip SHA256SUMS --title "Xtream Codes UI $(VERSION) (Build $(BUILD_NUMBER))" --notes-file RELEASE_NOTES.md --repo $(GITHUB_REPO)
	@echo "GitHub release created!"

auto-release: github-release
	@echo "Auto-release completed!"
	@echo "Check: https://github.com/$(GITHUB_REPO)/releases"

clean:
	@rm -rf $(TEMP_DIR) $(RELEASE_DIR)
