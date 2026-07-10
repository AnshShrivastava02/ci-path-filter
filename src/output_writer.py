def write_env_file(results, output_path):
    """Purpose of this file is to convert our output according to the expected output from .env file"""
    lines = []  # empty list to store result

    for name, matched in results.items():
        # parsing the results for key and value
        value = "true" if matched else "false"
        lines.append(f"{name}={value}")
        # fstring to append name = value

    # joining with new lines to acquire expected output
    with open(output_path, "w") as f:
        f.write("\n".join(lines) + "\n")
