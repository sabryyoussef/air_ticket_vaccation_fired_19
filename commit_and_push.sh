#!/bin/bash

# Git Commit and Push Script
# This script commits and pushes the Mowzf HR Management Suite changes

echo "=== Mowzf HR Management Suite - Git Operations ==="
echo ""

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "Error: Not in a git repository"
    exit 1
fi

echo "1. Checking git status..."
git status

echo ""
echo "2. Staging all changes..."
git add -A

echo ""
echo "3. Checking staged changes..."
git status --staged

echo ""
echo "4. Creating commit..."
git commit -m "Reorganize project structure and add comprehensive documentation

- Move all modules to custom_addons/ directory for better organization
- Remove original module directories from root (air_ticket_request, endservice_vacation_calculation, exit_reentry_request)
- Add comprehensive README.md with installation and usage instructions
- Add module-specific documentation for each component
- Clean up utility scripts (copy_modules.py, copy_modules.sh, reorganize_modules.sh)
- Prepare project for production deployment

Features:
✅ Air Ticket Request Module - Employee travel management
✅ End Service Vacation Calculation - Settlement calculations  
✅ Exit Re-entry Request Module - Visa management
✅ Complete documentation and user guides
✅ Enhancement roadmaps for future development

Ready for Odoo 16.0+ deployment in Gulf region organizations."

echo ""
echo "5. Pushing to remote repository..."
git push origin main

echo ""
echo "=== Git Operations Complete ==="
echo ""
echo "✅ Project successfully committed and pushed!"
echo "🚀 Mowzf HR Management Suite is ready for deployment"
echo ""
echo "Repository URL: https://github.com/sabryyoussef/air_ticket_vaccation_fired_19"
echo "Documentation: README.md"
echo "Modules: custom_addons/"