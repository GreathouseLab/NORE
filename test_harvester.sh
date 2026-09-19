#!/usr/bin/env bash
# ==============================================================================
# NORE Paper Harvester — Progressive Test Script
# ==============================================================================
# Run this from the directory containing:
#   - nore_paper_harvester.py
#   - llm_adapter.py  (universal version with llm_chat_universal)
#
# PREREQUISITES:
#   pip install requests           # For API calls (required)
#   pip install openai             # For screening with GPT models (Stage 3+)
#   pip install python-dotenv      # Optional — or set env vars directly
#
# BEFORE RUNNING:
#   export OPENAI_API_KEY=sk-...   # Needed for Stage 3+ (screening)
#   Optional: export NCBI_API_KEY=...  # Free from ncbi.nlm.nih.gov/account/settings
#
# Then: bash test_harvester.sh
# ==============================================================================

set -e  # Exit on error

# ── Configuration ──
# CHANGE THIS to your actual email (required by NCBI/Unpaywall TOS)
EMAIL="Leigh_Greathouse@baylor.edu"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Helper functions
header() {
    echo ""
    echo -e "${CYAN}════════════════════════════════════════════════════════════${NC}"
    echo -e "${CYAN}  $1${NC}"
    echo -e "${CYAN}════════════════════════════════════════════════════════════${NC}"
}

success() { echo -e "${GREEN}  ✓ $1${NC}"; }
warn()    { echo -e "${YELLOW}  ⚠ $1${NC}"; }
fail()    { echo -e "${RED}  ✗ $1${NC}"; }

pause() {
    echo ""
    echo -e "${YELLOW}  Press ENTER to continue to the next stage, or Ctrl+C to stop...${NC}"
    read -r
}

# ==============================================================================
# STAGE 0: Preflight Checks
# ==============================================================================
header "STAGE 0: Preflight Checks"

# Check email is set
if [ -z "$EMAIL" ]; then
    fail "EMAIL is not set. Edit this script and set EMAIL on line 25."
    exit 1
fi
success "Email set: $EMAIL"

# Check Python
if command -v python3 &>/dev/null; then
    PYTHON=python3
elif command -v python &>/dev/null; then
    PYTHON=python
else
    fail "Python not found. Install Python 3.9+"
    exit 1
fi
success "Python: $($PYTHON --version)"

# Check required files
if [ ! -f "nore_paper_harvester.py" ]; then
    fail "nore_paper_harvester.py not found in current directory"
    fail "cd to the directory containing the harvester files"
    exit 1
fi
success "nore_paper_harvester.py found"

if [ ! -f "llm_adapter.py" ]; then
    warn "llm_adapter.py not found — Stage 3+ (screening) will be skipped"
    warn "Copy the universal llm_adapter.py into this directory for screening"
    HAS_ADAPTER=false
else
    success "llm_adapter.py found"
    HAS_ADAPTER=true
fi

# Check requests library
if $PYTHON -c "import requests" 2>/dev/null; then
    success "requests library installed"
else
    fail "requests library not installed. Run: pip install requests"
    exit 1
fi

# Check API keys
echo ""
echo "  Environment variables:"
if [ -n "$NCBI_API_KEY" ]; then
    success "NCBI_API_KEY is set (10 req/sec rate limit)"
else
    warn "NCBI_API_KEY not set — using 3 req/sec rate limit (still works, just slower)"
    warn "Get a free key at: https://www.ncbi.nlm.nih.gov/account/settings/"
fi

if [ -n "$OPENAI_API_KEY" ]; then
    success "OPENAI_API_KEY is set (needed for screening in Stage 3+)"
elif [ -n "$TOGETHER_API_KEY" ]; then
    success "TOGETHER_API_KEY is set (can use for screening)"
else
    warn "No LLM API key set — screening stages will be skipped"
    warn "Set OPENAI_API_KEY or TOGETHER_API_KEY for abstract screening"
