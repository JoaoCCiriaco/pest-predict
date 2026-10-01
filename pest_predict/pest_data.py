PEST_DATABASE = {
    # --- PRAGAS URBANAS ---
    "escorpiao_amarelo": {
        "name": "Escorpião-Amarelo (Tityus serrulatus)",
        "category": "Urbana",
        "breeding_months": [10, 11, 12, 1, 2, 3],
        "ideal_temp_min": 24.0, "ideal_temp_max": 34.0, "min_humidity": 65, "rain_threshold_mm": 20.0,
        "high_risk_environments": ["Residência", "Comércio", "Próximo a APP/Córrego"]
    },
    "aedes_aegypti": {
        "name": "Mosquito da Dengue / Pernilongo (Aedes aegypti / Culex)",
        "category": "Urbana",
        "breeding_months": [11, 12, 1, 2, 3, 4],
        "ideal_temp_min": 25.0, "ideal_temp_max": 32.0, "min_humidity": 70, "rain_threshold_mm": 10.0,
        "high_risk_environments": ["Residência", "Comércio", "Próximo a Córrego"]
    },
    "barata_esgoto": {
        "name": "Barata-de-Esgoto (Periplaneta americana)",
        "category": "Urbana",
        "breeding_months": [10, 11, 12, 1, 2, 3],
        "ideal_temp_min": 25.0, "ideal_temp_max": 35.0, "min_humidity": 60, "rain_threshold_mm": 15.0,
        "high_risk_environments": ["Comércio", "Residência"]
    },
    "rato_esgoto": {
        "name": "Rato-de-Esgoto / Ratazana (Rattus norvegicus)",
        "category": "Urbana",
        "breeding_months": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], # Todo o ano
        "ideal_temp_min": 20.0, "ideal_temp_max": 32.0, "min_humidity": 50, "rain_threshold_mm": 25.0,
        "high_risk_environments": ["Comércio", "Próximo a APP/Córrego"]
    },

    # --- PRAGAS AGRÍCOLAS E FLORESTAIS ---
    "sauva_limoeira": {
        "name": "Formiga Saúva (Atta sexdens) - Cortadeira",
        "category": "Agrícola/Florestal",
        "breeding_months": [9, 10, 11, 12], # Revoada na primavera
        "ideal_temp_min": 22.0, "ideal_temp_max": 30.0, "min_humidity": 65, "rain_threshold_mm": 15.0,
        "high_risk_environments": ["Eucalyptus grandis", "Eucalyptus urograndis", "Soja", "Milho"]
    },
    "quenquem": {
        "name": "Formiga Quenquém (Acromyrmex spp.)",
        "category": "Agrícola/Florestal",
        "breeding_months": [9, 10, 11, 12],
        "ideal_temp_min": 20.0, "ideal_temp_max": 28.0, "min_humidity": 60, "rain_threshold_mm": 10.0,
        "high_risk_environments": ["Eucalyptus urograndis", "Eucalyptus dunnii", "Milho"]
    },
    "vespa_da_galha": {
        "name": "Vespa-da-Galha (Leptocybe invasa)",
        "category": "Agrícola/Florestal",
        "breeding_months": [10, 11, 12, 1, 2],
        "ideal_temp_min": 25.0, "ideal_temp_max": 33.0, "min_humidity": 55, "rain_threshold_mm": 5.0,
        "high_risk_environments": ["Eucalyptus camaldulensis", "Eucalyptus tereticornis", "Eucalyptus grandis"]
    },
    "broca_cana": {
        "name": "Broca-da-Cana (Diatraea saccharalis)",
        "category": "Agrícola/Florestal",
        "breeding_months": [10, 11, 12, 1, 2, 3],
        "ideal_temp_min": 24.0, "ideal_temp_max": 30.0, "min_humidity": 70, "rain_threshold_mm": 20.0,
        "high_risk_environments": ["Cana-de-Açúcar"]
    },
    "ferrugem_soja": {
        "name": "Fungo Ferrugem-Asiática (Phakopsora pachyrhizi)",
        "category": "Agrícola/Florestal",
        "breeding_months": [11, 12, 1, 2, 3],
        "ideal_temp_min": 18.0, "ideal_temp_max": 26.0, "min_humidity": 80, "rain_threshold_mm": 30.0, # Exige alta umidade
        "high_risk_environments": ["Soja"]
    },
    "lagarta_cartucho_milho": {
        "name": "Lagarta-do-Cartucho (Spodoptera frugiperda)",
        "category": "Agrícola/Florestal",
        "breeding_months": [10, 11, 12, 1, 2, 3, 4],
        "ideal_temp_min": 22.0, "ideal_temp_max": 32.0, "min_humidity": 50, "rain_threshold_mm": 10.0,
        "high_risk_environments": ["Milho", "Soja"]
    }
}
