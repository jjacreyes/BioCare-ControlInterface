import json
import os

class PresetManager:

    def __init__(self, preset_dir = "presets"):
        self.preset_dir = preset_dir
        os.makedirs(self.preset_dir, exist_ok=True)


    # === Preset folder path ====
    def _preset_path(self, preset_name):
        """Preset folder paths from preset names"""
        return os.path.joins(self.preset_dir, f"{preset_name}.json")
    

        # ====== Creating New Empty Preset =========
    def create_emptyPreset(self, preset_name):
        "Creates new preset with 3 empty (FingerPositions = 0) gestures."

        path = self._preset_path(preset_name)

        preset_data = {
            "Gesture1": {
                "name": "Gesture1",
                "FingerPositions": [0, 0, 0, 0]
            },
            "Gesture2": {
                "name": "Gesture2",
                "FingerPositions": [0, 0, 0, 0]
            },
            "Gesture3": {
                "name": "Gesture3",
                "FingerPositions": [0, 0, 0, 0]
            }
        }

        with open(path, "w") as file:
            json.dump(preset_data, file, indent = 4)

    def load_presets(self, preset_name):
        """Load and return presets from dictionary"""
        path = self._preset_path(preset_name)

        if not os.path.exists(path):
            raise ValueError(f"Preset: {preset_name} does not exist.")

        with open(path, "r") as file:
            return json.load(file)

    def save_preset(self, preset_name, preset_data):
        """Save preset dictionary back into file"""
        path = self._preset_path(preset_name)

        with open(path, "w") as file:
            json.dump(preset_data, file, indent = 4)

    # ===== Editing Gestures ========
    def edit_gesture(self, preset_name, gesture_id, new_name, finger_positions):
        """ Allows users to edit existing gestures. As well as to edit newly created ones
        to change from default.
        """

        preset = self.load_preset(preset_name)

        if gesture_id not in preset:
            raise ValueError(f"Gestured_id: {gesture_id} does not exist within preset.")
        
        preset[gesture_id] = {
            "name": new_name,
            "FingerPositions": finger_positions
        }

        self.save_preset(preset_name, preset)


    def list_presets (self):
        """Return all preset names"""
        files = os.listdir(self.preset_dir)
        return [os.path.splitext(f)[0] for f in files if f.endswith(".json")]

    # ===== Deleting Presets ======
    def delete_preset(self, preset_name):
        """Delete preset JSON file"""
        path = self._preset_path(preset_name)

        if os.path.exists(path):
            os.remove(path)
        else:
            raise ValueError(f"Preset {preset_name} does not exist.")