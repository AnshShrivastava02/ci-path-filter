import argparse

from src.config_parser import parse_filters
from src.filter_evaluator import evaluate_all
from src.output_writer import write_env_file

"""reads the config path, output path, and changed files from the command line, then runs parse → evaluate → write to produce the .env result, and only does this when the file is run directly"""


def main():
    # set up command line arguments the tool accepts
    parser = argparse.ArgumentParser(
        description="Filter CI/CD pipelines based on which files changed"
    )
    parser.add_argument("config", help="Path to the filters.yaml file")
    parser.add_argument("output", help="Path to write the env output file")
    parser.add_argument("changed_files", nargs="+", help="List of changed files")

    args = parser.parse_args()

    # Run the complete pipeline parse>evaluate>write
    filters = parse_filters(args.config)
    results = evaluate_all(filters, args.changed_files)
    write_env_file(results, args.output)

    # Print a summary so the user sees what happened
    print(f"Wrote {len(results)} filter results to {args.output}")


if __name__ == "__main__":
    main()
