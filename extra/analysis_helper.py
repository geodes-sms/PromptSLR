from pydantic_core.core_schema import simple_ser_schema
from sklearn.metrics import (
    balanced_accuracy_score,
    matthews_corrcoef,
    recall_score,
    precision_score,
    confusion_matrix,
    cohen_kappa_score,
)
from statsmodels.stats.inter_rater import fleiss_kappa
import numpy as np
import pandas as pd


# helper functions
def get_binary_count(df, is_true_label="is_true", confidence_label="Confidence"):
    # Check the current distribution of 'is_true'
    df.groupby(confidence_label)[is_true_label].value_counts()

    # Ensure 'is_true' is binary (0 or 1)
    df[is_true_label] = df[is_true_label].apply(lambda x: 1 if x else 0)

    # Convert 'is_true' to integer type (if not already binary)
    df[is_true_label] = df[is_true_label].astype(int)

    # Get the binary counts for each unique 'Confidence'
    binary_counts = df.groupby(confidence_label)[is_true_label].value_counts()

    return binary_counts


def print_percentage_confidence(
    binary_counts, print_all=True, is_true_label="is_true", total_corpus=None
):
    outer_bound = binary_counts.index.max()[0]
    for confidence in [8, 9]:
        total_corpus = total_corpus or binary_counts.sum()
        sliced_data = binary_counts.loc[confidence:outer_bound]
        correct = (
            sliced_data.xs(1, level=is_true_label, drop_level=False).sum()
            if 1 in sliced_data.index.get_level_values(is_true_label)
            else 0
        )
        incorrect = (
            sliced_data.xs(0, level=is_true_label, drop_level=False).sum()
            if 0 in sliced_data.index.get_level_values(is_true_label)
            else 0
        )

        total = correct + incorrect
        accuracy = correct / total if total > 0 else 0
        work_saved = (total / total_corpus) if total_corpus > 0 else 0
        if print_all:
            print(
                f"Confidence {confidence}: Accuracy = {accuracy:.4f}, Work Saved = {work_saved:.4f}"
            )
        return accuracy, work_saved


def calculate_expected_value(row):
    """
    Calculates the expected value based on SELECTION and COT decisions and their confidences.
    """
    # Convert decisions to binary values (1 for INCLUDE, 0 otherwise)
    # simple_decision = 1 if row["SIMPLE_Decision"] == "INCLUDE" else 0
    selection_decision = 1 if row["SELECTION_Decision"] == "INCLUDE" else 0
    cot_decision = 1 if row["COT_Decision"] == "INCLUDE" else 0

    # Calculate the total confidence
    total_confidence = (
        row["SELECTION_Confidence"]
        + row["COT_Confidence"]  # + row["SIMPLE_Confidence"]
    )

    # Avoid division by zero
    if total_confidence == 0:
        return 0

    # Calculate the weighted expected value
    expected_value = (
        (selection_decision * (row["SELECTION_Confidence"] / total_confidence))
        + (cot_decision * (row["COT_Confidence"] / total_confidence))
        # + (simple_decision * (row["SIMPLE_Confidence"] / total_confidence))
    )
    return expected_value


def calculate_avg_decision(row):
    """
    Calculates the average decision based on available keys (either two or three),
    using decisions and confidences to determine the final decision.

    Handles:
    - Two keys (e.g., COT and SELECTION)
    - Three keys (e.g., SIMPLE, COT, SELECTION)
    """
    # Extract decisions and confidences, defaulting to 0 if missing
    decisions = {
        "COT": 1 if row.get("COT_Decision") == "INCLUDE" else 0,
        "SELECTION": 1 if row.get("SELECTION_Decision") == "INCLUDE" else 0,
    }
    confidences = {
        "COT": row.get("COT_Confidence", 0),
        "SELECTION": row.get("SELECTION_Confidence", 0),
    }

    # Add SIMPLE if it exists in the row
    if "SIMPLE_Decision" in row and "SIMPLE_Confidence" in row:
        decisions["SIMPLE"] = 1 if row.get("SIMPLE_Decision") == "INCLUDE" else 0
        confidences["SIMPLE"] = row.get("SIMPLE_Confidence", 0)

    # Aggregate decisions by type and track associated confidences
    decision_counts = {}
    for key, decision in decisions.items():
        if decision not in decision_counts:
            decision_counts[decision] = []
        decision_counts[decision].append(key)

    # Majority decision logic
    for decision, keys in decision_counts.items():
        if len(keys) >= 2:  # Majority decision found
            avg_confidence = sum(confidences[key] for key in keys) / len(keys)

            # Identify the key(s) not in the majority decision group
            other_keys = [key for key in confidences if key not in keys]

            # If there are other keys, compare confidences
            if other_keys:
                other_confidence = sum(confidences[key] for key in other_keys) / len(
                    other_keys
                )
                if avg_confidence >= other_confidence:
                    return "INCLUDE" if decision == 1 else "EXCLUDE"
                else:
                    return "INCLUDE" if decisions[other_keys[0]] == 1 else "EXCLUDE"
            else:
                # If no other keys, return the majority decision
                return "INCLUDE" if decision == 1 else "EXCLUDE"

    # If no majority, return the decision with the highest confidence
    highest_confidence_key = max(confidences, key=confidences.get)
    return "INCLUDE" if decisions[highest_confidence_key] == 1 else "EXCLUDE"


