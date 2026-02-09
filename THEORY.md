# Propositional Theory: PROV-O Section 3.1

A material base extracted from the Elenchus dialectical state, following Hlobil and Brandom (2025).

## Material Base 𝔅 = ⟨L_𝔅, |∼_𝔅⟩

### Base Language L_𝔅

Atomic propositions representing commitments from the dialectic:

```
p1   Three core classes form the basis of PROV-O: Entity, Activity, Agent
p2   Entity is a thing with fixed aspects
p3   Activity is something that occurs over time and acts upon or with entities
p4   Agent bears responsibility for activities, entities, or other agents' activities
p5   used and wasGeneratedBy relate Activities to Entities
p6   wasInformedBy provides Activity-to-Activity dependency
p7   wasDerivedFrom expresses Entity-to-Entity transformation
p8   wasAssociatedWith and wasAttributedTo ascribe Agent responsibility
p9   actedOnBehalfOf expresses delegation with shared responsibility
p10  Three types of provenance chains exist: Activity-Entity, Activity-only, Entity-only
p18  'Fixed aspects' is pragmatic (context-relative); change modeled via derivation
p23  Expanded Terms add expressiveness, not just convenience
p24  wasDerivedFrom requires explicit assertion, not entailed by chains
p25  Delegation responsibility is hierarchical
p26  Delegation responsibility is transitive
p27  Activities are durational; InstantaneousEvents for instants
p28  wasDerivedFrom is broad; subtypes provide specificity
p29  Agency is pragmatic and context-dependent
p30  wasInformedBy inferred from generation-use, but doesn't entail Entity exists
```

**Denials:** D = ∅ (no explicit denials in this dialectic)

**Retracted:** p20 (wasDerivedFrom suffices for cross-context identity) — superseded by p23

---

### Base Consequence Relation |∼_𝔅

The relation |∼_𝔅 = I ∪ Cont, where I contains accepted material implications from resolved tensions.

#### Structural (Containment)

For any p ∈ L_𝔅:
```
p |∼ p
```

#### Material Implications I (from accepted tensions)

**From Challenge #11 (Entity change):**
```
p2 |∼ p18
```
*Commitment to "fixed aspects" is incoherent with denying pragmatist individuation.*

**From Challenge #12 (Activity duration):**
```
p3 |∼ p27
```
*Commitment to Activities occurring over time is incoherent with denying the durational/instantaneous distinction.*

**From Challenge #13 (Agent responsibility):**
```
p4 |∼ p29
```
*Commitment to Agents bearing responsibility is incoherent with denying pragmatic agency.*

**From Challenge #14 (wasInformedBy semantics):**
```
p6 |∼ p30
```
*Commitment to wasInformedBy providing Activity-to-Activity dependency is incoherent with denying the asymmetric inference pattern.*

**From Challenge #15 (Derivation scope):**
```
p7 |∼ p28
```
*Commitment to wasDerivedFrom as transformation is incoherent with denying its broad scope with subtypes.*

**From Challenge #16 (Delegation distribution):**
```
p9 |∼ p25
p9 |∼ p26
```
*Commitment to shared responsibility in delegation is incoherent with denying hierarchy or transitivity.*

**From Challenge #17 (Chain equivalence):**
```
p10 |∼ p24
```
*Commitment to three chain types is incoherent with denying that wasDerivedFrom requires explicit assertion.*

**From Challenges #19, #21 (Cross-context identity):**
```
p18 |∼ p23
```
*Commitment to pragmatic individuation is incoherent with denying that Expanded Terms add expressiveness.*

