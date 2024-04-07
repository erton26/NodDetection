from typing import List, Dict


class NodDetector:
    def __init__(self, angle: List[Dict[str, any]], fps: int, threshold: float, multiplier: float):
        self.angle = angle
        self.fps = fps
        self.threshold = threshold
        self.multiplier = multiplier

    def getNodTimestamp(self) -> List[Dict[str, any]]:
        current_idx = 0
        start_nod_idx = current_idx
        timestamps = []

        while (start_nod_idx < len(self.angle)):
            peak_nod_idx = start_nod_idx + 1
            start_nod_check_idx = start_nod_idx
            long_start = False

            if (peak_nod_idx >= len(self.angle)):
                return timestamps

            while (self.angle[peak_nod_idx]["pitch"] < self.angle[peak_nod_idx-1]["pitch"]):
                peak_nod_idx += 1
                if (peak_nod_idx >= len(self.angle)):
                    return timestamps
                while (self.angle[peak_nod_idx]["frame_num"] - self.angle[start_nod_check_idx]["frame_num"] > self.fps):
                    long_start = True
                    start_nod_check_idx += 1

            peak_nod_idx -= 1

            if (self.angle[start_nod_check_idx]["pitch"] - self.angle[peak_nod_idx]["pitch"] < self.threshold):
                start_nod_idx = peak_nod_idx + 1
                continue
        
            end_nod_idx = peak_nod_idx + 1
            long_end = False

            if (end_nod_idx >= len(self.angle)):
                    return timestamps

            while (self.angle[end_nod_idx]["pitch"] > self.angle[end_nod_idx-1]["pitch"]):
                end_nod_idx += 1
                if (end_nod_idx >= len(self.angle)):
                    return timestamps
                if (self.angle[end_nod_idx]["frame_num"] - self.angle[peak_nod_idx]["frame_num"] <= self.fps):
                    end_nod_check_idx = end_nod_idx
                elif (not long_end):
                    end_nod_check_idx = end_nod_idx - 1
                    long_end = True

            if (end_nod_check_idx == end_nod_idx):
                end_nod_check_idx -= 1

            end_nod_idx -= 1

            if (self.angle[end_nod_check_idx]["pitch"] - self.angle[peak_nod_idx]["pitch"] < self.threshold * self.multiplier):
                start_nod_idx = end_nod_check_idx + 1
                continue
            else:
                timestamp = {
                    "start_nod_time": self.angle[start_nod_idx]["frame_num"] * 1000 / self.fps,
                    "start_nod_check_time": self.angle[start_nod_check_idx]["frame_num"] * 1000 / self.fps,
                    "peak_nod_time": self.angle[peak_nod_idx]["frame_num"] * 1000 / self.fps,
                    "end_nod_check_time": self.angle[end_nod_check_idx]["frame_num"] * 1000 / self.fps,
                    "end_nod_time": self.angle[end_nod_idx]["frame_num"] * 1000 / self.fps,
                    "nod_angle": self.angle[start_nod_check_idx]["pitch"] - self.angle[peak_nod_idx]["pitch"],
                    "long_start": long_start,
                    "long_end" : long_end
                }

                timestamps.append(timestamp)

            start_nod_idx = end_nod_idx + 1

        return timestamps

    def getJerkTimestamp(self) -> List[Dict[str, any]]:
        current_idx = 0
        start_nod_idx = current_idx
        timestamps = []

        while (start_nod_idx < len(self.angle)):
            peak_nod_idx = start_nod_idx + 1
            start_nod_check_idx = start_nod_idx
            long_start = False

            if (peak_nod_idx >= len(self.angle)):
                return timestamps

            while (self.angle[peak_nod_idx]["pitch"] > self.angle[peak_nod_idx-1]["pitch"]):
                peak_nod_idx += 1
                if (peak_nod_idx >= len(self.angle)):
                    return timestamps
                while (self.angle[peak_nod_idx]["frame_num"] - self.angle[start_nod_check_idx]["frame_num"] > self.fps):
                    long_start = True
                    start_nod_check_idx += 1

            peak_nod_idx -= 1

            if (self.angle[peak_nod_idx]["pitch"] - self.angle[start_nod_check_idx]["pitch"] < self.threshold):
                start_nod_idx = peak_nod_idx + 1
                continue
        
            end_nod_idx = peak_nod_idx + 1
            long_end = False

            if (end_nod_idx >= len(self.angle)):
                    return timestamps

            while (self.angle[end_nod_idx]["pitch"] < self.angle[end_nod_idx-1]["pitch"]):
                end_nod_idx += 1
                if (end_nod_idx >= len(self.angle)):
                    return timestamps
                if (self.angle[end_nod_idx]["frame_num"] - self.angle[peak_nod_idx]["frame_num"] <= self.fps):
                    end_nod_check_idx = end_nod_idx
                elif (not long_end):
                    end_nod_check_idx = end_nod_idx - 1
                    long_end = True

            if (end_nod_check_idx == end_nod_idx):
                end_nod_check_idx -= 1

            end_nod_idx -= 1

            if (self.angle[peak_nod_idx]["pitch"] - self.angle[end_nod_check_idx]["pitch"] < self.threshold * self.multiplier):
                start_nod_idx = end_nod_check_idx + 1
                continue
            else:
                timestamp = {
                    "start_nod_time": self.angle[start_nod_idx]["frame_num"] * 1000 / self.fps,
                    "start_nod_check_time": self.angle[start_nod_check_idx]["frame_num"] * 1000 / self.fps,
                    "peak_nod_time": self.angle[peak_nod_idx]["frame_num"] * 1000 / self.fps,
                    "end_nod_check_time": self.angle[end_nod_check_idx]["frame_num"] * 1000 / self.fps,
                    "end_nod_time": self.angle[end_nod_idx]["frame_num"] * 1000 / self.fps,
                    "nod_angle": self.angle[start_nod_check_idx]["pitch"] - self.angle[peak_nod_idx]["pitch"],
                    "long_start": long_start,
                    "long_end" : long_end
                }

                timestamps.append(timestamp)

            start_nod_idx = end_nod_idx + 1

        return timestamps

    def getAllTimestamp(self) -> List[Dict[str, any]]:
        nod_timestamps = self.getNodTimestamp()
        jerk_timestamps = self.getJerkTimestamp()

        timestamps = nod_timestamps + jerk_timestamps
        timestamps = sorted(timestamps, key=lambda x: x['start_nod_time'])

        return timestamps