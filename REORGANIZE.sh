#!/bin/bash
# Enterprise Repository Reorganization Script
# This script reorganizes the AI-Powered Talent Intelligence System repo
# into an enterprise-level structure with proper folder organization

set -e  # Exit on error

echo "🛠️  Starting repository reorganization..."
echo "==========================================="

# Navigate to repo root
cd "$(dirname "$0")"

echo "
✅ Step 1: Rename gitignore to .gitignore"
git mv gitignore .gitignore 2>/dev/null || echo "Already renamed or doesn't exist"

echo "
✅ Step 2: Create src/ directory and move core modules"
mkdir -p src
touch src/__init__.py
cat > src/__init__.py << 'EOF'
"""Core application modules for AI-Powered Talent Intelligence System."""

__version__ = "1.0.0"
EOF

git mv config.py src/config.py 2>/dev/null || echo "config.py already moved"
git mv data_loader.py src/data_loader.py 2>/dev/null || echo "data_loader.py already moved"
git mv evidence.py src/evidence.py 2>/dev/null || echo "evidence.py already moved"
git mv recommendation.py src/recommendation.py 2>/dev/null || echo "recommendation.py already moved"
git mv scoring_pipeline.py src/scoring_pipeline.py 2>/dev/null || echo "scoring_pipeline.py already moved"
git mv ui_components.py src/ui_components.py 2>/dev/null || echo "ui_components.py already moved"

echo "
✅ Step 3: Create config/ directory and move template"
mkdir -p config
git mv env.example.py config/env.example.py 2>/dev/null || echo "env.example.py already moved"

echo "
✅ Step 4: Create scripts/ directory and move utility scripts"
mkdir -p scripts
git mv TRIGGER_PIPELINE.py scripts/trigger_pipeline.py 2>/dev/null || echo "TRIGGER_PIPELINE.py already moved"

echo "
✅ Step 5: Create notebooks/ directory and move notebooks"
mkdir -p notebooks
git mv "bi-encoder and cross encoder" notebooks/03_embeddings_and_reranking.py 2>/dev/null || echo "bi-encoder notebook already moved"
git mv "Query features" notebooks/02_feature_engineering.py 2>/dev/null || echo "Query features notebook already moved"

echo "
✅ Step 6: Ensure docs/ directory exists"
mkdir -p docs

echo "
✅ Step 7: Update app.py imports"
if [ -f "app.py" ]; then
    echo "Updating imports in app.py..."
    # Backup original
    cp app.py app.py.backup
    
    # Update imports (basic sed replacements - adjust if needed)
    sed -i.bak 's/^import config$/from src import config/g' app.py
    sed -i.bak 's/^from config import/from src.config import/g' app.py
    sed -i.bak 's/^from data_loader import/from src.data_loader import/g' app.py
    sed -i.bak 's/^from evidence import/from src.evidence import/g' app.py
    sed -i.bak 's/^from recommendation import/from src.recommendation import/g' app.py
    sed -i.bak 's/^from ui_components import/from src.ui_components import/g' app.py
    sed -i.bak 's/^from scoring_pipeline import/from src.scoring_pipeline import/g' app.py
    
    rm -f app.py.bak
    echo "Import statements updated!"
else
    echo "⚠️  app.py not found - skipping import updates"
fi

echo "
✅ Step 8: Check status"
git status

echo "
==========================================="
echo "🎉 Reorganization complete!"
echo ""
echo "Next steps:"
echo "1. Review changes: git status"
echo "2. Test the app: streamlit run app.py"
echo "3. Commit changes: git commit -m 'Reorganize repo into enterprise structure'"
echo "4. Push to GitHub: git push origin main"
echo ""
echo "See MIGRATION_GUIDE.md for detailed documentation."
echo "==========================================="