import os
import pandas as pd
from sklearn.metrics import cohen_kappa_score


def calculate_kappa_score(data):
    # Extract the clarification turn and type annotations
    annotator1_turn = data['clarification turn'].fillna('')
    annotator2_turn = data['clarification turn.1'].fillna('')
    annotator1_type = data['clarification type'].fillna('')
    annotator2_type = data['clarification type.1'].fillna('')

    # Align the annotations for comparison
    aligned_turns = [(a1, a2) for a1, a2 in zip(annotator1_turn, annotator2_turn)]
    aligned_types = [(a1, a2) for a1, a2 in zip(annotator1_type, annotator2_type)]

    # Calculate Cohen's Kappa for clarification turn
    kappa_turn = cohen_kappa_score([a1 for a1, a2 in aligned_turns], [a2 for a1, a2 in aligned_turns])

    # Calculate Cohen's Kappa for clarification type
    kappa_type = cohen_kappa_score([a1 for a1, a2 in aligned_types], [a2 for a1, a2 in aligned_types])

    return kappa_turn, kappa_type


def main():
    directory = 'csv_annotations'
    kappa_turns = []
    kappa_types = []

    # Iterate over all CSV files in the directory
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            path = os.path.join(directory, filename)
            data = pd.read_csv(path)
            kappa_turn, kappa_type = calculate_kappa_score(data)
            kappa_turns.append(kappa_turn)
            kappa_types.append(kappa_type)

    # Calculate average Kappa scores
    average_kappa_turn = sum(kappa_turns) / len(kappa_turns)
    average_kappa_type = sum(kappa_types) / len(kappa_types)

    # Print the average Kappa scores rounded to 3 decimals
    print(f"Average Cohen's Kappa for Clarification Turn: {average_kappa_turn:.3f}")
    print(f"Average Cohen's Kappa for Clarification Type: {average_kappa_type:.3f}")


if __name__ == '__main__':
    main()
