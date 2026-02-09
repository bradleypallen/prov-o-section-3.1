"""
Propositional Material Base: PROV-O Section 3.1

A Z3 encoding of the material base extracted from the Elenchus dialectical state
with Paul Groth (W3C Provenance Incubator Group).

Following Hlobil & Brandom (2025), a material base 𝔅 = ⟨L_𝔅, |∼_𝔅⟩ consists of:
- L_𝔅: an atomic language (propositional variables)
- |∼_𝔅: a base consequence relation (material implications)

The classical export represents commitments as assertions, material implications
as conditionals, and enables consistency checking and consequence queries.
"""

from z3 import Bool, Solver, Implies, And, Or, Not, sat, unsat, unknown
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


# =============================================================================
# BASE LANGUAGE L_𝔅
# =============================================================================

# Atomic propositions from the dialectic
# Each represents a commitment made by the respondent

PROPOSITIONS = {
    # Core PROV-O Section 3.1 commitments
    'p1':  "Three core classes form the basis of PROV-O: Entity, Activity, Agent",
    'p2':  "Entity is a thing with fixed aspects",
    'p3':  "Activity is something that occurs over time and acts upon or with entities",
    'p4':  "Agent bears responsibility for activities, entities, or other agents' activities",
    'p5':  "used and wasGeneratedBy relate Activities to Entities",
    'p6':  "wasInformedBy provides Activity-to-Activity dependency",
    'p7':  "wasDerivedFrom expresses Entity-to-Entity transformation",
    'p8':  "wasAssociatedWith and wasAttributedTo ascribe Agent responsibility",
    'p9':  "actedOnBehalfOf expresses delegation with shared responsibility",
    'p10': "Three types of provenance chains exist: Activity-Entity, Activity-only, Entity-only",

    # Interpretive commitments from dialectical examination
    'p18': "'Fixed aspects' is pragmatic (context-relative); change modeled via derivation",
    'p23': "Expanded Terms add expressiveness, not just convenience",
    'p24': "wasDerivedFrom requires explicit assertion, not entailed by chains",
    'p25': "Delegation responsibility is hierarchical",
    'p26': "Delegation responsibility is transitive",
    'p27': "Activities are durational; InstantaneousEvents for instants",
    'p28': "wasDerivedFrom is broad; subtypes provide specificity",
    'p29': "Agency is pragmatic and context-dependent",
    'p30': "wasInformedBy inferred from generation-use, but doesn't entail Entity exists",
}

# Retracted proposition (not in the current base)
RETRACTED = {
    'p20': "wasDerivedFrom suffices for cross-context Entity identity (RETRACTED)"
}


# =============================================================================
# MATERIAL IMPLICATIONS I (from accepted tensions)
# =============================================================================

# Each tuple (antecedent, consequent) represents a material implication
# derived from an accepted tension in the dialectic.
#
# Γ |∼ Δ means: asserting Γ while denying Δ is incoherent
# In classical export: Γ → Δ

MATERIAL_IMPLICATIONS = [
    # Challenge #11: "fixed aspects" implies pragmatist individuation
    (['p2'], 'p18'),

    # Challenge #12: "over time" implies durational/instantaneous distinction
    (['p3'], 'p27'),

    # Challenge #13: "responsibility" implies pragmatic agency
    (['p4'], 'p29'),

    # Challenge #14: wasInformedBy semantics
    (['p6'], 'p30'),

    # Challenge #15: wasDerivedFrom scope
    (['p7'], 'p28'),

    # Challenge #16: Delegation distribution (two implications)
    (['p9'], 'p25'),
    (['p9'], 'p26'),

    # Challenge #17: Chain types imply explicit assertion required
    (['p10'], 'p24'),

    # Challenges #19, #21: Pragmatic individuation implies Expanded Terms needed
    (['p18'], 'p23'),
]


# =============================================================================
# NON-IMPLICATIONS (explicit failures of entailment)
# =============================================================================

# These record inferences that were explicitly rejected in the dialectic.
# They cannot be directly expressed as Z3 constraints on the base,
# but they constrain what additional implications could be added.

