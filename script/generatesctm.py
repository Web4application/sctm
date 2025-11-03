import json
from datetime import datetime

class SCTMEntity:
    """
    A flexible SCTM entity that can represent any domain:
    students, health, biology, AI modules, skills, experiments, etc.
    """
    def __init__(self, name, entity_type="generic"):
        self.name = name
        self.type = entity_type          # e.g., "student", "experiment", "AI module"
        self.timestamp = datetime.now().isoformat()
        self.attributes = {}             # Lessons, metrics, confidence, tips, etc.
        self.emotions = {}               # Optional emotions/intensities
        self.additional = {}             # Extra structured data

    def add_attribute(self, key, value):
        """Add or update any domain-specific attribute"""
        self.attributes[key] = value

    def set_emotion(self, emotion_name, intensity):
        """Add or update an emotion"""
        self.emotions[emotion_name] = intensity

    def add_additional(self, category, data):
        """Add extra structured information under a category"""
        self.additional[category] = data

    def to_dict(self):
        return {
            "name": self.name,
            "type": self.type,
            "timestamp": self.timestamp,
            "attributes": self.attributes,
            "emotions": self.emotions,
            "additional": self.additional
        }

    def save_to_file(self, filename=None):
        if filename is None:
            filename = f"sctm_{self.name}.json"
        with open(filename, "w") as f:
            json.dump(self.to_dict(), f, indent=4)
        print(f"✅ SCTM entity saved to {filename}")


# ----------------------------
# Example: multi-domain SCTM
# ----------------------------
# Student domain
alice = SCTMEntity("Alice", entity_type="student")
alice.add_attribute("Physics", {"confidence": 0.92, "tip": "Visualize planets"})
alice.set_emotion("curious", 0.8)
alice.add_additional("biology", {"cell": "stem", "CRISPR": "P01"})
alice.add_additional("health", {"patient": "John"})

# Experiment domain
exp1 = SCTMEntity("GravityExperiment", entity_type="experiment")
exp1.add_attribute("setup", {"mass": "5kg", "height": "10m"})
exp1.add_attribute("result", "Acceleration measured: 9.8 m/s^2")
exp1.add_additional("notes", {"lab": "Physics Lab 1", "observer": "Alice"})

# AI module domain
ai_module = SCTMEntity("RODA_AI", entity_type="AI_module")
ai_module.add_attribute("version", "v1.0")
ai_module.add_attribute("capabilities", ["analysis", "prediction", "report_generation"])
ai_module.add_additional("training_data", {"dataset": "CIFAR-10", "size": "60k images"})

# Save entities
alice.save_to_file()
exp1.save_to_file()
ai_module.save_to_file()