def calculate_fleiss_kappa_for_group(group):
    """
    Calculates Fleiss' Kappa for a given group of data.

    Parameters:
    group (pd.DataFrame): A grouped DataFrame.

    Returns:
    float: Fleiss' Kappa for the group.
    """
    # Reset index to ensure row indices match matrix rows, while preserving original index
    group = group.reset_index(drop=True)

    # Get all unique decisions across the group
    unique_decisions = pd.unique(group.values.ravel())  # Unique values in the group
    decision_matrix = np.zeros((len(group), len(unique_decisions)), dtype=int)

    # Create a mapping from decisions to matrix columns
    decision_mapping = {decision: idx for idx, decision in enumerate(unique_decisions)}

    # Fill the decision matrix
    for row_idx, row in group.iterrows():
        for decision in row:
            decision_matrix[row_idx, decision_mapping[decision]] += 1

    # Calculate Fleiss' Kappa using the decision matrix
    return fleiss_kappa(decision_matrix, method="fleiss")


def calculate_metrics(df, results_df, confidences, confidence_threshold, total_samples):
    """
    Calculate binary classification metrics.
    Filters data based on the confidence threshold.

    Metrics: Balanced Accuracy, Recall, Specificity, NPV, Precision, MCC, WSP, Accuracy in WSP
    """
    # Filter based on confidence threshold
    mask = confidences >= confidence_threshold
    true_labels = true_labels[mask]
    predicted_labels = predicted_labels[mask]
    filtered_samples = mask.sum()  # Number of samples above threshold
    # Handle edge cases for empty or invalid filtered data
    if len(true_labels) == 0 or len(predicted_labels) == 0:
        return [None] * 8

    # Confusion matrix
    tn, fp, fn, tp = confusion_matrix(
        true_labels, predicted_labels, labels=["EXCLUDE", "INCLUDE"]
    ).ravel()

    # Metrics calculations
    # rec = tp / (tp + fn) if (tp + fn) > 0 else 0
    rec = recall_score(true_labels, predicted_labels, pos_label="INCLUDE")

    # spec = tn / (tn + fp) if (tn + fp) > 0 else 0
    spec = recall_score(true_labels, predicted_labels, pos_label="EXCLUDE")

    # bAcc = (rec + spec) / 2
    bAcc = balanced_accuracy_score(true_labels, predicted_labels)
    npv = tn / (tn + fn) if (tn + fn) > 0 else 0
    # prec = tp / (tp + fp) if (tp + fp) > 0 else 0
    prec = precision_score(true_labels, predicted_labels, pos_label="INCLUDE")
    # mcc = (tp * tn - fp * fn) / ((tp + fp) * (tp + fn) * (tn + fp) * (tn + fn)) ** 0.5 if (tp + fp) > 0 and (tp + fn) > 0 and (tn + fp) > 0 and (tn + fn) > 0 else 0
    mcc = matthews_corrcoef(true_labels, predicted_labels)

    # Work Saved Percentage (WSP)
    wsp = filtered_samples / total_samples if total_samples > 0 else 0

    # Accuracy in WSP (filtered subset)
    accuracy_in_wsp = (tp + tn) / (tp + tn + fp + fn) if (tp + tn + fp + fn) > 0 else 0

    return [bAcc, rec, spec, npv, prec, mcc, wsp, accuracy_in_wsp]


def calculate_metrics_for_classic_prompts(
    df,
    confidence_threshold,
    prediction_col_name,
    confidence_col_name,
    true_label_col_name,
    is_true_label,
    is_bernoulli_distributed=False,
    is_bernoulli_confidence=False,
):
    """
    Calculate binary classification metrics for classic prompts.
    Filters data based on the confidence threshold.

    Metrics: Balanced Accuracy, Recall, Specificity, NPV, Precision, MCC, WSP, Accuracy in WSP
    """
    # Filter based on confidence threshold

    # Extract true labels and predicted labels
    true_labels = df[true_label_col_name].sort_index()
    predicted_labels = df[prediction_col_name].sort_index()

    if not is_bernoulli_distributed:
        mask = df[confidence_col_name] >= confidence_threshold
    elif is_bernoulli_confidence:
        mask = (
            (df["COT_Confidence"] >= confidence_threshold)
            & (df["SELECTION_Confidence"] >= confidence_threshold)
            # & (df["SIMPLE_Confidence"] >= confidence_threshold)
        )
    else:
        mask = df.index

    # print(get_binary_count(df, is_true_label, confidence_col_name))

    # Confusion matrix
    tn, fp, fn, tp = confusion_matrix(
        true_labels, predicted_labels, labels=["EXCLUDE", "INCLUDE"]
    ).ravel()

    tn_thresh, fp_thresh, fn_thresh, tp_thresh = confusion_matrix(
        true_labels[mask], predicted_labels[mask], labels=["EXCLUDE", "INCLUDE"]
    ).ravel()

    # Metrics calculations
    rec = recall_score(true_labels[mask], predicted_labels[mask], pos_label="INCLUDE")
    spec = recall_score(true_labels[mask], predicted_labels[mask], pos_label="EXCLUDE")
    bAcc = (rec + spec) / 2
    npv = tn_thresh / (tn_thresh + fn_thresh)
    prec = precision_score(
        true_labels[mask], predicted_labels[mask], pos_label="INCLUDE"
    )
    # mcc = (
    #     (tp * tn - fp * fn) / ((tp + fp) * (tp + fn) * (tn + fp) * (tn + fn)) ** 0.5
    #     if (tp + fp) > 0 and (tp + fn) > 0 and (tn + fp) > 0 and (tn + fn) > 0
    #     else 0
    # )
    mcc = matthews_corrcoef(true_labels[mask], predicted_labels[mask])

    wsp = (tp_thresh + tn_thresh + fp_thresh + fn_thresh) / (tp + tn + fp + fn)
    accuracy_in_wsp = (tp_thresh + tn_thresh) / (
        tp_thresh + tn_thresh + fp_thresh + fn_thresh
    )
    return [bAcc, rec, spec, npv, prec, mcc, wsp, accuracy_in_wsp]
