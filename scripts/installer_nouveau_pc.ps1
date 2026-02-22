# ============================================================
#  SCRIPT D'INSTALLATION - Pour qui tu votes
#  A lancer sur le NOUVEAU PC apres avoir copie le dossier de migration
#  Usage : clic droit > "Executer avec PowerShell"
# ============================================================

$ErrorActionPreference = "Continue"

Write-Host "=== Installation Pour Qui Tu Votes ===" -ForegroundColor Cyan
Write-Host ""

# Detecter le dossier de migration
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
# On est dans FR comp mun\scripts, remonter de 2 niveaux si migration_meta.json est au-dessus
$migrationDir = Split-Path -Parent (Split-Path -Parent $scriptDir)
if (-not (Test-Path "$migrationDir\migration_meta.json")) {
    # Peut-etre lance depuis le dossier FR comp mun directement
    $migrationDir = Split-Path -Parent $scriptDir
    if (-not (Test-Path "$migrationDir\migration_meta.json")) {
        $migrationDir = Read-Host "Chemin du dossier de migration (celui contenant migration_meta.json)"
    }
}

# Lire les metadonnees de migration
$meta = $null
$ancienUsername = $null
if (Test-Path "$migrationDir\migration_meta.json") {
    $meta = Get-Content "$migrationDir\migration_meta.json" -Raw | ConvertFrom-Json
    $ancienUsername = $meta.ancien_username
    Write-Host "Migration depuis le PC de : $ancienUsername" -ForegroundColor DarkYellow
} else {
    Write-Host "ATTENTION : migration_meta.json non trouve. La memoire Claude devra etre ajustee manuellement." -ForegroundColor Red
    $ancienUsername = Read-Host "Quel etait l'ancien username Windows ?"
}

$nouveauUsername = $env:USERNAME
$usernameChange = $ancienUsername -ne $nouveauUsername
if ($usernameChange) {
    Write-Host "Changement de username detecte : $ancienUsername -> $nouveauUsername" -ForegroundColor Yellow
}

# ============================================================
# ETAPE 1 : Restaurer le projet
# ============================================================
Write-Host "`n[1/8] Restauration du projet..." -ForegroundColor Yellow

$projetSrc = "$migrationDir\FR comp mun"
$projetDest = "$env:USERPROFILE\Downloads\FR comp mun"

if ((Test-Path $projetSrc) -and ($projetSrc -ne $projetDest)) {
    robocopy $projetSrc $projetDest /MIR /NFL /NDL /NJH /NP | Out-Null
    Write-Host "  Projet copie vers $projetDest" -ForegroundColor Green
} elseif (Test-Path $projetDest) {
    Write-Host "  Projet deja en place" -ForegroundColor DarkYellow
} else {
    Write-Host "  Projet non trouve dans la migration" -ForegroundColor Red
}

# ============================================================
# ETAPE 2 : Restaurer la memoire Claude + adapter les chemins
# ============================================================
Write-Host "`n[2/8] Restauration de la memoire Claude..." -ForegroundColor Yellow

$claudeSrc = "$migrationDir\.claude"
$claudeDest = "$env:USERPROFILE\.claude"

if (Test-Path $claudeSrc) {
    # Copier tout le dossier .claude
    robocopy $claudeSrc $claudeDest /MIR /NFL /NDL /NJH /NP | Out-Null
    Write-Host "  Fichiers .claude copies" -ForegroundColor Green

    # Si le username a change, renommer le dossier projet dans .claude/projects/
    if ($usernameChange) {
        $ancienDossier = "$claudeDest\projects\C--Users-$ancienUsername"
        $nouveauDossier = "$claudeDest\projects\C--Users-$nouveauUsername"

        if ((Test-Path $ancienDossier) -and (-not (Test-Path $nouveauDossier))) {
            Rename-Item $ancienDossier $nouveauDossier
            Write-Host "  Dossier memoire renomme : C--Users-$ancienUsername -> C--Users-$nouveauUsername" -ForegroundColor Green
        } elseif (Test-Path $nouveauDossier) {
            Write-Host "  Dossier memoire deja au bon nom" -ForegroundColor DarkYellow
        }

        # Adapter les chemins dans settings.local.json (permissions)
        $settingsFile = "$claudeDest\settings.local.json"
        if (Test-Path $settingsFile) {
            $content = Get-Content $settingsFile -Raw -Encoding UTF8
            $newContent = $content -replace [regex]::Escape($ancienUsername), $nouveauUsername
            [System.IO.File]::WriteAllText($settingsFile, $newContent, [System.Text.UTF8Encoding]::new($false))
            Write-Host "  Chemins dans settings.local.json mis a jour ($ancienUsername -> $nouveauUsername)" -ForegroundColor Green
        }

        # Adapter les chemins dans MEMORY.md
        $memoryFile = "$nouveauDossier\memory\MEMORY.md"
        if (Test-Path $memoryFile) {
            $content = Get-Content $memoryFile -Raw -Encoding UTF8
            $newContent = $content -replace [regex]::Escape($ancienUsername), $nouveauUsername
            [System.IO.File]::WriteAllText($memoryFile, $newContent, [System.Text.UTF8Encoding]::new($false))
            Write-Host "  Chemins dans MEMORY.md mis a jour" -ForegroundColor Green
        }
    }

    # Supprimer les credentials (il faudra se reconnecter)
    $credFile = "$claudeDest\.credentials.json"
    if (Test-Path $credFile) {
        Remove-Item $credFile -Force
        Write-Host "  Ancien token supprime (reconnexion necessaire au 1er lancement)" -ForegroundColor DarkYellow
    }
} else {
    Write-Host "  Pas de dossier .claude dans la migration" -ForegroundColor Red
}