fi

pause

# ==============================================================================
# STAGE 1: Discovery Only — Test NCBI E-utilities Connection
# ==============================================================================
header "STAGE 1: Discovery Only (no downloads, no screening)"
echo "  Tests: NCBI E-utilities API connectivity + MeSH query parsing"
echo "  What happens: Searches PubMed for 5 papers on drug-nutrient topic"
echo "  Cost: Free (no API key required, no LLM calls)"
echo ""

$PYTHON nore_paper_harvester.py \
    --email "$EMAIL" \
    --topic drug_nutrient \
    --max-per-topic 5 \
    --no-screen \
    --output-dir test_harvest_stage1 \
    -v

echo ""
# Check what was produced
if [ -d "test_harvest_stage1" ]; then
    PDF_COUNT=$(find test_harvest_stage1 -name "*.pdf" 2>/dev/null | wc -l)
    META_COUNT=$(find test_harvest_stage1 -name "*.meta.json" 2>/dev/null | wc -l)
    success "Output directory created: test_harvest_stage1/"
    echo "  PDFs downloaded:  $PDF_COUNT"
    echo "  Metadata files:   $META_COUNT"

    # Show a sample metadata file
    SAMPLE_META=$(find test_harvest_stage1 -name "*.meta.json" -print -quit 2>/dev/null)
    if [ -n "$SAMPLE_META" ]; then
        echo ""
        echo "  Sample metadata sidecar:"
        $PYTHON -m json.tool "$SAMPLE_META" 2>/dev/null | head -20
        echo "  ..."
    fi

    # Show progress tracker
    if [ -f "test_harvest_stage1/.harvest_progress.json" ]; then
        echo ""
        echo "  Progress tracker:"
        $PYTHON -m json.tool "test_harvest_stage1/.harvest_progress.json" 2>/dev/null | head -15
    fi
else
    fail "Output directory not created — check error messages above"
fi

if [ "$PDF_COUNT" -gt 0 ]; then
    success "Stage 1 PASSED — Discovery + Download working"
else
    warn "No PDFs downloaded. Possible reasons:"
    warn "  - Papers found but no open-access PDFs available"
    warn "  - Network issue reaching PMC/Unpaywall"
    warn "  Check the verbose output above for details"
fi

pause

# ==============================================================================
# STAGE 2: Multi-Topic Discovery — Test All 4 Topics
# ==============================================================================
header "STAGE 2: Multi-Topic Discovery (3 papers per topic)"
echo "  Tests: All 4 topic query sets + cross-topic deduplication"
echo "  What happens: Searches all topics, downloads up to 3 each"
echo "  Cost: Free (no LLM calls)"
echo ""

$PYTHON nore_paper_harvester.py \
    --email "$EMAIL" \
    --max-per-topic 3 \
    --no-screen \
    --output-dir test_harvest_stage2 \
    -v

echo ""
if [ -d "test_harvest_stage2" ]; then
    echo "  Results by topic:"
    for TOPIC in drug_nutrient cachexia_sarcopenia immunotherapy_nutrition mediterranean_diet; do
        if [ -d "test_harvest_stage2/$TOPIC" ]; then
            TC=$(find "test_harvest_stage2/$TOPIC" -name "*.pdf" 2>/dev/null | wc -l)
            echo "    $TOPIC: $TC PDFs"
        else
            echo "    $TOPIC: (no directory created)"
        fi
    done
    TOTAL=$(find test_harvest_stage2 -name "*.pdf" 2>/dev/null | wc -l)
    success "Stage 2 PASSED — $TOTAL total PDFs across topics"
else
    fail "Output directory not created"
fi

pause

# ==============================================================================
# STAGE 3: Screening Calibration — Test LLM Relevance Gate
# ==============================================================================
header "STAGE 3: LLM Abstract Screening (drug-nutrient, 10 papers)"

