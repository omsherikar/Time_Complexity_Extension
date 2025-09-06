#!/bin/bash

# TimeComplexity Analyzer - Extension Packaging Script
# This script creates a production-ready ZIP file for Chrome Web Store submission

echo "🚀 Packaging TimeComplexity Analyzer Extension..."

# Create version from git tag or use default
VERSION=$(git describe --tags --abbrev=0 2>/dev/null || echo "v1.0.0")
echo "📦 Version: $VERSION"

# Create package directory
PACKAGE_DIR="timecomplexity-analyzer-${VERSION}"
rm -rf "$PACKAGE_DIR"
mkdir -p "$PACKAGE_DIR"

# Copy extension files
echo "📁 Copying extension files..."
cp manifest.json "$PACKAGE_DIR/"
cp popup.html "$PACKAGE_DIR/"
cp popup.css "$PACKAGE_DIR/"
cp popup.js "$PACKAGE_DIR/"
cp content.js "$PACKAGE_DIR/"
cp background.js "$PACKAGE_DIR/"

# Copy icons directory
cp -r icons "$PACKAGE_DIR/"

# Copy README
cp README.md "$PACKAGE_DIR/"

# Create ZIP file
ZIP_FILE="timecomplexity-analyzer-${VERSION}.zip"
echo "🗜️ Creating ZIP file: $ZIP_FILE"
cd "$PACKAGE_DIR"
zip -r "../$ZIP_FILE" . -x "*.DS_Store" "*.git*"
cd ..

# Clean up
rm -rf "$PACKAGE_DIR"

# Show file info
echo "✅ Package created successfully!"
echo "📁 File: $ZIP_FILE"
echo "📊 Size: $(du -h "$ZIP_FILE" | cut -f1)"

# Create releases directory if it doesn't exist
mkdir -p releases
mv "$ZIP_FILE" "releases/"

echo "🎉 Extension packaged and ready for Chrome Web Store submission!"
echo "📂 Package location: releases/$ZIP_FILE"
echo ""
echo "Next steps:"
echo "1. Go to https://chrome.google.com/webstore/devconsole/"
echo "2. Click 'Add new item'"
echo "3. Upload releases/$ZIP_FILE"
echo "4. Fill in the required information"
echo "5. Submit for review"
