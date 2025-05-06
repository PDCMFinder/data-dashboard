def plot_ideogram(api_response):
    annotations = {
        "keys": ["name", "start", "length", "expression-level", "gene-type"],
        "annots": [
            {
                "chr": "1",  # Placeholder as chromosome info is missing
                "annots": [
                    [
                        f'Gene: {item["symbol"]}, Mutation: {item["consequence"]}, ref /alt allele: {item["ref_allele"]}/{item["alt_allele"]}',  # Name
                        int(float(item["seq_start_position"])),  # Start
                        1,  # Length (defaulted to 1, adjust if needed)
                        1, #int(item["read_depth"]),  # Expression level (assuming read depth)
                        1  # Gene type (default value, modify as needed)
                    ] for item in api_response
                ]
            }

        ]
    }
    return annotations