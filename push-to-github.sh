#!/bin/bash
# Partner App QA Framework - Push to GitHub Script

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║        Partner App QA Framework - GitHub Push Script         ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════════╝${NC}"

# Change to project directory
cd "$(dirname "$0")"

# ============================================================================
# STEP 1: Get GitHub Repository URL
# ============================================================================

echo -e "\n${YELLOW}[1/7] Enter your GitHub repository URL${NC}"
echo -e "Example: https://github.com/username/partner-app-qa.git"
read -p "GitHub URL: " GITHUB_URL

if [ -z "$GITHUB_URL" ]; then
    echo -e "${RED}✗ GitHub URL is required${NC}"
    exit 1
fi

# ============================================================================
# STEP 2: Get Git User Configuration
# ============================================================================

echo -e "\n${YELLOW}[2/7] Configure Git user${NC}"
read -p "Git user name (e.g., John Doe): " GIT_NAME
read -p "Git user email (e.g., john@example.com): " GIT_EMAIL

# ============================================================================
# STEP 3: Initialize Repository
# ============================================================================

echo -e "\n${YELLOW}[3/7] Initializing Git repository${NC}"

if [ -d ".git" ]; then
    echo -e "${GREEN}✓ Git already initialized${NC}"
else
    git init
    echo -e "${GREEN}✓ Git repository initialized${NC}"
fi

# ============================================================================
# STEP 4: Configure Git User
# ============================================================================

echo -e "\n${YELLOW}[4/7] Configuring Git user${NC}"
git config user.name "$GIT_NAME"
git config user.email "$GIT_EMAIL"
echo -e "${GREEN}✓ Git user configured${NC}"

# ============================================================================
# STEP 5: Add All Files
# ============================================================================

echo -e "\n${YELLOW}[5/7] Staging all files${NC}"
git add .
echo -e "${GREEN}✓ Files staged${NC}"

# Show status
echo -e "\n${BLUE}Files to commit:${NC}"
git status --short | head -20
echo "..."

# ============================================================================
# STEP 6: Create Initial Commit
# ============================================================================

echo -e "\n${YELLOW}[6/7] Creating initial commit${NC}"
git commit -m "Initial commit: Enterprise QA Automation Framework

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

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"

echo -e "${GREEN}✓ Initial commit created${NC}"

# ============================================================================
# STEP 7: Push to GitHub
# ============================================================================

echo -e "\n${YELLOW}[7/7] Pushing to GitHub${NC}"
echo -e "Repository: ${BLUE}${GITHUB_URL}${NC}"

# Remove existing remote if it exists
git remote remove origin 2>/dev/null || true

# Add new remote
git remote add origin "$GITHUB_URL"

# Rename branch to main if needed
git branch -M main

# Push to GitHub
if git push -u origin main; then
    echo -e "${GREEN}✓ Successfully pushed to GitHub${NC}"
else
    echo -e "${RED}✗ Failed to push to GitHub${NC}"
    echo -e "Troubleshooting:"
    echo -e "  1. Check repository URL is correct"
    echo -e "  2. Verify GitHub credentials (use Personal Access Token for HTTPS)"
    echo -e "  3. For SSH, ensure SSH key is configured"
    exit 1
fi

# ============================================================================
# Summary
# ============================================================================

echo -e "\n${BLUE}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                    Push Complete!                             ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════════╝${NC}"

echo -e "\n${GREEN}✓ Framework successfully pushed to GitHub${NC}"
echo -e "\n${BLUE}Next Steps:${NC}"
echo -e "  1. Visit: https://github.com/$(echo $GITHUB_URL | sed 's/.*\///' | sed 's/.git$//')"
echo -e "  2. Verify all files are present"
echo -e "  3. Check GitHub Actions for pipeline status"
echo -e "  4. Configure repository secrets if needed"
echo -e "  5. Start development!"

echo -e "\n${BLUE}Useful Commands:${NC}"
echo -e "  git log --oneline          # View commit history"
echo -e "  git branch -a              # List all branches"
echo -e "  git status                 # Check repository status"
echo -e "  git pull origin main       # Pull latest changes"

echo ""
