from typing import Tuple, List, Dict


class NodDetector:
    def __init__(self, angle: List[Dict[str, any]], threshold: float, multiplier: float):
        self.angle = angle
        self.threshold = threshold
        self.multiplier = multiplier

    def getNodTimestamp(self) -> List[Dict[str, any]]:
        current_idx = 0
        start_nod_idx = current_idx
        timestamps = []

        while (start_nod_idx < len(self.angle)):
            peak_nod_idx = start_nod_idx + 1
            start_nod_check_idx = start_nod_idx

            while ((peak_nod_idx < len(self.angle)) & (self.angle[peak_nod_idx]["pitch"] < self.angle[peak_nod_idx-1]["pitch"])):
                peak_nod_idx += 1
                while (self.angle[peak_nod_idx]["frame_num"] - self.angle[start_nod_check_idx]["frame_num"] > 25):
                    start_nod_check_idx += 1

            peak_nod_idx -= 1

            if (self.angle[start_nod_check_idx]["pitch"] - self.angle[peak_nod_idx]["pitch"] < self.threshold):
                return
        
            end_nod_idx = peak_nod_idx + 1
            long_end = False

            while ((end_nod_idx < len(self.angle)) & (self.angle[end_nod_idx]["pitch"] > self.angle[end_nod_idx-1]["pitch"])):
                end_nod_idx += 1
                if (self.angle[end_nod_idx]["frame_num"] - self.angle[peak_nod_idx]["frame_num"] <= 25):
                    end_nod_check_idx = end_nod_idx
                elif (long_end == False):
                    end_nod_check_idx = end_nod_idx - 1
                    long_end = True

            if (self.angle[end_nod_check_idx]["pitch"] - self.angle[peak_nod_idx]["pitch"] < self.threshold < self.threshold * self.multiplier):
                return
            else:
                timestamp = {
                    "start_nod_idx": start_nod_idx,
                    "start_nod_check_idx": start_nod_check_idx,
                    "peak_nod_idx": peak_nod_idx,
                    "end_nod_check_idx": end_nod_check_idx,
                    "end_nod_idx": end_nod_idx,
                    "start_nod_frame": self.angle[start_nod_idx]["frame_num"],
                    "start_nod_check_frame": self.angle[start_nod_check_idx]["frame_num"],
                    "peak_nod_frame": self.angle[peak_nod_idx]["frame_num"],
                    "end_nod_check_frame": self.angle[end_nod_check_idx]["frame_num"],
                    "end_nod_frame": self.angle[end_nod_idx]["frame_num"],
                    "start_nod_time": self.angle[start_nod_idx]["frame_num"] * 40,
                    "start_nod_check_time": self.angle[start_nod_check_idx]["frame_num"] * 40,
                    "peak_nod_time": self.angle[peak_nod_idx]["frame_num"] * 40,
                    "end_nod_check_time": self.angle[end_nod_check_idx]["frame_num"] * 40,
                    "end_nod_time": self.angle[end_nod_idx]["frame_num"] * 40,
                    "nod_angle": self.angle[start_nod_check_idx]["pitch"] - self.angle[peak_nod_idx]["pitch"]
                }

                timestamps.append(timestamp)

        return timestamps

    def getJerkTimestamp():
        pass
    def getAllTimestamp():
        pass