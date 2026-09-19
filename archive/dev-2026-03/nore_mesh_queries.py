#!/usr/bin/env python3
"""
NORE Harvester — MeSH-Optimized Topic Queries
==============================================
All queries use proper MeSH controlled vocabulary with subheading qualifiers.

MeSH Qualifier Reference (from NLM official hierarchy):
  /diet therapy     (DH) — nutritional treatment of disease
  /drug therapy     (DT) — pharmacological treatment
  /therapy          (TH) — general therapy
  /adverse effects  (AE) — unwanted effects of substances
  /complications    (CO) — co-occurring conditions
  /prevention & control (PC) — preventive measures
  /metabolism       (ME) — metabolic processes
  /drug effects     (DE) — effects of drugs on processes
  /therapeutic use  (TU) — therapeutic application
  /immunology       (IM) — immune aspects
  /physiopathology  (PP) — pathological physiology
  /pharmacokinetics (PK) — ADME of substances

Key MeSH Headings Used:
  Nutrition:   "Nutrition Therapy", "Diet Therapy", "Nutritional Support",
               "Nutritional Status", "Diet", "Dietary Supplements", "Malnutrition"
  Oncology:    "Neoplasms", "Antineoplastic Agents", "Immunotherapy",
               "Immune Checkpoint Inhibitors"
  Body comp:   "Cachexia", "Sarcopenia", "Body Composition", "Muscle, Skeletal"
  GI/Immune:   "Gastrointestinal Microbiome", "Immunity"
  Diet patterns: "Diet, Mediterranean", "Diet, Food, and Nutrition"

Note: [MeSH] auto-explodes (includes all narrower terms in the tree).
      [MeSH:NoExp] prevents explosion (exact heading only).
      [Majr] limits to papers where this is a MAJOR topic (starred by indexer).
"""

