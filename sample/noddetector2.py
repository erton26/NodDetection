from typing import List, Dict


class NodDetector2:
    def __init__(self, angles: List[Dict[str, any]], threshold: float, multiplier: float, timelimit: float, fps: int = 25):
        self.angles = angles
        self.fps = fps
        self.threshold = threshold
        self.multiplier = multiplier
        self.timelimit = timelimit

    def getDiff(self) -> List[Dict[str, any]]:
        diffs = []
        for idx in range(1, len(self.angles)):
            diff = {
                "start_frame_num": self.angles[idx-1]["frame_num"],
                "end_frame_num": self.angles[idx]["frame_num"],
                "start_frame_timestamp": self.angles[idx-1]["frame_timestamp"],
                "end_frame_timestamp": self.angles[idx]["frame_timestamp"],
                "pitch_diff": self.angles[idx]["pitch"] - self.angles[idx-1]["pitch"],
                "yaw_diff": self.angles[idx]["yaw"] - self.angles[idx-1]["yaw"],
                "roll_diff": self.angles[idx]["yaw"] - self.angles[idx-1]["yaw"],
            }
            diffs.append(diff)
        
        return diffs
    
    def getPitchSymbolRange(self) -> List[Dict[str, any]]:
        
          
    def getNodTimestamp(self) -> List[Dict[str, any]]:
        