import yaml


def parse_filters(config_path):
    """
    Reading a YAML file with filters and returning a dictionary mapping
    each filter to its glob
    """
    # Open the file safely; the "with" block closes it automatically when done
    with open(config_path, "r") as f:
        # safe_load reads the YAML as plain data (and won't run any embedded code)
        data = yaml.safe_load(f)

        # The file wraps everything under a top-level "filters" key, so return just that
        return data["filters"]