NON_IMPLICATIONS = [
    # generation-use does NOT entail wasDerivedFrom
    {
        'antecedent': ['p5'],
        'consequent': 'p7',
        'note': "Existence of used(a,e) and wasGeneratedBy(e',a) does not entail wasDerivedFrom(e',e)"
    },
    # wasInformedBy does NOT entail intermediate Entity exists
    {
        'antecedent': ['p6'],
        'consequent': 'entity_exists',  # Not in base language
        'note': "wasInformedBy(a1,a2) does not entail ∃e. wasGeneratedBy(e,a2) ∧ used(a1,e)"
    },
    # wasDerivedFrom is NOT transitive
    {
        'antecedent': ['p7', 'p7'],  # Symbolic: wasDerivedFrom(a,b) ∧ wasDerivedFrom(b,c)
        'consequent': 'p7',          # does not entail wasDerivedFrom(a,c)
        'note': "wasDerivedFrom is not transitive (per PROV-CONSTRAINTS)"
    },
]


# =============================================================================
# Z3 ENCODING
# =============================================================================

class MaterialBase:
    """
    Z3 encoding of a propositional material base.

    Supports:
    - Consistency checking
    - Consequence queries (does X follow from the base?)
    - Countermodel generation
    - Adding/retracting commitments
    """

    def __init__(self):
        # Create Z3 Boolean variables for each proposition
        self.props = {name: Bool(name) for name in PROPOSITIONS}
        self.descriptions = PROPOSITIONS.copy()

        # Track which propositions are currently committed
        self.commitments = set(PROPOSITIONS.keys())

        # Store material implications
        self.implications = MATERIAL_IMPLICATIONS.copy()

        logger.info("Material base initialized with %d propositions", len(self.props))

    def _build_solver(self, include_commitments=True):
        """Build a Z3 solver with the current base."""
        s = Solver()

        # Add commitments as assertions
        if include_commitments:
            for name in self.commitments:
                s.add(self.props[name])

        # Add material implications as conditionals
        for antecedents, consequent in self.implications:
            ante = And([self.props[a] for a in antecedents])
            cons = self.props[consequent]
            s.add(Implies(ante, cons))

        return s

    def check_consistency(self):
        """Check if the current commitments are consistent with the implications."""
        s = self._build_solver()
        result = s.check()

        if result == sat:
            logger.info("✓ Base is consistent")
            return True
        elif result == unsat:
            logger.warning("✗ Base is inconsistent!")
            return False
        else:
            logger.warning("? Consistency check returned unknown")
            return None

    def query_consequence(self, proposition_name):
        """
        Check if a proposition is a consequence of the base.

        Returns True if denying the proposition is inconsistent with the base.
        """
        if proposition_name not in self.props:
            raise ValueError(f"Unknown proposition: {proposition_name}")

        s = self._build_solver()
        s.add(Not(self.props[proposition_name]))

        result = s.check()

        if result == unsat:
            # Denying it is inconsistent -> it's a consequence
            return True
        elif result == sat:
            # Denying it is consistent -> not a consequence
            return False
        else:
            return None

    def find_countermodel(self, proposition_name):
        """
        If a proposition is not a consequence, find a countermodel.

        Returns a dict of {prop_name: bool_value} or None if no countermodel.
        """
        if proposition_name not in self.props:
            raise ValueError(f"Unknown proposition: {proposition_name}")

        s = self._build_solver()
        s.add(Not(self.props[proposition_name]))

        if s.check() == sat:
            model = s.model()
            return {
                name: bool(model.eval(var, model_completion=True))
                for name, var in self.props.items()
            }
        return None

    def hypothetical_commitment(self, proposition_name):
        """
        Check what follows if we add a new commitment.

        Returns list of propositions that become consequences.
        """
        if proposition_name not in self.props:
            raise ValueError(f"Unknown proposition: {proposition_name}")

        # Temporarily add the commitment
        original = self.commitments.copy()
        self.commitments.add(proposition_name)

        consequences = []
        for name in self.props:
            if name not in self.commitments:
                if self.query_consequence(name):
                    consequences.append(name)

        # Restore original commitments
        self.commitments = original

        return consequences

    def hypothetical_denial(self, proposition_name):
        """
        Check if denying a proposition is consistent with remaining commitments.

        Simulates retracting the commitment and asserting its denial.
        """
        if proposition_name not in self.props:
            raise ValueError(f"Unknown proposition: {proposition_name}")

        # Build solver without the target commitment
        s = Solver()

        for name in self.commitments:
            if name != proposition_name:
                s.add(self.props[name])

        # Add the denial
        s.add(Not(self.props[proposition_name]))

        # Add implications
        for antecedents, consequent in self.implications:
            ante = And([self.props[a] for a in antecedents])
            cons = self.props[consequent]
            s.add(Implies(ante, cons))

        return s.check() == sat

    def retract(self, proposition_name):
        """Retract a commitment."""
        if proposition_name in self.commitments:
            self.commitments.remove(proposition_name)
            logger.info("Retracted: %s", proposition_name)

    def commit(self, proposition_name):
        """Add a commitment."""
        if proposition_name in self.props:
            self.commitments.add(proposition_name)
            logger.info("Committed: %s", proposition_name)

    def display_state(self):
        """Display the current dialectical state."""
        print("\n" + "="*70)
        print("MATERIAL BASE: PROV-O Section 3.1")
        print("="*70)

        print("\n## Commitments (C)")
        for name in sorted(self.commitments, key=lambda x: (int(x[1:]) if x[1:].isdigit() else float('inf'), x)):
            print(f"  {name}: {self.descriptions[name]}")

        print(f"\n## Material Implications (I) — {len(self.implications)} total")
        for ante, cons in self.implications:
            ante_str = ', '.join(ante)
            print(f"  {ante_str} |∼ {cons}")

        print("\n## Non-Implications (explicit)")
        for ni in NON_IMPLICATIONS:
            print(f"  {', '.join(ni['antecedent'])} |≁ {ni['consequent']}")
            print(f"      Note: {ni['note']}")

        print("\n" + "="*70)


