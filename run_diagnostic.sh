#!/usr/bin/env bash
# ==============================================================================
# NORE Harvester — Diagnostic Run
# Captures verbose output to debug PDF download failures
# ==============================================================================

# CHANGE THIS to your email
EMAIL="Leigh_Greathouse@baylor.edu"

echo "Running diagnostic harvest — drug_nutrient topic, 5 papers, verbose..."
echo "Output saved to: harvest_debug.txt"
echo ""

python3 nore_paper_harvester.py \
    --email "$EMAIL" \
    --topic drug_nutrient \
    --max-per-topic 5 \
    --no-screen \
    --output-dir test_debug \
    -v 2>&1 | tee harvest_debug.txt

echo ""
echo "════════════════════════════════════════════════════════"
echo "Done. Share harvest_debug.txt with Claude for diagnosis."
echo "════════════════════════════════════════════════════════"