# ============================================================
# ETAPE 3 : Git
# ============================================================
Write-Host "`n[3/8] Git..." -ForegroundColor Yellow
try {
    $gitVer = git --version 2>&1
    Write-Host "  Deja installe : $gitVer" -ForegroundColor Green
} catch {
    Write-Host "  Installation..."
    winget install Git.Git --accept-package-agreements --accept-source-agreements
    Write-Host "  Git installe (rouvrir le terminal pour l'utiliser)" -ForegroundColor Green
}

# ============================================================
# ETAPE 4 : Node.js (requis pour Claude Code)
# ============================================================
Write-Host "`n[4/8] Node.js..." -ForegroundColor Yellow
try {
    $nodeVer = node --version 2>&1
    Write-Host "  Deja installe : $nodeVer" -ForegroundColor Green
} catch {
    Write-Host "  Installation..."
    winget install OpenJS.NodeJS.LTS --accept-package-agreements --accept-source-agreements
    Write-Host "  Node.js installe (rouvrir le terminal)" -ForegroundColor Green
}

# ============================================================
# ETAPE 5 : Claude Code
# ============================================================
Write-Host "`n[5/8] Claude Code..." -ForegroundColor Yellow
try {
    $claudeVer = claude --version 2>&1
    Write-Host "  Deja installe : $claudeVer" -ForegroundColor Green
} catch {
    try {
        npm install -g @anthropic-ai/claude-code 2>&1 | Out-Null
        Write-Host "  Claude Code installe" -ForegroundColor Green
    } catch {
        Write-Host "  Echec (installer Node.js d'abord, puis : npm install -g @anthropic-ai/claude-code)" -ForegroundColor Red
    }
}

# ============================================================
# ETAPE 6 : Python + packages pip
# ============================================================
Write-Host "`n[6/8] Python + packages pip..." -ForegroundColor Yellow
$hasPython = $false
try {
    $pyVer = python --version 2>&1
    Write-Host "  Python : $pyVer" -ForegroundColor Green
    $hasPython = $true
} catch {
    Write-Host "  Python non installe. Installation..."
    winget install Python.Python.3.14 --accept-package-agreements --accept-source-agreements
    Write-Host "  IMPORTANT : Rouvrir le terminal apres installation" -ForegroundColor Red
}

if ($hasPython) {
    Write-Host "  Installation des packages pip..."
    pip install pytesseract PyMuPDF Pillow beautifulsoup4 requests lxml 2>&1 | Out-Null
    Write-Host "  Packages essentiels installes" -ForegroundColor Green

    $installEasyocr = Read-Host "  Installer EasyOCR ? (lourd ~2 Go avec PyTorch, optionnel si Tesseract suffit) [o/N]"
    if ($installEasyocr -eq "o") {
        pip install easyocr 2>&1 | Out-Null
        Write-Host "  EasyOCR + torch + opencv installes" -ForegroundColor Green
    }
}

# ============================================================
# ETAPE 7 : Tesseract OCR + modele francais
# ============================================================
Write-Host "`n[7/8] Tesseract OCR..." -ForegroundColor Yellow

$tessExe = "C:\Program Files\Tesseract-OCR\tesseract.exe"
if (Test-Path $tessExe) {
    Write-Host "  Deja installe" -ForegroundColor Green
} else {
    winget install UB-Mannheim.TesseractOCR --accept-package-agreements --accept-source-agreements
    Write-Host "  Tesseract installe" -ForegroundColor Green
}

# Modele francais
$tessdataDest = "$env:USERPROFILE\tessdata"
New-Item -ItemType Directory -Force -Path $tessdataDest | Out-Null
$fraSrc = "$migrationDir\tessdata\fra.traineddata"
$fraDest = "$tessdataDest\fra.traineddata"

if (Test-Path $fraSrc) {
    Copy-Item $fraSrc $fraDest -Force
    Write-Host "  Modele francais copie depuis la migration" -ForegroundColor Green
} elseif (Test-Path $fraDest) {
    Write-Host "  Modele francais deja present" -ForegroundColor Green
} else {
    Write-Host "  Telechargement du modele francais..."
    Invoke-WebRequest -Uri "https://github.com/tesseract-ocr/tessdata_best/raw/main/fra.traineddata" -OutFile $fraDest
    Write-Host "  Modele telecharge" -ForegroundColor Green
}

