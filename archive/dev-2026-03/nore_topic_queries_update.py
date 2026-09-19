#!/usr/bin/env python3
"""
NORE Paper Harvester — Topic Query Update (March 2026)
======================================================

INSTRUCTIONS:
  In nore_paper_harvester.py, replace ONLY the immunotherapy_nutrition and
  mediterranean_diet entries inside TOPIC_QUERIES with ALL of the entries below.

  Specifically, delete everything from:
      "immunotherapy_nutrition": {
  down through the closing of:
      "mediterranean_diet": { ... },
  }                               <-- and this final closing brace of TOPIC_QUERIES

  Then paste the contents of NEW_TOPICS below in its place, followed by }

  Your final TOPIC_QUERIES dict should have 6 keys:
    1. drug_nutrient               (unchanged)
    2. cachexia_sarcopenia          (unchanged)
    3. immunotherapy_nutrition      (UPDATED - microbiome queries removed)
    4. cancer_malnutrition          (NEW)
    5. dietary_patterns             (NEW - replaces mediterranean_diet)
    6. microbiome_diet_cancer       (NEW)
"""

# ═══════════════════════════════════════════════════════════════
# REPLACEMENT STARTS HERE — paste into TOPIC_QUERIES dict
# ═══════════════════════════════════════════════════════════════

