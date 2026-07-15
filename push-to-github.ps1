"""
Partner App QA Framework - Push to GitHub (PowerShell)
Run: .\push-to-github.ps1
"""

# ============================================================================
# CONFIGURATION
# ============================================================================

$ErrorActionPreference = "Stop"

Write-Host "`n" -ForegroundColor Green
Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║        Partner App QA Framework - GitHub Push Script         ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan

# ============================================================================
# STEP 1: Get GitHub Repository URL
# ============================================================================

Write-Host "`n[1/7] Enter your GitHub repository URL" -ForegroundColor Yellow
Write-Host "Example: https://github.com/username/partner-app-qa.git" -ForegroundColor Gray

$GITHUB_URL = Read-Host "GitHub URL"

if ([string]::IsNullOrEmpty($GITHUB_URL)) {
    Write-Host "✗ GitHub URL is required" -ForegroundColor Red
    exit 1
}

# ============================================================================
# STEP 2: Get Git User Configuration
# ============================================================================

Write-Host "`n[2/7] Configure Git user" -ForegroundColor Yellow

$GIT_NAME = Read-Host "Git user name (e.g., John Doe)"
$GIT_EMAIL = Read-Host "Git user email (e.g., john@example.com)"

if ([string]::IsNullOrEmpty($GIT_NAME) -or [string]::IsNullOrEmpty($GIT_EMAIL)) {
    Write-Host "✗ Git name and email are required" -ForegroundColor Red
    exit 1
}

# ============================================================================
# STEP 3: Initialize Repository
# ============================================================================

Write-Host "`n[3/7] Initializing Git repository" -ForegroundColor Yellow

if (Test-Path ".\.git") {
    Write-Host "✓ Git already initialized" -ForegroundColor Green
} else {
    git init
    Write-Host "✓ Git repository initialized" -ForegroundColor Green
}

# ============================================================================
# STEP 4: Configure Git User
# ============================================================================

Write-Host "`n[4/7] Configuring Git user" -ForegroundColor Yellow

git config user.name $GIT_NAME
git config user.email $GIT_EMAIL

Write-Host "✓ Git user configured: $GIT_NAME <$GIT_EMAIL>" -ForegroundColor Green

# ============================================================================
# STEP 5: Add All Files
# ============================================================================

Write-Host "`n[5/7] Staging all files" -ForegroundColor Yellow

git add .

Write-Host "✓ Files staged" -ForegroundColor Green

# Show status
Write-Host "`nFiles to commit:" -ForegroundColor Cyan
git status --short | Select-Object -First 20
Write-Host "..." -ForegroundColor Gray

# ============================================================================
# STEP 6: Create Initial Commit
# ============================================================================

Write-Host "`n[6/7] Creating initial commit" -ForegroundColor Yellow

$commit_message = @"
Initial commit: Enterprise QA Automation Framework

- Added core framework modules (logger, wait_utils, drivers)
- Implemented Page Object Model for web automation
- Added mobile automation support (Appium)
- Created API testing layer
- Added database validation module
- Implemented BDD framework with pytest-bdd
- Created comprehensive test fixtures
- Added GitHub Actions CI/CD pipeline
- Added Docker orchestration
- Included full documentation

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>
"@

git commit -m $commit_message

Write-Host "✓ Initial commit created" -ForegroundColor Green

# ============================================================================
# STEP 7: Push to GitHub
# ============================================================================

Write-Host "`n[7/7] Pushing to GitHub" -ForegroundColor Yellow
Write-Host "Repository: $GITHUB_URL" -ForegroundColor Blue

# Remove existing remote if it exists
try {
    git remote remove origin
} catch {
    # Remote doesn't exist, which is fine
}

# Add new remote
git remote add origin $GITHUB_URL

# Rename branch to main if needed
git branch -M main

# Push to GitHub
try {
    git push -u origin main
    Write-Host "✓ Successfully pushed to GitHub" -ForegroundColor Green
} catch {
    Write-Host "✗ Failed to push to GitHub" -ForegroundColor Red
    Write-Host "`nTroubleshooting:" -ForegroundColor Yellow
    Write-Host "  1. Check repository URL is correct" -ForegroundColor Gray
    Write-Host "  2. Verify GitHub credentials (use Personal Access Token for HTTPS)" -ForegroundColor Gray
    Write-Host "  3. For SSH, ensure SSH key is configured" -ForegroundColor Gray
    exit 1
}

# ============================================================================
# Summary
# ============================================================================

Write-Host "`n" -ForegroundColor Green
Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║                    Push Complete!                             ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Green

Write-Host "`n✓ Framework successfully pushed to GitHub" -ForegroundColor Green

Write-Host "`nNext Steps:" -ForegroundColor Cyan
Write-Host "  1. Visit GitHub repository to verify files" -ForegroundColor Gray
Write-Host "  2. Check GitHub Actions for pipeline status" -ForegroundColor Gray
Write-Host "  3. Configure repository secrets if needed" -ForegroundColor Gray
Write-Host "  4. Setup branch protection rules" -ForegroundColor Gray
Write-Host "  5. Start development!" -ForegroundColor Gray

Write-Host "`nUseful Commands:" -ForegroundColor Cyan
Write-Host "  git log --oneline          # View commit history" -ForegroundColor Gray
Write-Host "  git branch -a              # List all branches" -ForegroundColor Gray
Write-Host "  git status                 # Check repository status" -ForegroundColor Gray
Write-Host "  git pull origin main       # Pull latest changes" -ForegroundColor Gray

Write-Host "`n"
