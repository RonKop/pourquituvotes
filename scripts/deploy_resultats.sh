#!/bin/bash
# Pipeline complet : validation → shells → sitemap → commit → push → ping Google
# Usage :
#   bash scripts/deploy_resultats.sh "résultats T1 top 20 villes"
#   bash scripts/deploy_resultats.sh  # message par défaut

set -e
cd "$(dirname "$0")/.."

MSG="${1:-feat: mise à jour résultats municipales 2026}"
TIMESTAMP=$(date +%Y%m%d%H%M)

echo "=== 1/6 Validation des données ==="
python scripts/valider_donnees.py
echo ""

echo "=== 2/6 Régénération des shells SEO ==="
python scripts/generate_static_shells.py
echo ""

echo "=== 3/6 Régénération du sitemap ==="
python scripts/generate_sitemap.py
echo ""

echo "=== 4/6 Commit ==="
git add data/ municipales-2026/ enjeux-2026/ sitemap.xml _redirects js/ css/
git commit -m "$MSG

Timestamp: $TIMESTAMP
Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>" || echo "Rien à committer"
echo ""

echo "=== 5/6 Push ==="
git push origin main
echo ""

echo "=== 6/6 Ping Google Sitemap ==="
curl -s "https://www.google.com/ping?sitemap=https://pourquituvotes.fr/sitemap.xml" > /dev/null && echo "Google pinged OK" || echo "Google ping failed (non-bloquant)"
echo ""

echo "=== DEPLOY TERMINÉ ($TIMESTAMP) ==="
echo "Vérifier : https://pourquituvotes.fr/municipales-2026/resultats/"
