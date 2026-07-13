# 🛠️ Repository Reorganization - Migration Guide

## Overview

This guide helps you reorganize the repository from a flat structure into an enterprise-level organization.

## Current vs. New Structure

### Before (Flat Structure)
```
AI-Powered-Talent-Intelligence-System/
├── README.md
├── app.py
├── app.yaml
├── config.py
├── data_loader.py
├── evidence.py
├── recommendation.py
├── scoring_pipeline.py
├── ui_components.py
├── TRIGGER_PIPELINE.py
├── env.example.py
├── requirements.txt
├── gitignore
├── bi-encoder and cross encoder (notebook)
└── Query features (notebook)
```

### After (Organized Structure)
```
AI-Powered-Talent-Intelligence-System/
├── README.md                  # ✅ Stay at root
├── app.py                     # ✅ Stay at root
├── app.yaml                   # ✅ Stay at root
├── requirements.txt           # ✅ Stay at root
├── .gitignore                 # ✅ Renamed from 'gitignore'
│
├── src/                       # 📦 NEW: Core modules
│   ├── config.py
│   ├── data_loader.py
│   ├── evidence.py
│   ├── recommendation.py
│   ├── scoring_pipeline.py
│   └── ui_components.py
│
├── config/                    # 📦 NEW: Config templates
│   └── env.example.py
│
├── scripts/                   # 📦 NEW: Utility scripts
│   └── trigger_pipeline.py
│
├── notebooks/                 # 📦 NEW: Analysis notebooks
│   ├── 02_feature_engineering.py
│   └── 03_embeddings_and_reranking.py
│
└── docs/                      # 📦 NEW: Documentation
    ├── FILE_STRUCTURE.md
    ├── ARCHITECTURE.md
    ├── DEPLOYMENT.md
    └── API_REFERENCE.md
```

---

## Step-by-Step Migration

### Step 1: Rename gitignore to .gitignore

The file is currently named `gitignore` but needs to start with a dot.

```bash
cd AI-Powered-Talent-Intelligence-System
git mv gitignore .gitignore
```

---

### Step 2: Move files to src/

Move core application modules:

```bash
git mv config.py src/config.py
git mv data_loader.py src/data_loader.py
git mv evidence.py src/evidence.py
git mv recommendation.py src/recommendation.py
git mv scoring_pipeline.py src/scoring_pipeline.py
git mv ui_components.py src/ui_components.py
```

**Why**: Organizes business logic into a dedicated module directory

---

### Step 3: Move env template to config/

```bash
git mv env.example.py config/env.example.py
```

**Why**: Separates configuration templates from application code

---

### Step 4: Move script to scripts/

```bash
git mv TRIGGER_PIPELINE.py scripts/trigger_pipeline.py
```

**Why**: Groups operational scripts separately from core modules  
**Note**: Also renamed to lowercase for consistency

---

### Step 5: Move notebooks to notebooks/

```bash
git mv "bi-encoder and cross encoder" notebooks/03_embeddings_and_reranking.py
git mv "Query features" notebooks/02_feature_engineering.py
```

**Why**: Groups all notebooks together with numbered prefixes  
**Note**: Renamed for clarity and execution order

---

### Step 6: Update import statements in app.py

After moving files to `src/`, update imports in `app.py`:

#### Before:
```python
import config
from data_loader import load_candidates
from ui_components import render_candidate
from recommendation import generate_summary
```

#### After:
```python
from src import config
from src.data_loader import load_candidates
from src.ui_components import render_candidate
from src.recommendation import generate_summary
```

---

### Step 7: Create __init__.py in src/

Make `src/` a proper Python package:

```bash
touch src/__init__.py
git add src/__init__.py
```

Contents of `src/__init__.py`:
```python
"""Core application modules for AI-Powered Talent Intelligence System."""

__version__ = "1.0.0"
```

---

### Step 8: Update requirements.txt (if needed)

No changes needed since modules are still in the same repo.

---

### Step 9: Commit the reorganization

```bash
git status  # Review changes

git commit -m "Reorganize repo into enterprise structure

- Move core modules to src/
- Move config template to config/
- Move utility script to scripts/
- Move notebooks to notebooks/ with numbered prefixes
- Rename gitignore to .gitignore
- Add docs/FILE_STRUCTURE.md with comprehensive explanations
- Update import statements in app.py

See docs/FILE_STRUCTURE.md for complete structure documentation."

git push origin main
```

---

## Verification Checklist

After migration, verify:

- [ ] All files moved to correct directories
- [ ] `app.py` imports updated and tested
- [ ] `.gitignore` starts with dot (not `gitignore`)
- [ ] `src/__init__.py` created
- [ ] Streamlit app runs: `streamlit run app.py`
- [ ] No broken imports or missing modules
- [ ] Git status shows clean working tree
- [ ] Changes pushed to GitHub

---

## Rollback Plan

If something breaks, rollback with:

```bash
git reset --hard HEAD~1  # Undo last commit
git push --force origin main  # Force push (use carefully!)
```

Or restore specific files:

```bash
git checkout HEAD~1 -- app.py  # Restore old app.py
```

---

## Post-Migration

### Update CI/CD pipelines (if any)

Update any automated deployment scripts to reference new paths:
- `src/config.py` instead of `config.py`
- `scripts/trigger_pipeline.py` instead of `TRIGGER_PIPELINE.py`

### Update documentation references

Update any external documentation pointing to old file paths.

### Notify team members

Alert collaborators to pull latest changes and update their imports.

---

## Benefits of New Structure

✅ **Clearer organization** - Files grouped by purpose  
✅ **Easier onboarding** - New developers understand structure immediately  
✅ **Better maintainability** - Logical separation of concerns  
✅ **Standard conventions** - Follows Python best practices  
✅ **Scalability** - Easy to add new modules in appropriate directories  
✅ **Professional appearance** - Enterprise-ready repository structure

---

## Need Help?

Refer to:
- `docs/FILE_STRUCTURE.md` - Comprehensive file explanations
- `README.md` - Updated quick start guide
- GitHub Issues - Report migration problems

---

**Migration Date**: 2026-07-13  
**Performed by**: Shivani Kanodia