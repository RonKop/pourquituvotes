#!/bin/bash
# Build script for Cloudflare Pages
# Copies all files except heavy/unnecessary ones to _site/

set -e

rm -rf _site
mkdir -p _site

# Copy everything except excluded patterns
rsync -a --exclude='_site' \
  --exclude='.git' \
  --exclude='.github' \
  --exclude='.claude' \
  --exclude='.wrangler' \
  --exclude='node_modules' \
  --exclude='scripts' \
  --exclude='data/programmes' \
  --exclude='data/resultats-communes' \
  --exclude='data/dossiers_presse' \
  --exclude='data/communes_france.json' \
  --exclude='data/mapping_insee.json' \
  --exclude='data/suivi_candidats.csv' \
  --exclude='data/candidats_municipales_2026.csv' \
  --exclude='data/crawl-registry.json' \
  --exclude='data/debug_*' \
  --exclude='data/emails_*' \
  --exclude='data/mairies_*' \
  --exclude='data/candidatures_*' \
  --exclude='data/candidatures-*' \
  --exclude='municipales-2026/*/resultats' \
  --exclude='*.py' \
  --exclude='*.md' \
  --exclude='*.pyc' \
  --exclude='*.xlsx' \
  --exclude='*.pptx' \
  --exclude='*.docx' \
  --exclude='*.zip' \
  --exclude='*.csv' \
  --exclude='build.sh' \
  ./ _site/

echo "Build complete: $(find _site -type f | wc -l) files"
