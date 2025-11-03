import json
from datetime import datetime

class SCTM:
    def __init__(self, student_name):
        self.student = student_name
        self.timestamp = datetime.now().isoformat()
        self.lessons = {}          # {lesson_name: {"confidence": float, "tip": str}}
        self.emotions = {}         # {emotion_name: intensity (0-1)}
        self.additional = {}       # {category: {subdata}}

    # Add or update a lesson
    def add_lesson(self, lesson_name, confidence=0.0, tip=""):
        self.lessons[lesson_name] = {"confidence": confidence, "tip": tip}

    # Add or update an emotion
    def set_emotion(self, emotion_name, intensity):
        self.emotions[emotion_name] = intensity

    # Add additional structured data
    def add_additional(self, category, data):
        self.additional[category] = data

    # Export the full SCTM object as a dictionary
    def to_dict(self):
        return {
            "student": self.student,
            "timestamp": self.timestamp,
            "lessons": self.lessons,
            "emotions": self.emotions,
            "additional": self.additional
        }

    # Save to JSON file
    def save_to_file(self, filename=None):
        if filename is None:
            filename = f"sctm_{self.student}.json"
        with open(filename, "w") as f:
            json.dump(self.to_dict(), f, indent=4)
        print(f"✅ SCTM saved to {filename}")

# ----------------------------
# Example usage
# ----------------------------
sctm_alice = SCTM("Alice")
sctm_alice.add_lesson("Physics", confidence=0.92, tip="Visualize planets pulling each other")
sctm_alice.set_emotion("curious", 0.8)
sctm_alice.add_additional("biology", {"cell": "stem", "CRISPR": "P01"})
sctm_alice.add_additional("health", {"patient": "John"})

# Save to file
sctm_alice.save_to_file()
