from core.base_exercise import BaseExercise

# The LungesDetector class is a specialized implementation of the BaseExercise class, designed to detect and analyze lunges using pose estimation landmarks. It defines thresholds for knee angles to determine the stages of a lunge (up and down) and counts repetitions based on these stages. The class also calculates the angle of the torso and provides feedback on balance status based on the lateral offset between the shoulders and hips.

class LungesDetector(BaseExercise):
    DOWN_THRESHOLD = 100
    UP_THRESHOLD = 160
    MIN_VISIBILITY = 0.7
    BALANCE_TOLERANCE = 0.10

    LEFT_HIP = 23
    LEFT_KNEE = 25
    LEFT_ANKLE = 27
    RIGHT_HIP = 24
    RIGHT_KNEE = 26
    RIGHT_ANKLE = 28
    LEFT_SHOULDER = 11
    RIGHT_SHOULDER = 12

    def __init__(self):
        super().__init__()

    def reset(self) -> None:
        self.reps = 0
        self.stage = None

    def process(self, landmarks) -> dict:
        left_knee_angle = self.calculate_angle(
            self.get_point(landmarks, self.LEFT_HIP),
            self.get_point(landmarks, self.LEFT_KNEE),
            self.get_point(landmarks, self.LEFT_ANKLE),
        )

        right_knee_angle = self.calculate_angle(
            self.get_point(landmarks, self.RIGHT_HIP),
            self.get_point(landmarks, self.RIGHT_KNEE),
            self.get_point(landmarks, self.RIGHT_ANKLE),
        )

        # if the left knee angle is smaller than the right leg, it means the left leg is the one that is bent in front, while the right is relatively straighter behind. So we will use the left leg landmarks to calculate the knee angle and torso angle. Else we will use the right leg
        if left_knee_angle <= right_knee_angle:
            front_knee_angle = left_knee_angle
            front_hip_idx = self.LEFT_HIP
            front_knee_idx = self.LEFT_KNEE
            front_ankle_idx = self.LEFT_ANKLE
            shoulder_idx_for_torso = self.LEFT_SHOULDER
        else:
            front_knee_angle = right_knee_angle
            front_hip_idx = self.RIGHT_HIP
            front_knee_idx = self.RIGHT_KNEE
            front_ankle_idx = self.RIGHT_ANKLE
            shoulder_idx_for_torso = self.RIGHT_SHOULDER

        key_landmarks_visible = landmarks[front_hip_idx].visibility > self.MIN_VISIBILITY and landmarks[front_knee_idx].visibility > self.MIN_VISIBILITY and landmarks[front_ankle_idx].visibility > self.MIN_VISIBILITY

        if key_landmarks_visible:
            if front_knee_angle < self.DOWN_THRESHOLD:
                self.stage = "down"

            if front_knee_angle > self.UP_THRESHOLD and self.stage == "down":
                self.stage = "up"
                self.reps += 1

        # angle between the shoulder, hip, and knee of the front leg. This will give us an idea of how upright the torso is during the lunge.
        torso_angle = self.calculate_angle(
            self.get_point(landmarks, shoulder_idx_for_torso),
            self.get_point(landmarks, front_hip_idx),
            self.get_point(landmarks, front_knee_idx),
        )

        # Check if the user is losing their balance and leaning to the side. We do this by finding the center of their chest and the center of their hips. The 'lateral_offset' is just measuring how far the chest is drifting left or right from the hips.

        shoulder_mid_x = (landmarks[self.LEFT_SHOULDER].x + landmarks[self.RIGHT_SHOULDER].x) / 2
        hip_mid_x = (landmarks[self.LEFT_HIP].x + landmarks[self.RIGHT_HIP].x) / 2
        lateral_offset = abs(shoulder_mid_x - hip_mid_x)

        if lateral_offset <= self.BALANCE_TOLERANCE:
            balance_status = "BALANCED"
        else:
            balance_status = "OFF BALANCE"

        # returning a dictionary of parameters to be displayed to the user
        return {
            "reps": self.reps,
            "front_knee_angle": int(front_knee_angle),
            "torso_angle": int(torso_angle),
            "balance_status": balance_status,
        }
    