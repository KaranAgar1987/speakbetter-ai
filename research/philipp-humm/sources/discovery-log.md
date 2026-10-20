# Discovery log — Philipp Humm (review-ready)

**Last updated:** 2026-10-20 (catalog ↔ log alignment pass)  
**Status:** Paused for your review. No `concepts/` directory.

Canonical index: **`source-catalog.yaml`** (25 records). This log summarizes evidence judgments and mirrors catalog fields.

---

## Record counts (must match catalog header)

| Bucket | ID range | Count | `access` |
|--------|----------|------:|----------|
| Story Lab | SRC-001 … SRC-014 | 14 | public |
| YouTube | SRC-V01 … SRC-V10 | 10 | public |
| Discovery metadata | SRC-X01 | 1 | inaccessible |
| **Total** | | **25** | **24 accessible** |

---

## Catalog mirror — all sources

| ID | `evidence_status` | `verified_frameworks` | `research_status` | `review_level` |
|----|-------------------|----------------------|-------------------|----------------|
| SRC-001 | verified-framework | CART | extracted | — |
| SRC-002 | verified-framework | CART | extracted | — |
| SRC-003 | single-source | — | extracted | — |
| SRC-004 | lead-unverified | — | inventoried | — |
| SRC-005 | not-applicable | — | inventoried | — |
| SRC-006 | not-applicable | — | inventoried | — |
| SRC-007 | unresolved-relationship | — | extracted | — |
| SRC-008 | single-source | — | extracted | — |
| SRC-009 | not-applicable | — | inventoried | — |
| SRC-010 | verified-teaching-point | — | extracted | — |
| SRC-011 | single-source | — | extracted | — |
| SRC-012 | single-source | — | extracted | — |
| SRC-013 | single-source | — | extracted | — |
| SRC-014 | verified-framework | 5-P-confidence-loop | extracted | — |
| SRC-V01 | verified-framework | 5-P-confidence-loop | extracted | selective |
| SRC-V02 | unresolved-relationship | — | extracted | selective |
| SRC-V03 | single-source | — | extracted | selective |
| SRC-V04 | single-source | — | extracted | partial |
| SRC-V05 | lead-unverified | — | extracted | partial |
| SRC-V06 | lead-unverified | — | extracted | selective |
| SRC-V07 | lead-unverified | — | extracted | partial |
| SRC-V08 | lead-unverified | — | extracted | partial |
| SRC-V09 | lead-unverified | — | extracted | partial |
| SRC-V10 | lead-unverified | — | extracted | selective |
| SRC-X01 | inaccessible | — | inaccessible | — |

`evidence_status` values are defined in the **`source-catalog.yaml` header** (same list as `methodology/evidence-standards.md`, plus `verified-framework`, `unresolved-relationship`, `not-applicable`).

---

## Verified frameworks

### CART — Context, Adversity, Resolution, Takeaway

| Source | URL | Date on page |
|--------|-----|--------------|
| SRC-001 | https://storylab.co/structure/ | 2024-04-22 |
| SRC-002 | https://storylab.co/7-years-of-storytelling-advice-in-54-mins/ | 2024-10-30 |

**Criterion met:** Explicit four-step definition with aligned labels in ≥2 Tier-1 articles.  
**Extracts:** `extracts/articles/SRC-001-structure.md`, `SRC-002-seven-years-storytelling.md`

### 5-P confidence loop — Proof, Practice, Prime, Purpose, Praise

| Source | URL | Date |
|--------|-----|------|
| SRC-014 | https://storylab.co/5-p-confidence-loop-framework-public-speaking-confidence/ | 2026-04-13 |
| SRC-V01 | https://www.youtube.com/watch?v=OahwQSlPG0I | 2026-04-11 (upload) |

**Criterion met:** Same five component names and praise→proof cycle in article and video captions.  
**Extracts:** `extracts/articles/SRC-014-5-p-confidence-loop.md`, `extracts/videos/SRC-V01-speak-with-confidence.md`  
**Limitation:** Sub-exercises (e.g. full priming routine) not line-compared across article vs video.

---

## Verified teaching points (≥2 Tier-1 articles; not promoted to `concepts/`)

| Teaching point | Sources | Catalog rows |
|----------------|---------|--------------|
| **Constructive embarrassment** (voluntary awkward situations before speaking) | SRC-007, SRC-008, SRC-010 | SRC-010 `verified-teaching-point`; also SRC-007, SRC-008 |
| Beginners: **feel good on stage** before micro-delivery tactics | SRC-007, SRC-010 | SRC-010 |
| **Improv theatre** for speaking | SRC-007, SRC-010 | SRC-010 |

---

## Single-source (one Tier-1 source with explicit content)

| Item | Source |
|------|--------|
| Zoom-in five techniques (location, action, thoughts, feelings, dialogue) | SRC-003 |
| Five storytelling techniques article list | SRC-011 |
| SCR (Situation-Complication-Resolution) for interviews | SRC-012 |
| Five presentation openers | SRC-013 |
| Four TED prep strategies | SRC-008 |
| SME, S-Word, SSS labels | SRC-002 (other topics on same page) |
| Story bank field list | SRC-002 |
| Five **article** steps (“better than 99%”) | SRC-007 |
| Five **video** habits (“better than 99%”) | SRC-V02 |
| Presentation-opening video (selective excerpts) | SRC-V03 |

---

## Lead-unverified (`framework_leads` or partial video)

| Lead | Catalog |
|------|---------|
| StorySelling Method (multi-step system) | SRC-004; name also in SRC-002 |
| Anticipation Hook / 20 spices | SRC-007 `framework_leads` |
| Homework for Life (Matthew Dicks) | SRC-002 text |
| Videos not fully reviewed | SRC-V05, V06, V07, V08, V09, V10 |

---

## Unresolved relationships

| Pair | Catalog | Finding |
|------|---------|---------|
| SRC-007 **five steps** vs SRC-V02 **five habits** | Both `unresolved-relationship`, `paired_sources` | Different enumerations and content; same marketing theme only. **Not one method.** |

---

## Interpretations (not attributed to Humm)

- SRC-003 “zoom in” ↔ SRC-V04 / SRC-V07 “zoom” language — thematic only (`paired_sources` noted; not verified).
- SRC-013 ↔ SRC-V03 / V08 / V09 — all concern openings; **not** mapped to one framework.

---

## Inaccessible

| ID | URL | Reason |
|----|-----|--------|
| SRC-X01 | https://storylab.co/wp-sitemap-posts-post-1.xml | Cloudflare challenge |

---

## Video review levels (matches catalog `review_level`)

| Level | Meaning | IDs |
|-------|---------|-----|
| **selective** | Targeted timestamps/themes only; not full video | V01, V02, V03, V06, V10 |
| **partial** | Some excerpts; majority not reviewed | V04, V05, V07, V08, V09 |

---

## Your review checklist

1. Confirm **verified-framework** for CART and 5-P confidence loop.  
2. Confirm **unresolved-relationship** for SRC-007 vs SRC-V02.  
3. Confirm **verified-teaching-point** grouping for constructive embarrassment / improv / feel-good-on-stage.  
4. Approve next wave: book ingest, opening crosswalk (SRC-013 vs videos), or deeper partial-video passes.
