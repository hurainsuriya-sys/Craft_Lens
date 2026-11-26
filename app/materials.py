
def estimate_materials(craft_data):

    materials = craft_data.get("possible_materials", [])

    craft_name = craft_data.get("craft_name", "Unknown craft")

    wire_type = craft_data.get("wire_type", "Unknown")

    difficulty = craft_data.get("difficulty", "Unknown")

    material_analysis = []

    for material in materials:

        material_analysis.append({
            "material": material,
            "estimated_quantity": "Needs manual estimation",
            "purpose": "Used in the craft design",
            "confidence": "Visual identification only"
        })

    wire_information = {
        "wire_type": wire_type,
        "estimated_thickness": craft_data.get(
            "estimated_thickness", "Unknown"
        ),
        "wire_material": craft_data.get(
            "wire_material", "Unknown"
        ),
        "flexibility": craft_data.get(
            "wire_flexibility", "Unknown"
        )
    }

    return {
        "craft_name": craft_name,
        "difficulty": difficulty,
        "materials": material_analysis,
        "wire_information": wire_information,
        "note": (
            "Material quantities are approximate. "
            "Exact quantities depend on craft size and design."
        )
    }
