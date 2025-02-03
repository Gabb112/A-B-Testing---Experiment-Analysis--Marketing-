import os
from ab_analyzer import ABAnalyzer

if __name__ == "__main__":
    project_dir = os.getcwd()
    raw_data_dir = os.path.join(project_dir, "data", "raw", "1")
    output_dir = os.path.join(project_dir, "reports")

    try:
        ab_analyzer = ABAnalyzer(raw_data_dir, output_dir)
        ab_analyzer.run_analysis()
    except ValueError as e:
        print(e)
    except FileNotFoundError as e:
        print(e)
