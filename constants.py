# "Patients were evaluated at entry into the database and at intervals of approximately every 3 months...
MONTH_INTERVAL = 3
# "... thereafter for up to 4 years"
EVAL_YEARS = 4
EVAL_MONTHS = EVAL_YEARS * 12

# "Pain and urgency are subjective appraisals on a scale from 0 to 9" (0 = none, 9 = worst)
PAIN_URG_SCALE = {min: 0, max: 9}
# From the graphs, ranges from (-15 to 15)
FREQ_SCALE = {min: -15, max: 15}

# Amount of patients in the study
PATIENT_COUNT = 400
# Patient treated and untreated ratio
TREATED_RATIO = 0.47

# Evaluation time points
TIME_POINTS = ["baseline", "3mos", "6mos"]

PLOTS = [
    "Baseline",
    "At Treatment",
    "3 Months after Treatment",
    "6 Months after Treatment",
    "Difference (3 mos posttreatment)",
    "Differnece (6 mos posttreatment)",
]
PLOT_LABELS = ["Never/Later Treated", "Treated"]
