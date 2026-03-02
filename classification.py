import math

def classify_soil(LL, PL, fines, sand=None, gravel=None, Gs=None, color=None):

    confidence = 1.0

    # Compute PI
    if LL is None or PL is None:
        PI = None
        confidence -= 0.5
    else:
        PI = LL - PL

    if fines is None:
        confidence -= 0.3

    # Fine vs coarse
    if fines is not None and fines >= 50:
        if PI is None:
            USCS = "Fine-grained (undetermined)"
        else:
            PI_A = 0.73 * (LL - 20)

            if PI >= PI_A:
                USCS = "CL" if LL < 50 else "CH"
            else:
                USCS = "ML" if LL < 50 else "MH"
    else:
        # Coarse-grained
        if sand is None or gravel is None:
            soil_type = "S"
            confidence -= 0.1
        else:
            soil_type = "S" if sand >= gravel else "G"

        if fines is None:
            USCS = soil_type + "?"
        elif fines < 5:
            USCS = soil_type + "P"
        elif fines <= 12:
            USCS = soil_type + "P-M"
        else:
            if PI is None:
                USCS = soil_type + "M"
            else:
                PI_A = 0.73 * (LL - 20)
                USCS = soil_type + ("C" if PI >= PI_A else "M")

    # AASHTO classification
    AASHTO = classify_aashto(LL, PI, fines)

    # Lateritic flag
    soil_group = "Lateritic" if is_lateritic(LL, PI, fines, Gs, color) else "Non-lateritic"

    confidence = max(confidence, 0.4)

    return USCS, AASHTO, soil_group, PI, round(confidence, 2)


def classify_aashto(LL, PI, fines):
    if fines is None or LL is None or PI is None:
        return "AASHTO undetermined"

    if fines <= 35:
        if fines <= 10 and PI == 0:
            return "A-3"
        elif fines <= 15 and PI <= 6:
            return "A-1-b"
        elif PI <= 10:
            return "A-2-4"
        else:
            return "A-2-6"
    else:
        if LL <= 40 and PI <= 10:
            return "A-4"
        elif LL <= 40 and PI > 10:
            return "A-6"
        elif LL > 40 and PI <= 10:
            return "A-5"
        else:
            if PI <= LL - 30:
                return "A-7-5"
            else:
                return "A-7-6"


def is_lateritic(LL, PI, fines, Gs, color):
    if LL and PI and fines:
        if 30 <= LL <= 60 and 10 <= PI <= 25 and 25 <= fines <= 60:
            if Gs and Gs >= 2.60:
                return True
            if color and color.lower() in ["red", "reddish", "brown", "reddish brown"]:
                return True
    return False
