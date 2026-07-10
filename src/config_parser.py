import sys

import yaml


def parse_filters(config_path):
    """
    Reading a YAML file with filters and returning a dictionary mapping
    each filter to its glob
    """

    # Open the file safely; the "with" block closes it automatically when done
    try:
        with open(config_path, "r") as f:
            # safe_load reads the YAML as plain data (and won't run any embedded code)
            data = yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Error: Config File not Found: {config_path}")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error: Couldn't parse the YAML file: {e}")
        sys.exit(1)

    # making sure the config file has a filter section
    if not data or "filters" not in data:
        print("Error: config file must have top level 'filters' secion")
        sys.exit(1)
    # The file wraps everything under a top-level "filters" key, so return just that
    return data["filters"]