TOPIC_QUERIES = {

    # ╔══════════════════════════════════════════════════════════════════╗
    # ║  TOPIC 1: Drug-Nutrient Interactions in Oncology               ║
    # ╚══════════════════════════════════════════════════════════════════╝
    "drug_nutrient": {
        "label": "Drug-Nutrient Interactions in Oncology",
        "priority": 1,
        "queries": [
            # Q1: Core MeSH heading — Food-Drug Interactions + Cancer
            # "Food-Drug Interactions"[MeSH] is the canonical heading for this entire field
            '"Food-Drug Interactions"[Majr] AND "Neoplasms"[MeSH]',

            # Q2: Herb-drug interactions with cancer drugs
            # /adverse effects qualifier targets papers about harmful interaction effects
            '"Herb-Drug Interactions"[MeSH] AND "Antineoplastic Agents/adverse effects"[MeSH]',

            # Q3: Cancer drug pharmacokinetics affected by diet/food
            # /pharmacokinetics targets absorption/metabolism studies
            '"Antineoplastic Agents/pharmacokinetics"[MeSH] AND ("Diet"[MeSH] OR "Food"[MeSH])',

            # Q4: Dietary supplements interacting with cancer therapy
            # /adverse effects on supplements + drug therapy qualifier on neoplasms
            '"Dietary Supplements/adverse effects"[MeSH] AND "Neoplasms/drug therapy"[MeSH]',

            # Q5: CYP enzyme system affected by dietary compounds in cancer context
            # /drug effects qualifier targets papers about how substances affect CYP
            '"Cytochrome P-450 Enzyme System/drug effects"[MeSH] AND ("Diet"[MeSH] OR "Dietary Supplements"[MeSH]) AND "Neoplasms"[MeSH]',

            # Q6: Drug interactions with nutritional support during cancer
            # /diet therapy on neoplasms narrows to papers about nutritional treatment OF cancer
            '"Drug Interactions"[MeSH] AND "Neoplasms/diet therapy"[MeSH]',

            # Q7: Specific high-risk supplements in oncology
            # Targets papers about known problematic supplements
            '("Curcumin/adverse effects"[MeSH] OR "Tea/adverse effects"[MeSH] OR "Grapefruit/adverse effects"[MeSH] OR "Hypericum/adverse effects"[MeSH]) AND "Neoplasms/drug therapy"[MeSH]',

            # Q8: Nutritional status affecting drug metabolism in cancer
            # /metabolism qualifier captures papers about how nutrition state changes drug processing
            '"Nutritional Status"[MeSH] AND "Antineoplastic Agents/pharmacokinetics"[MeSH]',
        ],
        "europe_pmc_queries": [
            '(TITLE_ABS:"food-drug interaction" OR TITLE_ABS:"drug-nutrient interaction") AND (TITLE_ABS:"cancer" OR TITLE_ABS:"oncology") AND (OPEN_ACCESS:y)',
            '(TITLE_ABS:"herb-drug interaction") AND (TITLE_ABS:"chemotherapy" OR TITLE_ABS:"antineoplastic") AND (OPEN_ACCESS:y)',
            '(TITLE_ABS:"dietary supplement" AND TITLE_ABS:"adverse" AND TITLE_ABS:"cancer treatment") AND (OPEN_ACCESS:y)',
        ]
    },

    # ╔══════════════════════════════════════════════════════════════════╗
    # ║  TOPIC 2: Cancer Cachexia & Sarcopenia                         ║
    # ╚══════════════════════════════════════════════════════════════════╝
    "cachexia_sarcopenia": {
        "label": "Cancer Cachexia & Sarcopenia",
        "priority": 2,
        "queries": [
            # Q1: Cachexia diet therapy — canonical query
            # /diet therapy is THE qualifier for nutritional treatment of cachexia
            '"Cachexia/diet therapy"[MeSH] AND "Neoplasms/complications"[MeSH]',

            # Q2: Cachexia general therapy (includes multimodal — nutrition + exercise + drugs)
            '"Cachexia/therapy"[MeSH] AND "Neoplasms/complications"[MeSH] AND ("Nutrition Therapy"[MeSH] OR "Nutritional Support"[MeSH])',

            # Q3: Sarcopenia + nutritional status in cancer
            # /physiopathology captures mechanism papers, /diet therapy captures interventions
            '"Sarcopenia"[MeSH] AND "Neoplasms"[MeSH] AND ("Nutritional Status"[MeSH] OR "Body Composition"[MeSH])',

            # Q4: Skeletal muscle pathology with nutrition in cancer
            # /drug effects on muscle targets papers about how nutritional agents affect muscle
            '"Muscle, Skeletal/drug effects"[MeSH] AND "Neoplasms/complications"[MeSH] AND ("Dietary Supplements/therapeutic use"[MeSH] OR "Nutrition Therapy"[MeSH])',

            # Q5: Sarcopenic obesity in cancer — diet therapy focus
            # Combines sarcopenia + obesity + cancer with nutrition qualifier
            '"Sarcopenia"[MeSH] AND "Obesity"[MeSH] AND "Neoplasms"[MeSH] AND ("Diet"[MeSH] OR "Nutritional Status"[MeSH])',

            # Q6: Weight loss prevention/control in cancer with nutritional support
            # /prevention & control qualifier targets prevention of wasting
            '"Weight Loss/prevention & control"[MeSH] AND "Neoplasms/complications"[MeSH] AND ("Nutrition Therapy"[MeSH] OR "Dietary Supplements/therapeutic use"[MeSH])',

            # Q7: Protein supplementation for cancer muscle preservation
            # /therapeutic use on protein targets papers about protein as treatment
            '"Dietary Proteins/therapeutic use"[MeSH] AND ("Cachexia"[MeSH] OR "Sarcopenia"[MeSH]) AND "Neoplasms"[MeSH]',

            # Q8: Malnutrition in cancer — therapy and diet therapy focus
            '"Malnutrition/diet therapy"[MeSH] AND "Neoplasms/complications"[MeSH]',
        ],
        "europe_pmc_queries": [
            '(TITLE_ABS:"cancer cachexia") AND (TITLE_ABS:"nutrition" OR TITLE_ABS:"dietary intervention") AND (OPEN_ACCESS:y)',
            '(TITLE_ABS:"sarcopenia") AND (TITLE_ABS:"cancer" OR TITLE_ABS:"oncology") AND (TITLE_ABS:"protein" OR TITLE_ABS:"nutrition") AND (OPEN_ACCESS:y)',
            '(TITLE_ABS:"muscle wasting" OR TITLE_ABS:"lean body mass") AND (TITLE_ABS:"cancer") AND (TITLE_ABS:"nutritional support") AND (OPEN_ACCESS:y)',
        ]
    },

    # ╔══════════════════════════════════════════════════════════════════╗
    # ║  TOPIC 3: Immunotherapy & Nutrition                            ║
    # ╚══════════════════════════════════════════════════════════════════╝
    "immunotherapy_nutrition": {
        "label": "Immunotherapy & Nutrition",
        "priority": 3,
        "queries": [
            # Q1: Immunotherapy + nutritional status in cancer
            # /adverse effects on immunotherapy captures papers about how nutrition affects tolerability
            '"Immunotherapy"[MeSH] AND "Nutritional Status"[MeSH] AND "Neoplasms"[MeSH]',

            # Q2: Immune checkpoint inhibitors + diet/nutrition therapy
            # This is the most specific MeSH heading for modern immunotherapy
            '"Immune Checkpoint Inhibitors"[MeSH] AND ("Nutrition Therapy"[MeSH] OR "Diet"[MeSH] OR "Nutritional Status"[MeSH])',

            # Q3: Gut microbiome + immunotherapy + diet (the microbiome-immune axis)
            # "Gastrointestinal Microbiome" is the current MeSH heading (replaced "Gut Microbiota")
            '"Gastrointestinal Microbiome"[MeSH] AND "Immunotherapy"[MeSH] AND ("Diet"[MeSH] OR "Dietary Fiber"[MeSH])',

            # Q4: Immunotherapy response/efficacy affected by body composition
            # /immunology qualifier on neoplasms + body composition
            '"Neoplasms/immunology"[MeSH] AND "Immunotherapy"[MeSH] AND ("Body Composition"[MeSH] OR "Body Mass Index"[MeSH] OR "Malnutrition"[MeSH])',

            # Q5: Microbiome modulation through diet affecting immune response in cancer
            # /diet therapy on the microbiome + cancer immunology
            '"Gastrointestinal Microbiome/drug effects"[MeSH] AND ("Diet"[MeSH] OR "Probiotics/therapeutic use"[MeSH]) AND "Neoplasms/immunology"[MeSH]',

            # Q6: Cachexia/sarcopenia impacting immunotherapy outcomes
            # Captures the body composition → immunotherapy response pathway
            '("Cachexia"[MeSH] OR "Sarcopenia"[MeSH]) AND "Immune Checkpoint Inhibitors"[MeSH] AND "Neoplasms"[MeSH]',

            # Q7: Dietary supplements/nutrition support during immunotherapy
            '"Dietary Supplements/therapeutic use"[MeSH] AND "Immunotherapy/adverse effects"[MeSH] AND "Neoplasms"[MeSH]',

            # Q8: Immunity modulated by nutrition in cancer context
            # /immunology qualifier on neoplasms + nutrition therapy
            '"Neoplasms/diet therapy"[MeSH] AND ("Immunity"[MeSH] OR "Immune System"[MeSH])',
        ],
        "europe_pmc_queries": [
            '(TITLE_ABS:"immunotherapy" OR TITLE_ABS:"checkpoint inhibitor") AND (TITLE_ABS:"nutrition" OR TITLE_ABS:"diet") AND (TITLE_ABS:"cancer") AND (OPEN_ACCESS:y)',
            '(TITLE_ABS:"gut microbiome" OR TITLE_ABS:"microbiota") AND (TITLE_ABS:"immunotherapy") AND (TITLE_ABS:"diet" OR TITLE_ABS:"fiber") AND (OPEN_ACCESS:y)',
            '(TITLE_ABS:"immune checkpoint") AND (TITLE_ABS:"nutritional status" OR TITLE_ABS:"body composition" OR TITLE_ABS:"sarcopenia") AND (OPEN_ACCESS:y)',
        ]
    },

    # ╔══════════════════════════════════════════════════════════════════╗
    # ║  TOPIC 4: Mediterranean Diet & Cancer Survival                 ║
    # ╚══════════════════════════════════════════════════════════════════╝
    "mediterranean_diet": {
        "label": "Mediterranean Diet & Cancer Survival",
        "priority": 4,
        "queries": [
            # Q1: Mediterranean diet + cancer — canonical query using official MeSH heading
            # "Diet, Mediterranean" is the exact MeSH heading (note comma syntax)
            '"Diet, Mediterranean"[Majr] AND "Neoplasms"[MeSH]',

            # Q2: Mediterranean diet as cancer prevention
            # /prevention & control qualifier targets prevention studies
            '"Diet, Mediterranean"[MeSH] AND "Neoplasms/prevention & control"[MeSH]',

            # Q3: Mediterranean diet during cancer therapy (tolerability, outcomes)
            # /diet therapy on neoplasms + Mediterranean pattern
            '"Diet, Mediterranean"[MeSH] AND "Neoplasms/diet therapy"[MeSH]',

            # Q4: Mediterranean diet + cancer survival/mortality
            # /mortality qualifier on neoplasms narrows to survival studies
            '"Diet, Mediterranean"[MeSH] AND "Neoplasms/mortality"[MeSH]',

            # Q5: Anti-inflammatory dietary pattern + cancer outcomes
            # Captures papers about dietary inflammation index in cancer
            '"Inflammation"[MeSH] AND ("Diet"[MeSH] OR "Dietary Pattern"[All Fields]) AND "Neoplasms/diet therapy"[MeSH]',

            # Q6: Olive oil therapeutic use in cancer context
            # Olive oil is a key Mediterranean component with its own MeSH heading
            '"Olive Oil/therapeutic use"[MeSH] AND "Neoplasms"[MeSH]',

            # Q7: Mediterranean diet + specific high-prevalence cancers
            # /prevention & control for breast + colorectal — highest evidence base
            '"Diet, Mediterranean"[MeSH] AND ("Breast Neoplasms/prevention & control"[MeSH] OR "Colorectal Neoplasms/prevention & control"[MeSH])',

            # Q8: Fatty acids + dietary pattern + cancer outcomes
            # Captures omega-3/MUFA Mediterranean components
            '"Fatty Acids, Unsaturated/therapeutic use"[MeSH] AND "Diet"[MeSH] AND "Neoplasms/diet therapy"[MeSH]',
        ],
        "europe_pmc_queries": [
            '(TITLE_ABS:"Mediterranean diet") AND (TITLE_ABS:"cancer survival" OR TITLE_ABS:"cancer outcome" OR TITLE_ABS:"cancer mortality") AND (OPEN_ACCESS:y)',
            '(TITLE_ABS:"Mediterranean diet") AND (TITLE_ABS:"chemotherapy" OR TITLE_ABS:"cancer treatment") AND (OPEN_ACCESS:y)',
            '(TITLE_ABS:"anti-inflammatory diet" OR TITLE_ABS:"dietary inflammatory index") AND (TITLE_ABS:"cancer") AND (OPEN_ACCESS:y)',
        ]
    },
}


