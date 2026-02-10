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
p5 |≁ p7
```
*Generation-use chains do NOT entail wasDerivedFrom. (Commitment #24)*

```
p6 |≁ ∃e
```
*wasInformedBy does NOT entail intermediate Entity existence. (Commitment #30)*

```
p7, p7 |≁ p7
```
*wasDerivedFrom is NOT transitive. (Commitment #23, from PROV-CONSTRAINTS)*

---

## Two Reasoning Modes

The material base can be reasoned over in two ways, with different properties:

| Property | Classical Export | NMMS Reasoner |
|----------|------------------|---------------|
| Weakening | ✓ Holds | ✗ Fails |
| Base Transitivity | ✓ Holds | ✗ Fails |
| Logical Transitivity | ✓ Holds | ✓ Holds |
| Consistency Check | SAT/UNSAT | Derivability |
| Substructurality | Lost | Preserved |

---

## Classical Export

For integration with standard KR tools, the material base can be exported to classical propositional logic. See [`prov_o_classical_export.py`](prov_o_classical_export.py).

**Important:** The classical export is *lossy*. It flattens material implications into classical conditionals, which validates Weakening and Transitivity. This loses the substructural character of the material base.

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

## NMMS Reasoner

The NMMS (Non-Monotonic Multi-Succedent) sequent calculus from Hlobil & Brandom (2025) provides the *proper* logical extension of the material base that preserves its substructural character. See [`prov_o_nmms_reasoner.py`](prov_o_nmms_reasoner.py).

### Key Properties

1. **No Weakening (Nonmonotonicity)**: Adding premises can defeat inferences.
   ```
   p2 => p18: True
   p2, p5 => p18: False
   ```

2. **No Base Transitivity (Nontransitivity)**: Chains of base inferences don't compose.
   ```
   p2 => p18: True
   p18 => p23: True
   p2 => p23: False
   ```

3. **Logical Transitivity Holds**: Once explicitated as conditionals, transitivity is recovered.
   ```
   p2->p18, p18->p23 => p2->p23: True
   ```

4. **Supraclassicality**: All classical tautologies remain derivable.
   ```
   => p2 | ~p2: True
   ```

### Explicitation

Material implications can be made explicit using logical vocabulary:

| Material Implication | Explicit Conditional |
|---------------------|---------------------|
| p2 \|∼ p18 | p2 → p18 |
| p3 \|∼ p27 | p3 → p27 |
| p4 \|∼ p29 | p4 → p29 |
| p6 \|∼ p30 | p6 → p30 |
| p7 \|∼ p28 | p7 → p28 |
| p9 \|∼ p25 | p9 → p25 |
| p9 \|∼ p26 | p9 → p26 |
| p10 \|∼ p24 | p10 → p24 |
| p18 \|∼ p23 | p18 → p23 |

Each conditional is derivable: `=> p2 -> p18` holds in NMMS.

### The Key Insight

NMMS separates **defeasible base-level reasoning** from **indefeasible logical-level reasoning**:

- At the base level, `p2 |∼ p18` does NOT imply `p2, p5 |∼ p18` (no Weakening)
- At the logical level, `p2->p18, p18->p23` DOES imply `p2->p23` (transitivity via Cut)

The logical vocabulary (conditionals) makes material inferences *sayable* and recovers classical properties at that level, while preserving the substructural character of the base.

---

## Analysis: Logical Status of Commitments

Both reasoning modes can distinguish two kinds of dialectical content:

### 1. Logically Forced Commitments

These cannot be denied without creating inconsistency with other commitments.

**Example: ¬p20 (wasDerivedFrom does NOT suffice for cross-context identity)**

The material constraint `p7, p23 |∼ ~p20` encodes the tension that forced retraction.

| Mode | Test | Result |
|------|------|--------|
| Classical Export | Assert p7 ∧ p23 ∧ p20 with (p7 ∧ p23) → ¬p20 | UNSAT |
| NMMS | p7, p23 => ~p20 | True |

In NMMS, note the subtlety:
- `p7, p23 => ~p20`: **True** (from base axiom)
- `p7, p23, p20 => ~p20`: **False** (no Weakening!)

The constraint is *exact*: the sequent `p7, p23 ⊢ ~p20` rules out asserting p7 and p23 while denying ~p20. NMMS preserves this precision.

### 2. Substantive Expert Judgments

These could consistently be denied; they reflect domain expertise rather than logical necessity.

**Example: p24 (wasDerivedFrom requires explicit assertion)**

| Mode | Test | Result |
|------|------|--------|
| Classical Export | Assert all commitments with ¬p24 instead of p24 | SAT |
| NMMS | => p24 | False |
| NMMS | => ~p24 | False |
| NMMS | ~p24, p30 => contradiction | False |

Neither p24 nor ~p24 is derivable from the base. The asymmetric treatment of shortcut relations is a *design decision*, not logically forced.

### Summary Table

| Commitment | Description | Logical Status |
|------------|-------------|----------------|
| ¬p20 | wasDerivedFrom doesn't suffice | **Logically forced** |
| p23 | Expanded Terms add expressiveness | **Logically forced** (via p2→p18→p23) |
| p24 | wasDerivedFrom requires explicit assertion | Design decision |
| p30 | wasInformedBy inferred, not reducible | Design decision |

### Implications for Knowledge Engineering

- **Logically forced content** is robust to re-examination. Any revision would require retracting one of the forcing commitments or contesting the material implication.

- **Design decisions** may be revisited if domain understanding changes. They represent the respondent's expert judgment at a point in time, not immutable logical constraints.

The Elenchus protocol surfaces **both** kinds of content through the same dialectical process. The reasoners enable post-hoc analysis to classify them.

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
