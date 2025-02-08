import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy.spatial.distance import mahalanobis

import constants as c


def generate_patient_data():
    patients = []
    for patient_id in range(
        1, c.PATIENT_COUNT + 1
    ):  # Total of c.PATIENT_COUNT patients
        treatment_status = np.random.choice(
            c.PATIENT_GROUPS, p=[c.TREATED_RATIO, 1 - c.TREATED_RATIO]
        )
        # Create baseline data for each patient
        baseline_data = {
            "timePoint": "baseline",
            "patientId": patient_id,
            "treatmentStatus": treatment_status,
        }
        for symptom in c.SYMPTOMS:
            baseline_data[symptom] = np.random.uniform(
                c.PAIN_URG_SCALE["min"], c.PAIN_URG_SCALE["max"]
            )  # Random values for pain/urgency
        patients.append(baseline_data)

        # Create data for other time points
        for time in c.TIME_POINTS[1:]:
            treatment_data = {
                "timePoint": time,
                "patientId": patient_id,
                "treatmentStatus": treatment_status,
            }
            for symptom in c.SYMPTOMS:
                treatment_data[symptom] = np.random.uniform(
                    c.PAIN_URG_SCALE["min"], c.PAIN_URG_SCALE["max"]
                )  # Random values for symptoms
            patients.append(treatment_data)

    # Convert list of dictionaries to DataFrame
    patient_data_df = pd.DataFrame(patients)
    return patient_data_df


def find_nearest_control(data, treated_data):
    treated_patient_time = treated_data["timePoint"].iloc[0]

    # Filter potential control patients (untreated and time <= treated patient's time)
    potential_controls = data[
        (data["treatmentStatus"] == "untreated")
        & (data["timePoint"] <= treated_patient_time)
    ]

    if potential_controls.empty:
        print(
            f"No potential controls found for treated patient at time {treated_patient_time}."
        )
        return None

    # Drop rows with NaN values in symptom columns
    potential_controls = potential_controls.dropna(subset=c.SYMPTOMS)

    # Covariance matrix for Mahalanobis distance
    cov_matrix = np.cov(potential_controls[c.SYMPTOMS].T)
    inv_cov_matrix = np.linalg.pinv(cov_matrix)

    # Calculate Mahalanobis distance for each potential control patient
    distances = [
        mahalanobis(row, treated_data[c.SYMPTOMS].values[0], inv_cov_matrix)
        for row in potential_controls[c.SYMPTOMS].values
    ]
    min_distance_index = np.argmin(distances)
    return potential_controls.iloc[min_distance_index]


def calculate_differences(data):
    # Step 1: Ensure baseline data exists for each patient
    baseline_data = data[data["timePoint"] == "baseline"]

    # Ensure only patients with baseline data are considered
    data_cleaned = data[data["patientId"].isin(baseline_data["patientId"])]

    # Step 2: Create a list to store new rows for diff time points
    new_rows = []

    # Step 3: Calculate differences and create new rows
    time_points = ["3mos", "6mos"]
    diff_columns = ["pain", "urgency", "frequency"]

    for patient in data_cleaned["patientId"].unique():
        baseline_row = baseline_data[baseline_data["patientId"] == patient]

        if not baseline_row.empty:
            baseline_values = baseline_row[diff_columns].values[
                0
            ]  # Get baseline values

            for time_point in time_points:
                time_point_row = data_cleaned[
                    (data_cleaned["patientId"] == patient)
                    & (data_cleaned["timePoint"] == time_point)
                ]

                if not time_point_row.empty:
                    time_point_values = time_point_row[diff_columns].values[
                        0
                    ]  # Get time point values

                    # Calculate differences
                    diff_values = time_point_values - baseline_values

                    # Create new rows for the diff time points (3mos, 6mos)
                    new_row = {
                        "patientId": patient,
                        "treatmentStatus": time_point_row["treatmentStatus"].values[0],
                        "timePoint": f"diff{time_point[0]}",  # diff3 or diff6
                        "pain": diff_values[0],
                        "urgency": diff_values[1],
                        "frequency": diff_values[2],
                    }
                    new_rows.append(new_row)

    # Convert new rows into a DataFrame and append to the original data
    diff_data = pd.DataFrame(new_rows)

    # Step 4: Append the diff data to the cleaned data
    data_cleaned = pd.concat([data_cleaned, diff_data], ignore_index=True)

    return data_cleaned


def plot_boxplots_grid(data, column, label):
    fig, axes = plt.subplots(3, 2, figsize=(10, 10))

    time_points = c.TIME_POINTS + ["diff3", "diff6"]
    plot_labels = c.PLOTS

    treatment_order = [
        "untreated",
        "treated",
    ]  # Order for x-axis: Never/Later Treated -> Treated

    for i, (time_point, time_label) in enumerate(zip(time_points, plot_labels)):
        row, col = divmod(i, 2)
        plot_data = data[data["timePoint"] == time_point]

        if plot_data.empty:
            print(f"Warning: No data available for {time_point}, skipping plot.")
            continue  # Skip if no data

        sns.boxplot(
            data=plot_data,
            x="treatmentStatus",
            y=column,
            ax=axes[row, col],
            order=treatment_order,
        )

        axes[row, col].set_title(time_label, fontsize=14)
        axes[row, col].set_xticks([0, 1], c.PLOT_LABELS)
        axes[row, col].set_ylabel(label)
        axes[row, col].set_xlabel("")
        axes[row, col].grid(axis="y", linestyle="--", alpha=0.7)

    plt.subplots_adjust(wspace=0.5, hspace=0.5)
    plt.show()
