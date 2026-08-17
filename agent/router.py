from tools.claim_classifier import ClaimClassifier
from tools.counterexample import CounterexampleGenerator
from tools.fallacy import FallacyDetector
from tools.bias import BiasDetector


class LogicAgent:

    def __init__(self):
        self.classifier = ClaimClassifier()
        self.counterexample = CounterexampleGenerator()
        self.fallacy = FallacyDetector()
        self.bias = BiasDetector()

    def run(self, text):

        # ========================================
        # Step 1: Claim classification
        # ========================================

        claim = self.classifier.run(text)

        claim_type = claim.get("claim_type")

        # ========================================
        # Step 2: Counterexample
        # ========================================

        counterexample = None

        if claim.get("requires_counterexample", False):

            counterexample = self.counterexample.run(
                text,
                claim
            )

        # ========================================
        # Step 3: Fallacy detection
        # ========================================

        fallacy_types = {
            "universal",
            "necessary",
            "sufficient",
            "causal",
            "generalization"
        }

        if claim_type in fallacy_types:

            fallacy = self.fallacy.run(text)

        else:

            fallacy = {
                "fallacy": "none",
                "reason": "该陈述没有明显的论证结构，因此暂不判定逻辑谬误。"
            }

        # ========================================
        # Step 4: Cognitive bias detection
        # ========================================

        bias_types = {
            "universal",
            "necessary",
            "sufficient",
            "causal",
            "probabilistic",
            "generalization"
        }

        if claim_type in bias_types:

            bias = self.bias.run(text)

        else:

            bias = {
                "bias": "none",
                "reason": "该陈述本身没有明显的认知偏差证据。"
            }

        # ========================================
        # Step 5: Unified result
        # ========================================

        return {
            "input": text,

            "claim": {
                "type": claim.get("claim_type"),
                "subject": claim.get("subject"),
                "predicate": claim.get("predicate"),
                "direction": claim.get("direction"),
                "has_data": claim.get("has_data"),
                "is_absolute": claim.get("is_absolute"),
                "requires_counterexample": claim.get(
                    "requires_counterexample"
                ),
                "reason": claim.get("reason")
            },

            "counterexample": counterexample,

            "fallacy": {
                "name": fallacy.get("fallacy"),
                "reason": fallacy.get("reason")
            },

            "bias": {
                "name": bias.get("bias"),
                "reason": bias.get("reason")
            }
        }