---
name: lit-review
description: Literature review for a research project in the user's house format. Two modes. (1) Protocol - a systematic search plan with research questions, concept blocks A-F, Web of Science/Scopus queries, filters, export, dedup, screening and PRISMA counts. (2) Analysis - the literature organized by research direction, one table per direction (Lucrare / Ce face / De ce contează aici) plus "Ce preluăm", then gaps, novelty table, risks and sources. Use when the user asks for a literature review, state of the art, "analiza literaturii", "studiul literaturii", a search protocol, related work positioning, or a novelty/gap check for a project (e.g. Tessera, Geometric Models and Circuits, VLDB, federated learning, edge/fog). Not for summarizing a single paper (research-litnote) or drafting the final Related Work prose (related-work).
---

# Literature review (house format)

Output language: **Romanian**, technical terms kept in English (federated learning, non-IID, mesh, operator learning). Plain, direct sentences; no hype.

## 0. Before writing

1. Pin down the project in 3-5 sentences: the core idea, what is claimed new, the target venue if known. Ask if unclear; never guess the contribution.
2. Ask which mode is needed if the request does not say:
   - **Protocol**: the review hasn't been run yet, or must be reproducible (thesis, grant report, systematic review).
   - **Analysis**: the user wants the map of the field and the positioning now.
3. Decide where it goes: a Claude Doc by default (that is where the user keeps these), a Markdown file if they are working in a repo.

## Hard rules on sources

- **Never invent a paper, author, year, venue, number or quote.** Every work listed must have been found in this session (search, a PDF the user gave, a lookup tool) or supplied by the user.
- Each paper gets a **working link** (DOI, publisher, arXiv, proceedings) and the venue in parentheses: `[Autor et al. AAAA, Titlu scurt](url) (Venue)`.
- If a claim could not be verified, mark it `[neverificat]` instead of dropping or stating it as fact.
- State the coverage honestly at the end: how many works were read, from where, and what a broader search could still change. A gap claim from <20 papers is a hypothesis, not a finding.
- Run `/citation-check` on the final list when the user is preparing a submission.

## Mode 1: Protocol

Sections, in order:

1. **Scop și întrebări de cercetare** - one paragraph on what the stage produces, then RQ1..RQn. Typical set: context, open problems, the project's specific mechanism, adjacent techniques, evaluation (datasets, benchmarks, metrics), and the **gap RQ** ("ce lipsește exact la intersecția X × Y × Z").
2. **Vocabular de căutare** - table `Bloc | Concept | Termeni (OR în interiorul blocului)`, blocks A, B, C... Use quotes for phrases and `*` for truncation. Note which blocks are rare and must be combined more loosely.
3. **Interogări** - Step 1: base blocks #1..#n. Step 2: table `Cod | Combinație | Ce răspunde | Rol în studiu` for Q1..Qn (include a reviews-only query `DT=(Review)` and a precise title-only `TI=` variant).
4. **Cum ajustezi** - >~2000 results: narrow (TI= instead of TS=, filters); <~20: it is likely the gap, so extend with snowballing and other databases; known noise terms with `NOT`; keep a search log (date, exact query, count).
5. **Filtre** - years, document types, editions (include CPCI-S for IEEE/ACM conferences), WoS categories; a looser variant for the rarer queries.
6. **Colectare și export** - plain text full record + cited references for the bibliometric map; RIS/BibTeX into Zotero (Better BibTeX); Excel for screening. File naming `wos_Q4_AAAA-LL-ZZ.ris` in `01-raw/`, raw files never edited. Complementary sources (Scopus, arXiv, IEEE Xplore) and snowballing.
7. **Deduplicare, screening și PRISMA** - dedup (DOI, then normalized title + year; preprint = published version), inclusion criteria I1..In and exclusion E1..En with codes, title/abstract screening with calibration, full-text eligibility, reading priority, and a PRISMA 2020 counts table to fill in.
8. **Maparea literaturii** - bibliometric layer (VOSviewer / bibliometrix: co-occurrence, co-citation, thematic map) and conceptual layer: an extraction table with the same fields for every included paper (problem, mechanism, setting, datasets, metrics, limits).
9. **Organizare și livrabile** - Zotero + versioned Markdown notes; deliverables list ending with the state-of-the-art report that becomes the paper's Related Work.
10. **Pașii următori** - the first concrete step is a dry run that only counts results; the user reports the counts back and the queries are tuned before any export.

When the user returns with counts, add a **Rezultatele rulării (data)** table `Interogare | Set WoS | Rezultate | Decizie` and the narrowed queries (Q3b, Q4b...).

## Mode 2: Analysis

Sections, in order:

1. **Rezumat** - the proposal in one paragraph, then the 2-4 ideas that support it, each with its precedent in the literature (bold lead sentence + explanation). Then **Ce trebuie să decizi** (open choices that change the plan) and, once answered, **Decizii luate (data)**.
2. **Analiza literaturii** - one short intro, then one subsection per research direction, numbered `### 1. Direcția ...`:
   - one paragraph framing the direction;
   - table **`Lucrare | Ce face | De ce contează aici`** (5-10 rows; the last column says what it means *for this project*, not a generic summary);
   - a closing line **`Ce preluăm:`** - the concrete idea, mechanism or baseline the project takes from this direction.
3. **Goluri în literatură** - **Goluri identificate** (bullets: what no work combines) and **Riscuri și mitigări** (table `Risc | De ce | Mitigare`).
4. **Ce aducem nou** - table `Contribuție | De ce e nouă (față de ce am citit) | Ce trebuie demonstrat`. Each row must point at specific papers from the tables above. This table is the basis for the paper's contribution list and its experiments.
5. **Surse și verificare** - how many works, from where, what remains unverified, and what a broader search should check before publishing.

If an analysis document already exists and has grown by additions, start with **Sinteză critică (data)**: what is new, internal contradictions, duplicated sections, missing scenarios, and a proposed restructuring. Propose changes as suggestions in the doc rather than rewriting it.

## Style

- Tables over long prose for comparisons; prose for reasoning.
- One idea per paragraph; lead with the claim, then the evidence.
- Dates as absolute dates (21 noiembrie 2026), never "ieri" or "săptămâna trecută".
- Keep it as long as the material needs; do not pad directions with weak papers to reach a count.