# =============================================================================
# DEMONSTRATION
# =============================================================================

def main():
    """Demonstrate the material base encoding."""

    base = MaterialBase()
    base.display_state()

    print("\n" + "="*70)
    print("QUERIES")
    print("="*70)

    # Check consistency
    print("\n## Consistency Check")
    base.check_consistency()

    # Query some consequences
    print("\n## Consequence Queries")

    # These should be consequences (derived from implications)
    test_consequences = ['p18', 'p23', 'p27', 'p29', 'p30', 'p24', 'p25', 'p26', 'p28']

    for prop in test_consequences:
        is_consequence = base.query_consequence(prop)
        status = "✓ consequence" if is_consequence else "✗ not a consequence"
        print(f"  {prop}: {status}")

    # Check what would follow from a hypothetical commitment
    print("\n## Hypothetical: What if we retracted p2 (fixed aspects)?")
    can_deny_p2 = base.hypothetical_denial('p2')
    print(f"  Can consistently deny p2? {can_deny_p2}")

    if can_deny_p2:
        # Check if p18 is still a consequence without p2
        base.retract('p2')
        is_p18_still = base.query_consequence('p18')
        print(f"  Is p18 still a consequence? {is_p18_still}")
        base.commit('p2')  # Restore

    print("\n## Closure under implications")
    print("  All propositions that are consequences of the base:")
    for name in sorted(base.props.keys(), key=lambda x: (int(x[1:]) if x[1:].isdigit() else float('inf'), x)):
        if base.query_consequence(name):
            print(f"    {name}: {base.descriptions[name]}")

    print("\n" + "="*70)
    print("PROVENANCE")
    print("="*70)
    print("\nRespondent: Paul Groth (W3C Provenance Incubator Group)")
    print("Source: https://github.com/bradleypallen/prov-o-section-3.1")
    print("Framework: Hlobil & Brandom (2025), 'Reasons for Logic'")


if __name__ == "__main__":
    main()
