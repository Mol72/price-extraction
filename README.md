# Price Extraction Project - README

This project aims to extract iPhone price data from a text file and generate a structured JSON dataset, suitable for direct use with Pandas.  The core of the project is prioritizing the order of the price mentions to act as a temporal proxy.

## Project Overview

The script reads a text file (`data/content.txt`), utilizes a local LLM client (`LocalLLMClient`) to extract price information, and outputs a JSON file (`output.json`) containing the extracted data.  The JSON structure is designed for easy integration with Pandas.

**Install Dependencies:**
    ```bash
    pip install matplotlib tqdm
    ```
2.  **LocalLLMClient:**  This project assumes the existence of a `LocalLLMClient` module (likely defined in `src/llmisolator.py`). This client handles the interaction with the LLM. Make sure this is set up correctly.
3.  **Data File:** Ensure the `data/content.txt` file exists and contains the text from which to extract prices.
4.  **Run the Script:**
    ```bash
    python main.py
    ```

## Script Breakdown

*`main()`: The main function that orchestrates the entire process.
*Initializes a `LocalLLMClient`.
*Reads the text file line by line using `read_txt_file_line_by_line`.
*Splits the text into chunks for processing.
*Iterates through the chunks, generating prompts for the LLM, and collecting the results.
*Saves the extracted data to `output.json` using `json.dump`.
*Prints the processing time.

*`save_plot()`:  Generates a plot showing the price trends over time, based on the `output.json` file.  This function creates a scatter plot of the price for each iPhone model.

## Key Features & Design Choices

***Order-Based Temporal Proxy:** The `timestamp` field in the JSON output is crucial. The order in which prices are extracted from the text determines the value of this timestamp.
***JSON Output Format:**  The JSON structure is designed to be efficient and optimized for Pandas.
***Chunking:**  The text is split into chunks to manage the LLM's context window.
***Temperature:** A low temperature (0.3) is used to encourage the LLM to generate more consistent and deterministic outputs.
***Error Handling:** A basic `try...except` block handles potential errors during JSON parsing, preventing the script from crashing.
***Tqdm Progress Bar**:  A progress bar provides real-time feedback during the chunk processing.
***Prompt Engineering:** The prompt is carefully crafted to instruct the LLM on the desired output format and priorities.

## Potential Improvements

***More Robust Error Handling:** Implement more detailed error handling, including logging.
***Dynamic Chunk Size:**  Instead of a fixed chunk size, consider dynamically adjusting the chunk size based on the LLM's context window limits and processing speed.
***Prompt Refinement:** Experiment with different prompt variations to optimize the extraction process.
***Data Validation:** Add data validation checks to ensure the extracted prices are valid numbers.
***Logging**: Add logging to track the execution, troubleshoot issues, and monitor performance.
***Configuration:** Use a configuration file to manage parameters such as the LLM client, chunk size, and temperature.
