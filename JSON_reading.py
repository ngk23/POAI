import json
import csv
import os

def read_apod_results(file_path="apod_results.json"):
    try:
        file_path = os.path.abspath(file_path)
        with open(file_path, "r") as file:
            data = json.load(file)
            return data
    except FileNotFoundError as error:
        print(f"The file '{file_path}' was not found: {error}")
    except PermissionError as error:
        print(f"Permission denied to read the file '{file_path}': {error}")
    except json.JSONDecodeError as error:
        print(f"The file '{file_path}' is invalid JSON. Error details: {error}")
        print(f"Error occurred at line {error.lineno}, column {error.colno} in the file.")
    except Exception as error:
        print(f"An unexpected error occurred: {error}")
    return None


def print_apod_titles_and_dates(file_path="apod_results.json"):
    data = read_apod_results(file_path)
    if data:
        print("APOD Titles and Dates:")
        for complex_entry in data:
            print(f"Date: {complex_entry['date']}, Title: {complex_entry['title']}")
    else:
        print("No data to display.")

def analyze_media(file_path="apod_results.json"):
    data = read_apod_results(file_path)
    if data:
        image_sum = 0
        video_sum = 0
        longest_explanation_length = 0
        date_with_longest_explanation = ""
        for entry in data:
            if entry.get("media_type") == "image":
                image_sum += 1
            elif entry.get("media_type") == "video":
                video_sum += 1
            explanation_length = len(entry.get("explanation", ""))
            if explanation_length > longest_explanation_length:
                longest_explanation_length = explanation_length
                date_with_longest_explanation = entry.get("date", "")
        print("Analysis Results:")
        print(f"Image count: {image_sum}")
        print(f"Video count: {video_sum}")
        print(f"Date with longest explanation: {date_with_longest_explanation}")
    else:
        print("No data available for analysis.")

def write_apod_result_to_csv(file_path="apod_results.json", csv_file="apod_result.csv"):
    data = read_apod_results(file_path)
    if data:
        csv_file = os.path.abspath(csv_file)
        write_header = not os.path.exists(csv_file)
        with open(csv_file, mode="a", newline="") as csvfile:
            fieldnames = ["Date", "Title", "Media Type", "URL"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if write_header:
                writer.writeheader()
            for entry in data:
                writer.writerow({
                    "Date": entry["date"],
                    "Title": entry["title"],
                    "Media Type": entry["media_type"],
                    "URL": entry["url"]
                })
        print(f"APOD data has been written to '{csv_file}'.")
    else:
        print("No data available to write to CSV.")

def main():
    print("Printing date and title of each APOD entry")
    print_apod_titles_and_dates()

    print("\nAnalyzing media types and most detailed explanation")
    analyze_media()

    print("\nWriting APOD results to CSV")
    write_apod_result_to_csv()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occurred during execution: {e}")