# Variable d'environnement TESSDATA_PREFIX
$currentTessdata = [Environment]::GetEnvironmentVariable("TESSDATA_PREFIX", "User")
if ($currentTessdata -ne $tessdataDest) {
    [Environment]::SetEnvironmentVariable("TESSDATA_PREFIX", $tessdataDest, "User")
    $env:TESSDATA_PREFIX = $tessdataDest
    Write-Host "  Variable TESSDATA_PREFIX configuree : $tessdataDest" -ForegroundColor Green
}

# GitHub CLI (optionnel)
Write-Host ""
$installGh = Read-Host "  Installer GitHub CLI (pour push/PR) ? [o/N]"
if ($installGh -eq "o") {
    winget install GitHub.cli --accept-package-agreements --accept-source-agreements
    Write-Host "  GitHub CLI installe" -ForegroundColor Green
}

# ============================================================
# ETAPE 8 : Verification finale
# ============================================================
Write-Host "`n[8/8] Verification finale..." -ForegroundColor Yellow
Write-Host ""

$allOk = $true

# Projet
if (Test-Path "$projetDest\js\app.js") {
    Write-Host "  [OK] Projet (js/app.js)" -ForegroundColor Green
} else {
    Write-Host "  [!!] Projet non trouve" -ForegroundColor Red; $allOk = $false
}

# JSON data
$jsonCount = (Get-ChildItem "$projetDest\data\elections\*.json" -ErrorAction SilentlyContinue | Measure-Object).Count
if ($jsonCount -gt 0) {
    Write-Host "  [OK] $jsonCount fichiers elections JSON" -ForegroundColor Green
} else {
    Write-Host "  [!!] Aucun fichier election JSON" -ForegroundColor Red; $allOk = $false
}

# Memoire Claude
$memoryPath = "$env:USERPROFILE\.claude\projects\C--Users-$nouveauUsername\memory\MEMORY.md"
if (Test-Path $memoryPath) {
    Write-Host "  [OK] MEMORY.md (memoire Claude)" -ForegroundColor Green
} else {
    Write-Host "  [!!] MEMORY.md non trouve a $memoryPath" -ForegroundColor Red; $allOk = $false
}

# Permissions Claude
if (Test-Path "$env:USERPROFILE\.claude\settings.local.json") {
    Write-Host "  [OK] Permissions Claude (settings.local.json)" -ForegroundColor Green
} else {
    Write-Host "  [!!] Permissions Claude manquantes" -ForegroundColor Red
}

# Python
try { python --version 2>&1 | Out-Null; Write-Host "  [OK] Python" -ForegroundColor Green }
catch { Write-Host "  [!!] Python" -ForegroundColor Red; $allOk = $false }

# Node.js
try { node --version 2>&1 | Out-Null; Write-Host "  [OK] Node.js" -ForegroundColor Green }
catch { Write-Host "  [!!] Node.js (requis pour Claude Code)" -ForegroundColor Red; $allOk = $false }

# Claude Code
try { claude --version 2>&1 | Out-Null; Write-Host "  [OK] Claude Code" -ForegroundColor Green }
catch { Write-Host "  [!!] Claude Code (npm install -g @anthropic-ai/claude-code)" -ForegroundColor Red; $allOk = $false }

# Git
try { git --version 2>&1 | Out-Null; Write-Host "  [OK] Git" -ForegroundColor Green }
catch { Write-Host "  [!!] Git" -ForegroundColor Red }

# Tesseract
if (Test-Path $tessExe) { Write-Host "  [OK] Tesseract OCR" -ForegroundColor Green }
else { Write-Host "  [!!] Tesseract OCR" -ForegroundColor Red }

# Modele francais
if (Test-Path $fraDest) { Write-Host "  [OK] Modele francais OCR" -ForegroundColor Green }
else { Write-Host "  [!!] Modele francais OCR" -ForegroundColor Red }

# TESSDATA_PREFIX
if ($env:TESSDATA_PREFIX) { Write-Host "  [OK] TESSDATA_PREFIX = $env:TESSDATA_PREFIX" -ForegroundColor Green }
else { Write-Host "  [!!] TESSDATA_PREFIX non configure" -ForegroundColor Red }

# Resume
Write-Host ""
if ($allOk) {
    Write-Host "=== Installation terminee avec succes ===" -ForegroundColor Cyan
} else {
    Write-Host "=== Installation terminee avec des avertissements ===" -ForegroundColor Yellow
    Write-Host "Certains outils doivent etre installes manuellement (voir ci-dessus)"
}

Write-Host ""
Write-Host "Prochaines etapes :" -ForegroundColor Yellow
Write-Host "  1. Rouvrir le terminal (pour que les PATH soient a jour)"
Write-Host "  2. Lancer 'claude' et se connecter (la memoire sera chargee automatiquement)"
Write-Host ""
Write-Host "Pour lancer le site en local :" -ForegroundColor Yellow
Write-Host "  cd '$projetDest'"
Write-Host "  python -m http.server 8000"
Write-Host "  Ouvrir http://localhost:8000"
