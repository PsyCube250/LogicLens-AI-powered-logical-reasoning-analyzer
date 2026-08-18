from tools.claim_classifier import ClaimClassifier
from tools.counterexample import CounterexampleGenerator
from tools.fact_checker import FactChecker
from tools.fallacy import FallacyDetector
from tools.bias import BiasDetector


class LogicAgent:

    def __init__(self):
        self.classifier = ClaimClassifier()
        self.counterexample = CounterexampleGenerator()
        self.fact_checker = FactChecker()
        self.fallacy = FallacyDetector()
        self.bias = BiasDetector()

    def run(self, text):

        # ========================================
        # Step 1: Claim classification
        # ========================================

        claim = self.classifier.run(text)

        claim_type = claim.get("claim_type")

        # ========================================
        # Step 2a: Counterexample
        # ========================================
        #
        # 适用于可以用"满足前提但违反结论"的单个实例直接推翻的
        # 关系型命题（universal / necessary / sufficient /
        # generalization），也适用于趋势/存在性命题
        # （probabilistic / existential）—— 这类命题虽然不能被
        # 单个反例直接推翻，但可以用真实统计数据去验证/反驳其
        # 趋势判断，交给 CounterexampleGenerator 内部判断是否
        # 需要检索。

        evidence_backed_types = {
            "probabilistic",
            "existential",
        }

        counterexample = None

        if claim.get("requires_counterexample", False) or claim_type in evidence_backed_types:

            counterexample = self.counterexample.run(
                text,
                claim
            )

        # ========================================
        # Step 2b: Fact check
        # ========================================
        #
        # statistical 类命题本身就是在陈述一个数据/比例，
        # 不适用"反例"框架，而是需要核实这个数据本身准不准确。

        fact_check = None

        if claim_type == "statistical":

            fact_check = self.fact_checker.run(
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

            "fact_check": fact_check,

            "fallacy": {
                "name": fallacy.get("fallacy"),
                "reason": fallacy.get("reason")
            },

            "bias": {
                "name": bias.get("bias"),
                "reason": bias.get("reason")
            }
        }
