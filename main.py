from cProfile import label
import os
import sys
import time
current_dir = os.getcwd()
sys.path.append(current_dir)
from src.llmisolator import LocalLLMClient
from src.reader import read_txt_file_line_by_line
from tqdm import tqdm
import json
import matplotlib.pyplot as plt

PATH = f'data/content.txt'
CHUNK = 10

PROMPT = f"""
You are a data extraction specialist. Your task is to extract iPhone price data from the following text. Your goal is to create a structured dataset optimized for direct use with the Pandas library. Specifically, you must capture the order of price appearances as a proxy for temporal evolution.

Text Input: [Paste the complete text string here]

Instructions:

Model & Storage: For each iPhone model, identify the storage size.
Price Extraction: Extract the price associated with each model and storage combination.
Order-Based Temporal Proxy: Crucially, assign a 'timestamp' value to each record based on its position within the original text. Treat the text as a sequence – the first record has a timestamp of 1, the second has a timestamp of 2, and so on. This will reflect the order of prices presented.
Offer Capture: Flag any promotional offers alongside the price and timestamp.
Data Structure: Generate a JSON array of dictionaries. Each dictionary represents a single iPhone price record.


JSON Output Format (Example):

List[ dict ]
dict = "timestamp": 3,
"model": "genericiphonemodel#3",
"storage": "256GB",
"price": 84300,
"offer": "None"

etc

Notes for the AI Agent:

Prioritize the order-based timestamping. It's the core requirement.
Assume that a lack of explicit offer designation means there’s no promotional offer.
Handle any ambiguous price mentions carefully, aiming for the most consistent representation.
Key Changes & Rationale:

Explicit Timestamp: The prompt directly instructs the AI to generate a 'timestamp' field.
JSON Format: JSON is ideal for Pandas because it's easily parsed into dataframes.
Simplified Structure: The JSON structure is designed to be clean and straightforward.
Clearer Instructions: Emphasis on consistent representation and handling ambiguity.

Text Input begins: 

"""
def save_plot():
    with open("output.json", 'r', encoding='utf-8') as file:
        data = json.load(file)
    models = [dat['model'] for dat in data]
    uniqueModels = list(set(models))
    plt.figure(figsize=(8, 6))
    plt.title(f'Price Trend Over Time: ')
    for model in uniqueModels:
        prices = [float(dat['price']) for dat in data if dat['model'] == model and dat['price'] is not None]
        plt.plot(prices, label=model)
    plt.legend()
    plt.savefig("prices.png")
    plt.show()

def main():
    client = LocalLLMClient()
    lines = read_txt_file_line_by_line(PATH)
    starttime = time.time()
    output = f'output.json'
    chunks = len(lines) / CHUNK
    print("chunks: ", chunks)
    results = []
    for i in tqdm(range(int(400)), desc= "Processing chunks: ", leave=False): 
        document = " ".join(lines[i:CHUNK+i])
        prompt = f"{PROMPT} {document}"
        summary = client.generate(prompt, temperature=0.3)
        summary = summary.replace('`', '')
        summary = summary.replace('json', '')
        try:
            summ = json.loads(summary)
            for item in summ:
                results.append(item)
        except Exception as e:
            print(f"Error: {e}")
            pass
    with open(output, 'w') as f:
        json.dump(results, f, indent=4)
    processing_time = round(time.time() - starttime, 2)
    print("Processing Time: ", processing_time)
    print("price_list Done!")

if __name__ == "__main__":
    main()
    save_plot()