def predict_top_opd(
    model,
    vector
):

    probabilities = (
        model.predict_proba(vector)
    )

    labels = model.classes_

    top1 = []
    top2 = []

    for row in probabilities:

        sorted_idx = (
            row.argsort()[::-1]
        )

        top1.append(
            labels[sorted_idx[0]]
        )

        top2.append(
            labels[sorted_idx[1]]
        )

    return top1, top2