# ──────────────────────────────────────────
# Quick reference: What each qualifier does
# ──────────────────────────────────────────
QUALIFIER_GUIDE = """
MeSH Qualifiers Used in NORE Harvester Queries
═══════════════════════════════════════════════

QUALIFIER              WHAT IT CAPTURES                              EXAMPLE
──────────────────────────────────────────────────────────────────────────────
/diet therapy (DH)     Nutritional treatment of a condition           "Cachexia/diet therapy"[MeSH]
                       → papers where nutrition IS the intervention

/drug therapy (DT)     Pharmacological treatment                      "Neoplasms/drug therapy"[MeSH]
                       → papers about drug treatment of cancer

/adverse effects (AE)  Unwanted effects of substances/treatments      "Immunotherapy/adverse effects"[MeSH]
                       → papers about side effects

/therapeutic use (TU)  Substance used as treatment                    "Dietary Supplements/therapeutic use"[MeSH]
                       → papers about supplements AS treatment

/complications (CO)    Co-occurring conditions or sequelae            "Neoplasms/complications"[MeSH]
                       → papers about conditions caused by cancer

/prevention & control  Preventive measures                            "Neoplasms/prevention & control"[MeSH]
                       → papers about preventing cancer

/pharmacokinetics (PK) Absorption, distribution, metabolism, excretion "Antineoplastic Agents/pharmacokinetics"[MeSH]
                       → papers about how drugs move through body

/drug effects (DE)     Effects of drugs/substances on processes        "Muscle, Skeletal/drug effects"[MeSH]
                       → papers about how substances affect muscle

/metabolism (ME)       Metabolic processes                             "Cytochrome P-450 Enzyme System/metabolism"[MeSH]
                       → papers about CYP enzyme activity

/immunology (IM)       Immune aspects                                  "Neoplasms/immunology"[MeSH]
                       → papers about immune response to cancer

/mortality (MO)        Death/survival outcomes                         "Neoplasms/mortality"[MeSH]
                       → papers about cancer survival

/physiopathology (PP)  Pathological physiology                         "Cachexia/physiopathology"[MeSH]
                       → papers about mechanisms of wasting

SPECIAL TAGS:
[Majr]    = Major topic (indexer starred it as primary focus of the paper)
[MeSH]    = MeSH heading with automatic tree explosion (includes narrower terms)
[MeSH:NoExp] = Exact heading only (no tree explosion)
"""

if __name__ == "__main__":
    print(QUALIFIER_GUIDE)
    print("\n\nQuery Summary:")
    print("=" * 60)
    for topic_key, topic in TOPIC_QUERIES.items():
        print(f"\n{topic['label']} (Priority {topic['priority']})")
        print(f"  PubMed queries:    {len(topic['queries'])}")
        print(f"  Europe PMC queries: {len(topic['europe_pmc_queries'])}")
        for i, q in enumerate(topic['queries'], 1):
            print(f"  Q{i}: {q[:90]}...")