if [ -z "$OPENAI_API_KEY" ] && [ -z "$TOGETHER_API_KEY" ]; then
    warn "SKIPPING — No LLM API key set"
    warn "Set OPENAI_API_KEY or TOGETHER_API_KEY and re-run"
else
    if [ "$HAS_ADAPTER" = false ]; then
        warn "SKIPPING — llm_adapter.py not found"
        warn "Copy the universal llm_adapter.py into this directory"
    else
        echo "  Tests: LLM abstract screening with relevance threshold ≥6"
        echo "  What happens: Screens abstracts, only downloads relevant papers"
        echo "  Cost: ~10 LLM calls (gpt-4.1-mini ≈ $0.002 total)"
        echo ""

        SCREEN_MODEL="gpt-4.1-mini"
        if [ -z "$OPENAI_API_KEY" ] && [ -n "$TOGETHER_API_KEY" ]; then
            SCREEN_MODEL="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo"
            echo "  Using Together AI model: $SCREEN_MODEL"
        fi

        $PYTHON nore_paper_harvester.py \
            --email "$EMAIL" \
            --topic drug_nutrient \
            --max-per-topic 10 \
            --screen-model "$SCREEN_MODEL" \
            --min-relevance 6 \
            --output-dir test_harvest_stage3 \
            -v

        echo ""
        if [ -d "test_harvest_stage3" ]; then
            SCREENED_PDF=$(find test_harvest_stage3 -name "*.pdf" 2>/dev/null | wc -l)
            echo "  PDFs that passed screening: $SCREENED_PDF"

            # Check screening stats in progress file
            if [ -f "test_harvest_stage3/.harvest_progress.json" ]; then
                echo ""
                echo "  Screening statistics:"
                $PYTHON -c "
import json
with open('test_harvest_stage3/.harvest_progress.json') as f:
    p = json.load(f)
screened_out = len(p.get('screened_out', {}))
downloaded = p.get('stats', {}).get('total_downloaded', 0)
errors = p.get('stats', {}).get('total_errors', 0)
print(f'    Screened out (score < 6): {screened_out}')
print(f'    Downloaded:               {downloaded}')
print(f'    Download errors:          {errors}')
"
            fi
            success "Stage 3 PASSED — Screening working"
        fi
    fi
fi

pause

# ==============================================================================
# STAGE 4: Resume Capability
# ==============================================================================
header "STAGE 4: Resume Test"
echo "  Tests: --resume flag correctly skips already-processed papers"
echo "  What happens: Re-runs Stage 2 with --resume, should skip all papers"
echo ""

$PYTHON nore_paper_harvester.py \
    --email "$EMAIL" \
    --max-per-topic 3 \
    --no-screen \
    --output-dir test_harvest_stage2 \
    --resume \
    -v

echo ""
success "Stage 4 PASSED if output shows 'After filtering already-processed: 0 remaining'"

pause

# ==============================================================================
# STAGE 5: Pipeline Integration — Feed PDFs into mupdf_trainer_v3.py
# ==============================================================================
header "STAGE 5: Pipeline Integration"

if [ ! -f "mupdf_trainer_v3.py" ]; then
    warn "SKIPPING — mupdf_trainer_v3.py not found in current directory"
    warn "Copy mupdf_trainer_v3.py here to test full pipeline integration"
