import json
from statistics import mean

def calculate_iou(box1, box2):
    x1, y1, w1, h1 = box1
    x2, y2, w2, h2 = box2

    intersection_x1 = max(x1, x2)
    intersection_y1 = max(y1, y2)
    intersection_x2 = min(x1 + w1, x2 + w2)
    intersection_y2 = min(y1 + h1, y2 + h2)

    intersection_area = max(0, intersection_x2 - intersection_x1) * max(0, intersection_y2 - intersection_y1)

    union_area = w1 * h1 + w2 * h2 - intersection_area

    iou = intersection_area / union_area if union_area > 0 else 0

    return iou

def organize_boxes(boxlist1, boxlist2):
    """Organize boxlists to pair correctly each detected box to the labelized box corresponding.

    Args:
        boxlist1: ground truth boxes.
        boxlist2: detected boxes.

    Returns:
        organized_boxlist1, organized_boxlist2: organized boxlists.
        iou_list: list of iou for each couple of boxes.
    """
    organized_boxlist1 = []
    organized_boxlist2 = []
    iou_list = []

    while boxlist1 and boxlist2:
        max_iou = 0
        best_index1 = 0
        best_index2 = 0

        for i, box1 in enumerate(boxlist1):
            for j, box2 in enumerate(boxlist2):
                iou = calculate_iou(box1, box2)
                if iou > max_iou:
                    max_iou = iou
                    best_index1 = i
                    best_index2 = j

        organized_boxlist1.append(boxlist1.pop(best_index1))
        organized_boxlist2.append(boxlist2.pop(best_index2))
        iou_list.append(max_iou)

    return iou_list

def mean_iou(boxlist1, boxlist2):
    iou_list = organize_boxes(boxlist1, boxlist2)

    return mean(iou_list)

def calculate_precision_recall_iou_threshold(ground_truth_boxes, detected_boxes, iou_threshold):
    true_positives = 0
    false_positives = 0
    false_negatives = 0

    for detected_box in detected_boxes:
        iou_found = False

        for ground_truth_box in ground_truth_boxes:
            iou = calculate_iou(detected_box, ground_truth_box)

            if iou >= iou_threshold:
                true_positives += 1
                iou_found = True
                break

        if not iou_found:
            false_positives += 1

    false_negatives = len(ground_truth_boxes) - true_positives

    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0

    return precision, recall, true_positives, false_positives, false_negatives

def convert_coordinates(box_trbl):
    """Convert coordinates from "top, right, bottom, left" to "x, y, w, h"."""
    top, right, bottom, left = box_trbl

    x = left
    y = top
    w = right - left
    h = bottom - top

    return [x, y, w, h]

def evaluation(label_dict, detected_boxes, iou_threshold):
    ground_truth = label_dict[1]
    ground_truth_boxes = [ground_truth[i][:4] for i in range(label_dict[0])]

    if len(detected_boxes) == 0:
        print("Evaluation impossible since no visage where detected")
        return 0, 0, label_dict[0]
    
    for i, box in enumerate(detected_boxes):
        # tuple to list
        box = list(box)

        detected_boxes[i] = convert_coordinates(box)

    mean_iou_calculated = mean_iou(ground_truth_boxes.copy(), detected_boxes.copy())
    precision, recall, true_positives, false_positives, false_negatives = calculate_precision_recall_iou_threshold(ground_truth_boxes, detected_boxes, iou_threshold)

    print(f"Average IoU: {mean_iou_calculated}\nPrecision: {precision}\nRecall: {recall}")

    return true_positives, false_positives, false_negatives
