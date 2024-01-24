import os
import click

def jaccard_similarity(set1, set2):
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union if union != 0 else 0

def calculate_global_jaccard(ground_truth_folder, predictions_folder, verbose):
    ground_truth_subdirectories = [os.path.join(ground_truth_folder, d) for d in os.listdir(ground_truth_folder) if os.path.isdir(os.path.join(ground_truth_folder, d)) and d != "_all"]
    predictions_folder_subdirectories = [os.path.join(predictions_folder, d) for d in os.listdir(predictions_folder) if os.path.isdir(os.path.join(predictions_folder, d))]

    sum_jaccard = 0

    for gt_d in ground_truth_subdirectories:
        if verbose:
            print(f"DIR_NAME: {gt_d}")
        gt_set = set([f for f in os.listdir(gt_d)])
        max_jaccard = 0
        for pred_d in predictions_folder_subdirectories:
            if verbose:
                print(f"PRED_NUM: {pred_d}")
            pred_set = set([f for f in os.listdir(pred_d) if f.endswith('.jpg')])
            jaccard_idx = jaccard_similarity(gt_set, pred_set)
            if verbose:
                print(f"JACCARD: {jaccard_idx}")
            if jaccard_idx > max_jaccard:
                max_jaccard = jaccard_idx
        if verbose:
            print(f"MAX JACCARD: {max_jaccard}")
        sum_jaccard += max_jaccard
    
    return sum_jaccard / len(ground_truth_subdirectories)


@click.command()
@click.option('--verbose', '-v', is_flag=True, help='Activate the verbose', required=False)
def main(verbose):
    ground_truth_folder = "data/lfw_cropped"
    predictions_folder = "src/architecture/images/persons"

    global_jaccard = calculate_global_jaccard(ground_truth_folder, predictions_folder, verbose)
    print(f"Global Jaccard Index: {global_jaccard}")


if __name__ == "__main__":
    main()
