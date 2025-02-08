import functions as fn

data = fn.generate_patient_data()
# Calculate the difference
data_with_diff = fn.calculate_differences(data)
print(data_with_diff)
fn.plot_boxplots_grid(data_with_diff, "pain", "Pain Score")
fn.plot_boxplots_grid(data_with_diff, "urgency", "Urgency Score")
fn.plot_boxplots_grid(data_with_diff, "frequency", "Frequency Score")
