def adjust_confidence(base_conf, N=None, MDD=None, region_data_level=100):
    confidence = base_conf

    if N is None:
        confidence -= 0.15

    if MDD is None:
        confidence -= 0.10

    if region_data_level < 100:
        confidence -= 0.10

    return round(max(confidence, 0.4), 2)
