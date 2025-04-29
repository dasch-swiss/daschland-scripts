import json
from typing import Any

# Load the source JSON schema (Daschland_Nodegoat.json)
with open("Daschland_Nodegoat.json", "r") as file:
    nodegoat_data = json.load(file)

# Load the target schema structure (daschland.json)
with open("daschland.json", "r") as file:
    daschland_schema = json.load(file)


# Function to transform the nodegoat data to match daschland schema
def transform_to_daschland(nodegoat_data: dict[str, Any]) -> dict[str, Any]:
    transformed_data: dict[str, Any] = {}

    # Example: Mapping the nodegoat 'Book' type to daschland 'Book' structure
    for type_name, type_data in nodegoat_data["data"]["types"].items():
        if type_name == "Book":  # Example for Book, add similar transformations for other types
            transformed_data["book"] = {
                "name": type_data["type"]["name"],
                "description": type_data["object_descriptions"]["Description"]["object_description_name"],
                "author": type_data["object_descriptions"]["Author"]["object_description_name"],
                "publication_date": type_data["object_descriptions"]["Publication Date"][
                    "object_description_value_type_base"
                ],
                # Add more mappings based on the schema requirements
            }

    return transformed_data


# Apply the transformation
transformed_data = transform_to_daschland(nodegoat_data)

# Save the transformed data to a new JSON file
with open("transformed_daschland.json", "w") as file:
    json.dump(transformed_data, file, indent=4)

print("Transformation complete. Output saved to 'transformed_daschland.json'.")