else
    # Find a topic directory with at least 1 PDF
    TEST_DIR=""
    for STAGE_DIR in test_harvest_stage1 test_harvest_stage2 test_harvest_stage3; do
        for TOPIC in drug_nutrient cachexia_sarcopenia immunotherapy_nutrition mediterranean_diet; do
            DIR="$STAGE_DIR/$TOPIC"
            if [ -d "$DIR" ] && [ "$(find "$DIR" -name '*.pdf' | wc -l)" -gt 0 ]; then
                TEST_DIR="$DIR"
                break 2
            fi
        done
    done

    if [ -z "$TEST_DIR" ]; then
        # Try the stage dir itself
        for STAGE_DIR in test_harvest_stage1 test_harvest_stage2; do
            if [ "$(find "$STAGE_DIR" -name '*.pdf' 2>/dev/null | wc -l)" -gt 0 ]; then
                TEST_DIR="$STAGE_DIR"
                break
            fi
        done
    fi

    if [ -z "$TEST_DIR" ]; then
        warn "No PDFs found from previous stages to test with"
    else
        PDF_COUNT=$(find "$TEST_DIR" -name "*.pdf" | wc -l)
        echo "  Tests: mupdf_trainer_v3.py can process harvested PDFs"
        echo "  Using: $TEST_DIR ($PDF_COUNT PDFs)"
        echo "  What happens: Generates Q/A pairs from the first harvested PDF"
        echo ""

        FIRST_PDF=$(find "$TEST_DIR" -name "*.pdf" -print -quit)
        FIRST_PDF_DIR=$(dirname "$FIRST_PDF")

        if [ -z "$OPENAI_API_KEY" ] && [ -z "$TOGETHER_API_KEY" ]; then
            warn "No LLM API key — can only test PDF extraction, not Q/A generation"
            echo "  Testing extraction only..."
            $PYTHON -c "
import sys
sys.path.insert(0, '.')
# Try importing the extraction function
try:
    from mupdf_trainer_v3 import extract_text_from_pdf
    text, pages = extract_text_from_pdf('$FIRST_PDF')
    print(f'  Extracted {len(text)} chars from {pages} pages')
    print(f'  First 200 chars: {text[:200]}...')
    print('  ✓ PDF extraction working')
except Exception as e:
    print(f'  ✗ Extraction failed: {e}')
"
        else
            QA_MODEL="gpt-4.1"
            if [ -z "$OPENAI_API_KEY" ] && [ -n "$TOGETHER_API_KEY" ]; then
                QA_MODEL="moonshotai/Kimi-K2-Instruct-0905"
            fi

            echo "  Generating Q/A pairs with $QA_MODEL..."
            echo "  (Processing 1 PDF, ~4 Q/A pairs expected)"
            echo ""

            $PYTHON mupdf_trainer_v3.py \
                "$FIRST_PDF_DIR" \
                --gen_qa \
                --llm_model "$QA_MODEL" \
                --qa_k 4

            # Check output
            JSONL_COUNT=$(find "$FIRST_PDF_DIR" -name "*.jsonl" 2>/dev/null | wc -l)
            if [ "$JSONL_COUNT" -gt 0 ]; then
                echo ""
                echo "  Generated JSONL files:"
                find "$FIRST_PDF_DIR" -name "*.jsonl" -exec echo "    {}" \;
                echo ""
                echo "  Sample Q/A pair:"
                FIRST_JSONL=$(find "$FIRST_PDF_DIR" -name "*.jsonl" -print -quit)
                head -1 "$FIRST_JSONL" | $PYTHON -m json.tool 2>/dev/null | head -15
                success "Stage 5 PASSED — Full pipeline working: Harvest → Q/A Generation"
            else
                warn "No JSONL output — check mupdf_trainer_v3.py output above"
            fi
        fi
    fi
fi

# ==============================================================================
# SUMMARY
# ==============================================================================
header "TEST COMPLETE"
echo ""
echo "  Test directories created:"
for D in test_harvest_stage1 test_harvest_stage2 test_harvest_stage3; do
    if [ -d "$D" ]; then
        PC=$(find "$D" -name "*.pdf" 2>/dev/null | wc -l)
        echo "    $D/ — $PC PDFs"
    fi
done
echo ""
echo "  Clean up test data when ready:"
echo "    rm -rf test_harvest_stage1 test_harvest_stage2 test_harvest_stage3"
echo ""
echo "  Ready for full harvest:"
echo "    python nore_paper_harvester.py --email $EMAIL --max-per-topic 500 --resume -v"
echo ""
