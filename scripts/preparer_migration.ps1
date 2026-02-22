# ============================================================
#  SCRIPT DE SAUVEGARDE - Pour qui tu votes
#  A lancer sur l'ANCIEN PC avant la migration
#  Usage : clic droit > "Executer avec PowerShell"
# ============================================================

$ErrorActionPreference = "Stop"

# Dossier de destination (cle USB, disque externe, OneDrive...)
$dest = Read-Host "Ou sauvegarder ? (ex: D:\migration-pqtv, ou appuyez Entree pour le Bureau)"
if ([string]::IsNullOrWhiteSpace($dest)) {
    $dest = Join-Path ([Environment]::GetFolderPath("Desktop")) "migration-pqtv"
}

Write-Host "`n=== Sauvegarde Pour Qui Tu Votes ===" -ForegroundColor Cyan
Write-Host "Destination : $dest`n"

New-Item -ItemType Directory -Force -Path $dest | Out-Null

# 1. Projet complet
$projet = "$env:USERPROFILE\Downloads\FR comp mun"
if (Test-Path $projet) {
    Write-Host "[1/5] Copie du projet (site + donnees + scripts)..." -ForegroundColor Yellow
    robocopy $projet "$dest\FR comp mun" /MIR /NFL /NDL /NJH /NP /XD node_modules .git __pycache__ | Out-Null
    Write-Host "  OK" -ForegroundColor Green
} else {
    Write-Host "[1/5] ATTENTION : projet non trouve a $projet" -ForegroundColor Red
}

# 2. Dossier .claude (memoire, sessions, config)
$claude = "$env:USERPROFILE\.claude"
if (Test-Path $claude) {
    Write-Host "[2/5] Copie de la memoire Claude (.claude/)..." -ForegroundColor Yellow
    robocopy $claude "$dest\.claude" /MIR /NFL /NDL /NJH /NP | Out-Null
    Write-Host "  OK" -ForegroundColor Green
} else {
    Write-Host "[2/5] Dossier .claude non trouve" -ForegroundColor Red
}

# 3. Modele Tesseract francais
$tessdata = "$env:USERPROFILE\tessdata\fra.traineddata"
if (Test-Path $tessdata) {
    Write-Host "[3/5] Copie du modele Tesseract francais..." -ForegroundColor Yellow
    New-Item -ItemType Directory -Force -Path "$dest\tessdata" | Out-Null
    Copy-Item $tessdata "$dest\tessdata\fra.traineddata" -Force
    Write-Host "  OK" -ForegroundColor Green
} else {
    Write-Host "[3/5] Modele Tesseract non trouve (sera retelecharge)" -ForegroundColor DarkYellow
}

# 4. Sauvegarder le nom d'utilisateur actuel (crucial pour la migration .claude)
Write-Host "[4/5] Sauvegarde des metadonnees de migration..." -ForegroundColor Yellow
$meta = @{
    ancien_username = $env:USERNAME
    ancien_userprofile = $env:USERPROFILE
    ancien_projet_path = $projet
    date_sauvegarde = (Get-Date -Format "yyyy-MM-dd HH:mm")
    claude_project_folder = "C--Users-$env:USERNAME"
}
$meta | ConvertTo-Json | Out-File "$dest\migration_meta.json" -Encoding UTF8
Write-Host "  Username actuel sauvegarde : $env:USERNAME" -ForegroundColor Green

# 5. Inventaire des outils installes
Write-Host "[5/5] Generation de l'inventaire des outils..." -ForegroundColor Yellow
$inventaire = @()
$inventaire += "=== INVENTAIRE OUTILS - $(Get-Date -Format 'yyyy-MM-dd') ==="
$inventaire += "Username: $env:USERNAME"
$inventaire += ""

# Python
try { $inventaire += "Python : $(python --version 2>&1)" }
catch { $inventaire += "Python : non detecte" }

# Node
try { $inventaire += "Node.js : $(node --version 2>&1)" }
catch { $inventaire += "Node.js : non detecte" }

# npm
try { $inventaire += "npm : $(npm --version 2>&1)" }
catch { $inventaire += "npm : non detecte" }

# Git
try { $inventaire += "Git : $(git --version 2>&1)" }
catch { $inventaire += "Git : non detecte" }

# GitHub CLI
try { $inventaire += "GitHub CLI : $(gh --version 2>&1 | Select-Object -First 1)" }
catch { $inventaire += "GitHub CLI : non detecte" }

# Claude Code
try { $inventaire += "Claude Code : $(claude --version 2>&1)" }
catch { $inventaire += "Claude Code : non detecte" }

# Tesseract
$tessExe = "C:\Program Files\Tesseract-OCR\tesseract.exe"
if (Test-Path $tessExe) {
    $inventaire += "Tesseract : $(& $tessExe --version 2>&1 | Select-Object -First 1)"
} else { $inventaire += "Tesseract : non installe" }

# Pip packages
$inventaire += ""
$inventaire += "=== PACKAGES PIP ==="
try {
    $pips = pip list --format=freeze 2>&1 | Where-Object {
        $_ -match "^(pytesseract|PyMuPDF|easyocr|Pillow|torch|opencv|beautifulsoup4|requests|lxml)"
    }
    foreach ($p in $pips) { $inventaire += "  $p" }
} catch { $inventaire += "  pip : erreur" }

$inventaire += ""
$inventaire += "=== COMMANDES D'INSTALLATION RAPIDE ==="
$inventaire += "winget install Git.Git"
$inventaire += "winget install GitHub.cli"
$inventaire += "winget install OpenJS.NodeJS.LTS"
$inventaire += "winget install UB-Mannheim.TesseractOCR"
$inventaire += "npm install -g @anthropic-ai/claude-code"
$inventaire += "pip install pytesseract PyMuPDF Pillow beautifulsoup4 requests lxml"
$inventaire += ""
$inventaire += "=== FIN INVENTAIRE ==="
$inventaire | Out-File "$dest\inventaire_outils.txt" -Encoding UTF8
Write-Host "  OK" -ForegroundColor Green

# Resume
$size = (Get-ChildItem $dest -Recurse -File | Measure-Object -Property Length -Sum).Sum / 1MB
Write-Host "`n=== Sauvegarde terminee ===" -ForegroundColor Cyan
Write-Host "Taille totale : $([math]::Round($size, 0)) MB"
Write-Host "Dossier : $dest"
Write-Host "`nContenu :"
Write-Host "  FR comp mun\         -> le projet complet"
Write-Host "  .claude\             -> memoire + sessions + permissions Claude"
Write-Host "  tessdata\            -> modele OCR francais"
Write-Host "  migration_meta.json  -> metadonnees (username, chemins)"
Write-Host "  inventaire_outils.txt -> versions des outils"
Write-Host "`nSur le nouveau PC, lancer :" -ForegroundColor Yellow
Write-Host "  .\FR comp mun\scripts\installer_nouveau_pc.ps1"