NEW_TOPICS = {

    # ═══════════════════════════════════════════════════════════════
    #  TOPIC 3: Immunotherapy & Nutrition (UPDATED)
    #  REMOVED: Microbiome queries (moved to Topic 6)
    #  MeSH qualifiers: /immunology, /adverse effects, /diet therapy
    # ═══════════════════════════════════════════════════════════════
    "immunotherapy_nutrition": {
        "label": "Immunotherapy & Nutrition",
        "priority": 3,
        "queries": [
            # Immunotherapy + nutritional status in cancer
            '"Immunotherapy"[MeSH] AND "Nutritional Status"[MeSH] AND "Neoplasms"[MeSH]',
            # Immune checkpoint inhibitors + diet/nutrition therapy
            '"Immune Checkpoint Inhibitors"[MeSH] AND ("Nutrition Therapy"[MeSH] OR "Diet"[MeSH] OR "Nutritional Status"[MeSH])',
            # Cancer immunology + immunotherapy + body composition/malnutrition
            '"Neoplasms/immunology"[MeSH] AND "Immunotherapy"[MeSH] AND ("Body Composition"[MeSH] OR "Body Mass Index"[MeSH] OR "Malnutrition"[MeSH])',
            # Cachexia/sarcopenia impacting immunotherapy outcomes
            '("Cachexia"[MeSH] OR "Sarcopenia"[MeSH]) AND "Immune Checkpoint Inhibitors"[MeSH] AND "Neoplasms"[MeSH]',
            # Dietary supplements during immunotherapy — /therapeutic use + /adverse effects
            '"Dietary Supplements/therapeutic use"[MeSH] AND "Immunotherapy/adverse effects"[MeSH] AND "Neoplasms"[MeSH]',
            # Cancer diet therapy + immune system
            '"Neoplasms/diet therapy"[MeSH] AND ("Immunity"[MeSH] OR "Immune System"[MeSH])',
            # Obesity/BMI effect on immunotherapy response
            '("Obesity"[MeSH] OR "Body Mass Index"[MeSH]) AND "Immune Checkpoint Inhibitors"[MeSH] AND "Treatment Outcome"[MeSH]',
            # Nutritional intervention during immunotherapy adverse events (colitis, etc.)
            '"Immunotherapy/adverse effects"[MeSH] AND ("Nutrition Therapy"[MeSH] OR "Nutritional Support"[MeSH]) AND "Neoplasms"[MeSH]',
        ],
        "europe_pmc_queries": [
            '(TITLE_ABS:"immunotherapy" OR TITLE_ABS:"checkpoint inhibitor") AND (TITLE_ABS:"nutrition" OR TITLE_ABS:"diet") AND (TITLE_ABS:"cancer") AND (OPEN_ACCESS:y)',
            '(TITLE_ABS:"immune checkpoint") AND (TITLE_ABS:"nutritional status" OR TITLE_ABS:"body composition" OR TITLE_ABS:"sarcopenia") AND (OPEN_ACCESS:y)',
            '(TITLE_ABS:"immunotherapy") AND (TITLE_ABS:"obesity" OR TITLE_ABS:"BMI") AND (TITLE_ABS:"cancer outcome" OR TITLE_ABS:"treatment response") AND (OPEN_ACCESS:y)',
        ]
    },

    # ═══════════════════════════════════════════════════════════════
    #  TOPIC 4: Cancer Malnutrition — Screening, Assessment & Intervention (NEW)
    #  The foundational clinical topic — affects 20-70% of cancer patients.
    #  MeSH qualifiers: /diagnosis, /diet therapy, /therapy, /prevention & control
    # ═══════════════════════════════════════════════════════════════
    "cancer_malnutrition": {
        "label": "Cancer Malnutrition: Screening, Assessment & Intervention",
        "priority": 2,
        "queries": [
            # Malnutrition + cancer — direct nutritional treatment
            '"Malnutrition/diet therapy"[MeSH] AND "Neoplasms"[MeSH]',
            # Malnutrition diagnosis/screening in cancer — PG-SGA, NRS-2002, MUST, GLIM
            '"Malnutrition/diagnosis"[MeSH] AND "Neoplasms"[MeSH]',
            # Nutrition assessment in cancer (broad — captures all screening tools)
            '"Nutrition Assessment"[MeSH] AND "Neoplasms"[MeSH]',
            # Nutritional support interventions in cancer — ONS, enteral, parenteral
            '"Nutritional Support"[MeSH] AND "Neoplasms/diet therapy"[MeSH]',
            # Enteral nutrition in cancer — tube feeding, ONS during treatment
            '"Enteral Nutrition"[MeSH] AND "Neoplasms"[MeSH]',
            # Parenteral nutrition in cancer — when enteral is not possible
            '"Parenteral Nutrition"[MeSH] AND "Neoplasms"[MeSH]',
            # Perioperative nutrition — pre/post-surgical optimization in cancer
            '("Preoperative Care"[MeSH] OR "Postoperative Care"[MeSH]) AND "Nutritional Status"[MeSH] AND "Neoplasms"[MeSH]',
            # Malnutrition impact on treatment tolerance and outcomes
            '"Malnutrition"[MeSH] AND "Neoplasms/therapy"[MeSH] AND ("Treatment Outcome"[MeSH] OR "Patient Outcome Assessment"[MeSH])',
        ],
        "europe_pmc_queries": [
            '(TITLE_ABS:"malnutrition" OR TITLE_ABS:"nutritional screening") AND (TITLE_ABS:"cancer") AND (TITLE_ABS:"assessment" OR TITLE_ABS:"PG-SGA" OR TITLE_ABS:"GLIM") AND (OPEN_ACCESS:y)',
            '(TITLE_ABS:"nutritional support" OR TITLE_ABS:"oral nutritional supplement") AND (TITLE_ABS:"cancer" OR TITLE_ABS:"oncology") AND (OPEN_ACCESS:y)',
            '(TITLE_ABS:"perioperative nutrition" OR TITLE_ABS:"prehabilitation") AND (TITLE_ABS:"cancer" OR TITLE_ABS:"surgery") AND (TITLE_ABS:"nutritional") AND (OPEN_ACCESS:y)',
        ]
    },

    # ═══════════════════════════════════════════════════════════════
    #  TOPIC 5: Dietary Patterns in Cancer (NEW — replaces Mediterranean-only)
    #  Covers: Mediterranean, ketogenic, fasting/TRE/FMD, plant-based,
    #          anti-inflammatory, dietary inflammatory index
    #  MeSH qualifiers: /prevention & control, /diet therapy, /mortality,
    #                    /therapeutic use, /adverse effects
    # ═══════════════════════════════════════════════════════════════
    "dietary_patterns": {
        "label": "Dietary Patterns in Cancer",
        "priority": 4,
        "queries": [
            # Mediterranean diet + cancer (retained from old topic)
            '"Diet, Mediterranean"[Majr] AND "Neoplasms"[MeSH]',
            # Ketogenic diet + cancer — metabolic targeting, Warburg effect
            '"Diet, Ketogenic"[MeSH] AND "Neoplasms"[MeSH]',
            # Ketogenic diet during cancer treatment — adjuvant role
            '"Diet, Ketogenic"[MeSH] AND "Neoplasms/diet therapy"[MeSH]',
            # Intermittent fasting + cancer — chemo sensitization, metabolic switching
            '"Intermittent Fasting"[MeSH] AND "Neoplasms"[MeSH]',
            # Fasting + cancer treatment — fasting-mimicking diet, short-term fasting
            '"Fasting"[MeSH] AND "Neoplasms/diet therapy"[MeSH]',
            # Caloric restriction + cancer — prevention and treatment
            '"Caloric Restriction"[MeSH] AND "Neoplasms"[MeSH]',
            # Anti-inflammatory dietary pattern + cancer outcomes
            '"Inflammation"[MeSH] AND "Diet"[MeSH] AND "Neoplasms/diet therapy"[MeSH]',
            # Plant-based / vegetarian diet + cancer
            '("Diet, Vegetarian"[MeSH] OR "Diet, Vegan"[MeSH]) AND "Neoplasms"[MeSH]',
        ],
        "europe_pmc_queries": [
            '(TITLE_ABS:"ketogenic diet") AND (TITLE_ABS:"cancer" OR TITLE_ABS:"glioblastoma" OR TITLE_ABS:"tumor") AND (OPEN_ACCESS:y)',
            '(TITLE_ABS:"intermittent fasting" OR TITLE_ABS:"time-restricted eating" OR TITLE_ABS:"fasting-mimicking") AND (TITLE_ABS:"cancer") AND (OPEN_ACCESS:y)',
            '(TITLE_ABS:"Mediterranean diet" OR TITLE_ABS:"anti-inflammatory diet" OR TITLE_ABS:"dietary inflammatory index") AND (TITLE_ABS:"cancer") AND (OPEN_ACCESS:y)',
        ]
    },

    # ═══════════════════════════════════════════════════════════════
    #  TOPIC 6: Microbiome, Diet & Cancer Outcomes (NEW — split from immunotherapy)
    #  The microbiome-diet connection extends beyond immunotherapy to chemo
    #  response, radiation enteritis, GVHD, and surgical recovery.
    #  MeSH qualifiers: /drug effects, /therapeutic use, /diet therapy
    # ═══════════════════════════════════════════════════════════════
    "microbiome_diet_cancer": {
        "label": "Microbiome, Diet & Cancer Outcomes",
        "priority": 5,
        "queries": [
            # Gut microbiome + diet + cancer (broadest capture)
            '"Gastrointestinal Microbiome"[MeSH] AND "Diet"[MeSH] AND "Neoplasms"[MeSH]',
            # Microbiome modulation through diet affecting cancer immune response
            # (moved from immunotherapy topic)
            '"Gastrointestinal Microbiome/drug effects"[MeSH] AND ("Diet"[MeSH] OR "Probiotics/therapeutic use"[MeSH]) AND "Neoplasms"[MeSH]',
            # Gut microbiome + immunotherapy + diet (moved from immunotherapy topic)
            '"Gastrointestinal Microbiome"[MeSH] AND "Immunotherapy"[MeSH] AND ("Diet"[MeSH] OR "Dietary Fiber"[MeSH])',
            # Probiotics/prebiotics during cancer treatment
            '("Probiotics/therapeutic use"[MeSH] OR "Prebiotics/therapeutic use"[MeSH]) AND "Neoplasms"[MeSH]',
            # Dietary fiber + microbiome + cancer (fiber as prebiotic modulator)
            '"Dietary Fiber"[MeSH] AND "Gastrointestinal Microbiome"[MeSH] AND "Neoplasms"[MeSH]',
            # Microbiome and chemotherapy response/toxicity
            '"Gastrointestinal Microbiome"[MeSH] AND "Antineoplastic Agents/adverse effects"[MeSH]',
            # Microbiome and radiation therapy — enteritis, gut damage recovery
            '"Gastrointestinal Microbiome"[MeSH] AND ("Radiation Injuries"[MeSH] OR "Radiotherapy"[MeSH]) AND ("Diet"[MeSH] OR "Probiotics"[MeSH])',
            # Dysbiosis + cancer + nutritional intervention
            '"Dysbiosis"[MeSH] AND "Neoplasms"[MeSH] AND ("Diet"[MeSH] OR "Nutrition Therapy"[MeSH])',
        ],
        "europe_pmc_queries": [
            '(TITLE_ABS:"gut microbiome" OR TITLE_ABS:"gut microbiota") AND (TITLE_ABS:"diet" OR TITLE_ABS:"fiber" OR TITLE_ABS:"prebiotic") AND (TITLE_ABS:"cancer") AND (OPEN_ACCESS:y)',
            '(TITLE_ABS:"probiotics" OR TITLE_ABS:"synbiotics") AND (TITLE_ABS:"cancer" OR TITLE_ABS:"chemotherapy") AND (TITLE_ABS:"nutrition" OR TITLE_ABS:"diet") AND (OPEN_ACCESS:y)',
            '(TITLE_ABS:"microbiome") AND (TITLE_ABS:"immunotherapy" OR TITLE_ABS:"checkpoint inhibitor") AND (TITLE_ABS:"diet" OR TITLE_ABS:"fiber") AND (OPEN_ACCESS:y)',
        ]
    },
}

