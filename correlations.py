def predict_cbr(region, PI=None, MDD=None, N=None):
    if region == "West":
        if MDD and PI is not None:
            return round(0.25 * MDD - 0.12 * PI + 2, 2)
        elif PI is not None:
            return round(12 - 0.35 * PI, 2)

    elif region == "North":
        if MDD:
            return round(1.8 * (MDD - 1.6) * 100, 2)

    elif region == "South":
        if PI is not None:
            return round(10 - 0.3 * PI, 2)

    elif region == "East":
        if N:
            return round(2.5 * N, 2)

    return None


def predict_cu(region, PI=None, N=None):
    if N:
        return round(5.5 * N, 2)

    if region == "South" and PI:
        return round(7 * PI, 2)

    return None


def predict_phi(region, sand=None, N=None):
    if region == "West" and N:
        return min(round(27 + 0.3 * N, 2), 36)

    if region == "North" and N:
        return round(30 + 0.25 * N, 2)

    if region == "East" and sand is not None:
        return round(28 + 0.1 * sand, 2)

    return None


def subgrade_rating(CBR):
    if CBR is None:
        return "Undetermined"

    if CBR > 30:
        return "Excellent"
    elif CBR >= 15:
        return "Good"
    elif CBR >= 5:
        return "Fair"
    else:
        return "Poor"
