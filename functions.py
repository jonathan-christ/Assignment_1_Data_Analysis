import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import constants as c

# patient data generation
def generatePatientData():
    data = []
    totalEvalCount = len(c.TIME_POINTS)

    for patientId in range(c.PATIENT_COUNT):
        # radomize treatment status (consistent across time points)
        treatmentStatus = np.random.choice(
            ["treated", "untreated"], 
            p=[c.TREATED_RATIO, 1 - c.TREATED_RATIO]
        )
        
        # generate symptom scores for each time point
        pain = np.random.randint(c.PAIN_URG_SCALE["min"], c.PAIN_URG_SCALE["max"] + 1, totalEvalCount)
        urgency = np.random.randint(c.PAIN_URG_SCALE["min"], c.PAIN_URG_SCALE["max"] + 1, totalEvalCount)
        frequency = np.random.randint(c.FREQ_SCALE["min"], c.FREQ_SCALE["max"] + 1, totalEvalCount)
        
        # add data for each time point
        for i, timePoint in enumerate(c.TIME_POINTS):
            data.append({
                "patientId": patientId,
                "treatmentStatus": treatmentStatus,
                "timePoint": timePoint,
                "pain": pain[i],
                "urgency": urgency[i],
                "frequency": frequency[i]
            })

    # convert list of dictionaries to DataFrame
    df = pd.DataFrame(data)
    return df
     
# difference between treated and control patients
def calculateDataDiff(patientData):
    pass # TBA

    
