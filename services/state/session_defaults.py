import streamlit as st

# we need to initialise the session state with default values for the progress trackers, workout plan, common angles, and status fields. This is done in the initial_session_defaults function, which is called at the start of the script. The function checks if each key is already in the session state, and if not, it sets it to the default value.



def initial_session_defaults():
    defaults = {
        # The progress trackers
        "reps": 0,
        "target_sets": 0,
        "reps_per_set": 0,
        "sets_completed": 0,
        "current_set_reps": 0,
        "workout_complete": False,
        "last_notified_sets_completed": 0,
        "last_notified_workout_complete": False,
        "last_saved_sets_completed": 0,
        "set_cycle_started_at": 0.0,
        "last_exercise_type": "Squats",

        # Workout plan (set before starting)
        "workout_started": False,
        "plan_exercise": "Squats",
        "plan_sets": 3,
        "plan_reps": 10,

        # Common Angles
        "knee_angle": 0,
        "back_angle": 0,
        "elbow_angle": 0,
        "front_knee_angle": 0,
        "torso_angle": 0,

        # Status fields
        "depth_status": "N/A",
        "body_alignment": "N/A",
        "hip_status": "N/A",
        "shoulder_status": "N/A",
        "swing_status": "N/A",
        "extension_status": "N/A",
        "back_arch_status": "N/A",
        "balance_status": "N/A",
    }

# it is important to inject the default values in the session state only if they are not already present. This is because the session state persists across reruns of the script, and we don't want to overwrite any values that have already been set by the user or by the app logic. Therefore, we check if each key is already in the session state, and if not, we set it to the default value.


    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value