# ═══════════════════════════════════════════════════════════════
# REPLACEMENT ENDS HERE
# ═══════════════════════════════════════════════════════════════


# ──────────────────────────────────────────────────────────────
# VALIDATION: Run this file standalone to verify all queries
# ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 70)
    print("NORE Topic Query Update — Validation Report")
    print("=" * 70)

    total_pubmed = 0
    total_epmc = 0
    total_mesh_qualifiers = 0

    for key, topic in NEW_TOPICS.items():
        pm = len(topic["queries"])
        ep = len(topic.get("europe_pmc_queries", []))
        total_pubmed += pm
        total_epmc += ep

        # Count MeSH qualifier usage
        qualifiers = 0
        for q in topic["queries"]:
            qualifiers += q.count("/")
        total_mesh_qualifiers += qualifiers

        print(f"\n  {topic['label']} (priority {topic['priority']})")
        print(f"    PubMed queries:     {pm}")
        print(f"    Europe PMC queries: {ep}")
        print(f"    MeSH qualifiers:    {qualifiers}")
        print(f"    Key: {key}")

    print(f"\n{'─' * 70}")
    print(f"  NEW/UPDATED TOPICS TOTAL:")
    print(f"    Topics:             {len(NEW_TOPICS)}")
    print(f"    PubMed queries:     {total_pubmed}")
    print(f"    Europe PMC queries: {total_epmc}")
    print(f"    MeSH qualifiers:    {total_mesh_qualifiers}")

    # Add the 2 unchanged topics for the full picture
    print(f"\n  FULL HARVESTER (including unchanged drug_nutrient + cachexia):")
    print(f"    Total topics:       {len(NEW_TOPICS) + 2}")
    print(f"    Total PubMed:       {total_pubmed + 16}  (+ 8 drug_nutrient + 8 cachexia)")
    print(f"    Total Europe PMC:   {total_epmc + 6}  (+ 3 drug_nutrient + 3 cachexia)")

    # List all MeSH headings used
    all_headings = set()
    import re
    for topic in NEW_TOPICS.values():
        for q in topic["queries"]:
            headings = re.findall(r'"([^"]+)"(?:\[MeSH\]|\[Majr\])', q)
            for h in headings:
                # Strip qualifier
                base = h.split("/")[0]
                all_headings.add(base)

    print(f"\n  UNIQUE MeSH HEADINGS USED (new topics only): {len(all_headings)}")
    for h in sorted(all_headings):
        print(f"    • {h}")

    print(f"\n{'═' * 70}")
    print("  Validation complete. Copy topics into nore_paper_harvester.py")
    print(f"{'═' * 70}")