**Cross-commitment coherence (implicit in respondent's position):**
```
p18, p29 |∼
```
*p18 and p29 are co-tenable (no incoherence). Pragmatist Entity individuation coheres with pragmatist Agency.*

```
p24, p30 |∼
```
*p24 and p30 are co-tenable. Both shortcut relations (wasDerivedFrom, wasInformedBy) have the same logical status: inferable from but not reducible to chains.*

---

### Non-Implications (Explicit)

The following were explicitly established as **not holding**:

```
p5 |≁ p7
```
*Generation-use chains do NOT entail wasDerivedFrom. (Commitment #24)*

```
p6 |≁ ∃e
```
*wasInformedBy does NOT entail intermediate Entity existence. (Commitment #30)*

```
p7, p7 |≁ p7
```
*wasDerivedFrom is NOT transitive. (Commitment #23, from PROV-CONSTRAINTS)*

---

## Classical Export

For integration with standard KR tools, the material base can be exported to classical propositional logic:

### Assertions (from C)
```
p1 ∧ p2 ∧ p3 ∧ p4 ∧ p5 ∧ p6 ∧ p7 ∧ p8 ∧ p9 ∧ p10 ∧
p18 ∧ p23 ∧ p24 ∧ p25 ∧ p26 ∧ p27 ∧ p28 ∧ p29 ∧ p30
```

### Material Conditionals (from I)
```
p2 → p18
p3 → p27
p4 → p29
p6 → p30
p7 → p28
p9 → p25
p9 → p26
p10 → p24
p18 → p23
```

### Negations (from non-implications, expressed as blocked inferences)
```
¬(p5 → p7)           -- generation-use does not entail derivation
¬(p6 → ∃e)           -- wasInformedBy does not entail Entity
¬((p7 ∧ p7) → p7)    -- wasDerivedFrom not transitive
```

---

## Z3 Analysis: Logical Status of Commitments

The material base is encoded in Z3 (see [`prov_o_classical_export.py`](prov_o_classical_export.py)) to computationally distinguish two kinds of content:

### 1. Logically Forced Commitments

These cannot be denied without creating inconsistency with other commitments and accepted material implications.

**Example: ¬p20 (wasDerivedFrom does NOT suffice for cross-context identity)**

```
Setup:
  - All current commitments (p1-p10, p18, p23-p30)
  - Retracted commitment p20
  - Material implication: p7 ∧ p23 → ¬p20

Result: UNSAT
```

The retraction of p20 was **logically forced**, not a preference change. Given:
- p7: wasDerivedFrom expresses Entity-to-Entity transformation
- p23: Expanded Terms add genuine expressiveness
- The material implication p7 ∧ p23 → ¬p20

...asserting p20 creates inconsistency. The respondent could have contested the material implication, but PROV-CONSTRAINTS establishes that alternateOf and specializationOf have formal properties (transitivity, symmetry, attribute inheritance) that wasDerivedFrom cannot express.

### 2. Substantive Expert Judgments

These could consistently be denied; they reflect domain expertise rather than logical necessity.

**Example: p24 (wasDerivedFrom requires explicit assertion)**

```
Setup:
  - All commitments except p24
  - ¬p24 (assume wasDerivedFrom IS entailed by chains)
  - p30 still asserted (wasInformedBy inferred but not reducible)

Result: SAT
```

The asymmetric treatment of shortcut relations is a **design decision**. The two relations could have been treated symmetrically:
- Both inferred from chains, or
- Both requiring explicit assertion

The respondent chose asymmetric treatment based on domain judgment about PROV-O semantics, not because logic forced it.

### Summary Table

| Commitment | Description | Logical Status |
|------------|-------------|----------------|
| ¬p20 | wasDerivedFrom doesn't suffice | **Logically forced** |
| p23 | Expanded Terms add expressiveness | **Logically forced** (via p2→p18→p23) |
| p24 | wasDerivedFrom requires explicit assertion | Design decision |
| p30 | wasInformedBy inferred, not reducible | Design decision |

### Implications for Knowledge Engineering

This distinction matters:

- **Logically forced content** is robust to re-examination. Any revision would require retracting one of the forcing commitments or contesting the material implication.

- **Design decisions** may be revisited if domain understanding changes. They represent the respondent's expert judgment at a point in time, not immutable logical constraints.

The Elenchus protocol surfaces **both** kinds of content through the same dialectical process. The Z3 encoding enables post-hoc analysis to classify them.

---

## Summary Statistics

| Component | Count |
|-----------|-------|
| Atomic propositions (L_𝔅) | 19 |
| Denials (D) | 0 |
| Material implications (I) | 9 |
| Explicit non-implications | 3 |
| Retracted propositions | 1 |
| Logically forced commitments | 2+ |
| Design decisions | 2+ |

---

## Respondent

**Paul Groth** — W3C Provenance Incubator Group, co-editor of PROV specifications.

---

## References

- Hlobil, U. & Brandom, R. (2025). *Reasons for Logic, Logic for Reasons*. Routledge.
- Lebo, T., Sahoo, S., & McGuinness, D. (2013). PROV-O: The PROV Ontology. W3C Recommendation.
- Cheney, J., Missier, P., & Moreau, L. (2013). Constraints of the PROV Data Model. W3C Recommendation.

---

*Extracted from dialectical state at [bradleypallen/prov-o-section-3.1](https://github.com/bradleypallen/prov-o-section-3.1), 2026-02-09*
