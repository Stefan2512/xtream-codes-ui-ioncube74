# Xtream Codes UI Archive Builder with ION Cube 7.4 + Auto Update System
# Author: Stefan2512
# Repository: https://github.com/Stefan2512/xtream-codes-ui-ioncube74

# Variables
VERSION := v1.0
RELEASE_DATE := $(shell date +%Y%m%d)
BUILD_NUMBER := $(shell date +%Y%m%d%H%M)
SOURCE_DIR := /home/xtreamcodes/iptv_xtream_codes
BUILD_DIR := ./build
RELEASE_DIR := ./releases
TEMP_DIR := ./temp

# Archive names
MAIN_ARCHIVE := xtream-codes-ui-main-ioncube74.zip
LB_ARCHIVE := xtream-codes-ui-loadbalancer-ioncube74.zip
RELEASE_ARCHIVE := release_22f_$(BUILD_NUMBER).zip

# GitHub settings
GITHUB_REPO := Stefan2512/xtream-codes-ui-ioncube74

# Colors for output
RED := \033[0;31m
GREEN := \033[0;32m
YELLOW := \033[1;33m
BLUE := \033[0;34m
PURPLE := \033[0;35m
CYAN := \033[0;36m
NC := \033[0m # No Color

.PHONY: all clean main lb release check-source help auto-release github-release

# Help target
help:
.git@echo "$(BLUE)🚀 Xtream Codes Archive Builder + Auto Update System$(NC)"
.git@echo ""
.git@echo "$(YELLOW)📦 Build Commands:$(NC)"
.git@echo "  $(GREEN)all$(NC)             - Build all archives"
.git@echo "  $(GREEN)release$(NC)         - Build release update archive"
.git@echo "  $(GREEN)auto-release$(NC)    - Build + Auto push to GitHub"
.git@echo ""
.git@echo "$(YELLOW)🔄 GitHub Integration:$(NC)"
.git@echo "  $(GREEN)github-release$(NC)  - Create GitHub release"
.git@echo "  $(GREEN)test-build$(NC)      - Test build without GitHub"
.git@echo ""
.git@echo "$(YELLOW)🛠️  Setup:$(NC)"
.git@echo "  $(GREEN)check-source$(NC)    - Verify source installation"
.git@echo "  $(GREEN)clean$(NC)           - Clean build directories"

# Check if source installation exists
check-source:
.git@echo "$(BLUE)🔍 Checking source installation...$(NC)"
.git@if [ ! -d "$(SOURCE_DIR)" ]; then \
ot found!$(NC)"; \
)✅ Source installation verified$(NC)"

# Create build directories
$(BUILD_DIR) $(RELEASE_DIR) $(TEMP_DIR):
@mkdir -p $@

# Clean build directories
clean:
@echo "$(YELLOW)🧹 Cleaning build directories...$(NC)"
@rm -rf $(BUILD_DIR) $(TEMP_DIR) $(RELEASE_DIR)
@echo "$(GREEN)✅ Clean completed$(NC)"

# Build release update archive (admin panel only)
release: check-source $(RELEASE_DIR) $(TEMP_DIR)
@echo "$(PURPLE)🔄 Building RELEASE update archive...$(NC)"

# Create XtreamUI-master structure
@mkdir -p $(TEMP_DIR)/XtreamUI-master

# Copy only admin panel and pytools
@if [ -d "$(SOURCE_DIR)/admin" ]; then \
 $(TEMP_DIR)/XtreamUI-master/; \
)✅ Admin panel included$(NC)"; \
fi
@if [ -d "$(SOURCE_DIR)/pytools" ]; then \
)✅ Python tools included$(NC)"; \
fi

# Copy essential files
@if [ -f "$(SOURCE_DIR)/permissions.sh" ]; then \
s.sh $(TEMP_DIR)/XtreamUI-master/; \
fi

# Add release info
@echo "# Xtream Codes UI Release Update" > $(TEMP_DIR)/XtreamUI-master/RELEASE_INFO
@echo "Version: $(VERSION)" >> $(TEMP_DIR)/XtreamUI-master/RELEASE_INFO
@echo "Build Date: $(RELEASE_DATE)" >> $(TEMP_DIR)/XtreamUI-master/RELEASE_INFO
@echo "Build Number: $(BUILD_NUMBER)" >> $(TEMP_DIR)/XtreamUI-master/RELEASE_INFO
@echo "Type: Admin Panel Update" >> $(TEMP_DIR)/XtreamUI-master/RELEASE_INFO

# Create version.json for update system
@echo '{"version":"$(VERSION)","build":"$(BUILD_NUMBER)","date":"$(shell date -Iseconds)","type":"admin_update"}' > $(TEMP_DIR)/XtreamUI-master/version.json

# Create archive
@cd $(TEMP_DIR) && zip -r ../$(RELEASE_DIR)/$(RELEASE_ARCHIVE) XtreamUI-master/ > /dev/null

@echo "$(GREEN)✅ Release update archive created: $(RELEASE_ARCHIVE)$(NC)"

# Generate checksums
checksums: $(RELEASE_DIR)
@echo "$(BLUE)🔐 Generating checksums...$(NC)"
@cd $(RELEASE_DIR) && sha256sum *.zip > SHA256SUMS 2>/dev/null || true

# Create GitHub release
github-release: release checksums
@echo "$(BLUE)📋 Creating GitHub release...$(NC)"

# Create release notes
@echo "# Xtream Codes UI $(VERSION) - Build $(BUILD_NUMBER)" > $(RELEASE_DIR)/RELEASE_NOTES.md
@echo "" >> $(RELEASE_DIR)/RELEASE_NOTES.md
@echo "## 🎯 What's New" >> $(RELEASE_DIR)/RELEASE_NOTES.md
@echo "- ✅ **ION Cube 7.4** pre-installed" >> $(RELEASE_DIR)/RELEASE_NOTES.md
@echo "- ✅ **Auto-update system** integrated" >> $(RELEASE_DIR)/RELEASE_NOTES.md
@echo "- ✅ **Admin panel updates**" >> $(RELEASE_DIR)/RELEASE_NOTES.md
@echo "" >> $(RELEASE_DIR)/RELEASE_NOTES.md
@echo "**Build:** $(BUILD_NUMBER) | **Date:** $(RELEASE_DATE)" >> $(RELEASE_DIR)/RELEASE_NOTES.md

# Create GitHub release
@if command -v gh >/dev/null 2>&1; then \
)-$(BUILD_NUMBER) *.zip SHA256SUMS \
) (Build $(BUILD_NUMBER))" \
otes-file RELEASE_NOTES.md \
 \
)✅ GitHub release $(VERSION)-$(BUILD_NUMBER) created!$(NC)"; \
else \
ot available$(NC)"; \
fi

# Auto release
auto-release: clean github-release
@echo "$(PURPLE)🚀 Auto-release $(VERSION)-$(BUILD_NUMBER) completed!$(NC)"
@echo "$(GREEN)✅ Check: https://github.com/$(GITHUB_REPO)/releases$(NC)"

all: release
