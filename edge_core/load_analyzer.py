import numpy as np

class MicroML:
    """
    A lightweight on-device inference model for cognitive overload probability.
    Uses pure NumPy for maximum efficiency on edge devices.
    """
    def __init__(self):
        # Pre-trained weights for: [speech_rate, pause_irregularity, keyword_density, repetition_score]
        self.weights = np.array([0.5, 0.4, 0.2, 0.1]) # More sensitive to rate/pause
        self.bias = -0.6 # Lower bias to increase probability

    def sigmoid(self, z):
        return 1 / (1 + np.exp(-z))

    def predict_overload(self, features: list) -> float:
        """
        Features: [rate, pause, keywords, repetition]
        Returns: Probability of high cognitive overload (0.0 to 1.0)
        """
        z = np.dot(features, self.weights) + self.bias
        return self.sigmoid(z)

class LoadAnalyzer:
    def __init__(self):
        self.ml_model = MicroML()

    def calculate_score(self, speech_metrics: dict) -> dict:
        """
        Calculates a quantifiable overload score using the weighted formula.
        """
        # Feature Extraction
        rate = speech_metrics.get("speech_rate", 0.5)         # 0.0 to 1.0 (normalized)
        pause = speech_metrics.get("pause_irregularity", 0.5) # 0.0 to 1.0
        keywords = speech_metrics.get("keyword_density", 0.5) # 0.0 to 1.0
        repetition = speech_metrics.get("repetition_score", 0.5) # 0.0 to 1.0

        features = [rate, pause, keywords, repetition]
        
        # 1. Classical Weighted Score (Interpretable)
        weighted_score = (
            0.4 * rate + 
            0.3 * pause + 
            0.2 * keywords + 
            0.1 * repetition
        )

        # 2. ML Probability (Advanced Inference)
        ml_prob = self.ml_model.predict_overload(features)

        # Normalize total score
        total_score = (weighted_score + ml_prob) / 2
        
        level = "LOW"
        if total_score > 0.35: level = "MEDIUM"
        if total_score > 0.6: level = "HIGH"

        return {
            "total_score": round(total_score, 2),
            "ml_probability": round(ml_prob, 2),
            "level": level,
            "features_used": features
        }

if __name__ == "__main__":
    analyzer = LoadAnalyzer()
    # Mock high-stress metrics
    metrics = {"speech_rate": 0.9, "pause_irregularity": 0.8, "keyword_density": 0.7, "repetition_score": 0.6}
    print(analyzer.calculate_score(metrics))
