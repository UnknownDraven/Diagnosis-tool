from models.result import DiagnosticResult

class Summary:
    def __init__(self, results):
        self.results = results

    def calculate_score(self):
        score = 100
        for result in self.results:
            if result.status == "FAIL":
                score -= 40 if result.severity == "DEAL_BREAKER" else 20
            elif result.status == "WARN":
                score -= 10 if result.severity == "NEGOTIATE" else 2
        return max(0, score)

    def determine_verdict(self, score):
        if any(result.severity == "DEAL_BREAKER" and result.status != "PASS" for result in self.results):
            return "DO NOT BUY"
        elif score < 60:
            return "HIGH RISK"
        elif score < 80:
            return "PROCEED WITH CAUTION"
        return "SAFE TO BUY"

    def summarize(self):
        score = self.calculate_score()
        verdict = self.determine_verdict(score)
        return score, verdict
    
def summarize_results(results):
    summary = Summary(results)
    return summary.summarize()