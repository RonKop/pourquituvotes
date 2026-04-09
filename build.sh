#!/bin/bash
# Build script for Cloudflare Pages
# Copies deployable files to _site/, excluding heavy/unnecessary ones

set -e

rm -rf _site
mkdir -p _site

# Copy everything first
cp -r . _site/ 2>/dev/null || true

# Remove excluded directories and files
rm -rf _site/_site
rm -rf _site/.git
rm -rf _site/.github
rm -rf _site/.claude
rm -rf _site/.wrangler
rm -rf _site/node_modules
rm -rf _site/scripts
rm -rf _site/data/programmes
rm -rf _site/data/resultats-communes
rm -rf _site/data/dossiers_presse

# Remove results pages (32K+ files)
find _site/municipales-2026 -type d -name "resultats" -exec rm -rf {} + 2>/dev/null || true

# Remove heavy data files
rm -f _site/data/communes_france.json
rm -f _site/data/mapping_insee.json
rm -f _site/data/suivi_candidats.csv
rm -f _site/data/candidats_municipales_2026.csv
rm -f _site/data/crawl-registry.json
rm -f _site/data/debug_*
rm -f _site/data/emails_*
rm -f _site/data/mairies_*
rm -f _site/data/candidatures_*
rm -f _site/data/candidatures-*

# Remove by extension
find _site -name "*.py" -delete
find _site -name "*.md" -delete
find _site -name "*.pyc" -delete
find _site -name "*.xlsx" -delete
find _site -name "*.pptx" -delete
find _site -name "*.docx" -delete
find _site -name "*.zip" -delete
find _site -name "*.csv" -delete

# Remove build script itself
rm -f _site/build.sh

echo "Build complete: $(find _site -type f | wc -l) files"
