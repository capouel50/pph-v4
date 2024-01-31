def convert_quantity(quantity, from_unit, to_unit):
    # Ajoutez ici la logique de conversion pour chaque unité
    conversion_rates = {
        'kg': {
            'kg': 1,
            'g': 1000,
            'mg': 1000000,
        },
        'g': {
            'kg': 0.001,
            'g': 1,
            'mg': 1000,
            'gttes': 55,
        },
        'mg': {
            'kg': 0.000001,
            'g': 0.001,
            'mg': 1,
        },
        'gttes': {
             'g': 0.018,
             'mg': 18,
        },
        'l': {
            'l': 1,
            'ml': 1000,
        },
        'ml': {
            'l': 0.001,
            'ml': 1,
        },
    }

    if from_unit in conversion_rates and to_unit in conversion_rates[from_unit]:
        conversion_rate = conversion_rates[from_unit][to_unit]
        converted_quantity = quantity * conversion_rate
        return converted_quantity
    else:
        # Gérez ici le cas où la conversion n'est pas possible
        raise ValueError("Conversion non supportée")