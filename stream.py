import time
import json
import argparse
import pandas as pd
import os
from datetime import datetime

parser = argparse.ArgumentParser()
parser.add_argument('--folder', '-f', type=str, required=True)
parser.add_argument('--batch-size', '-b', type=int, required=True)
parser.add_argument('--split', '-s', type=str, default='train')
parser.add_argument('--sleep', '-t', type=int, default=5)
args = parser.parse_args()

OUTPUT_DIR = "stream_data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

class Dataset:
    def generate_batches(self, csv_path, batch_size, split):
        df = pd.read_csv(csv_path)
        df = df.sample(frac=1, random_state=42).reset_index(drop=True)
        train_size = int(0.8 * len(df))
        df = df[:train_size] if split == 'train' else df[train_size:]
        texts, labels = df['text'].tolist(), df['label'].tolist()

        for i in range(0, len(texts), batch_size):
            yield texts[i:i+batch_size], labels[i:i+batch_size]

    def write_batches_to_files(self, path, batch_size, split):
        for texts, labels in self.generate_batches(path, batch_size, split):
            batch = [
                {"text": texts[i], "label": int(labels[i])}
                for i in range(len(texts))
            ]
            filename = f"batch_{datetime.now().strftime('%Y%m%d_%H%M%S%f')}.json"
            filepath = os.path.join(OUTPUT_DIR, filename)
            with open(filepath, "w", encoding="utf-8") as f:
                for item in batch:
                    f.write(json.dumps(item) + "\n")
            print(f"Wrote {len(batch)} records to {filepath}")
            time.sleep(args.sleep)

if __name__ == '__main__':
    dataset = Dataset()
    dataset.write_batches_to_files(os.path.join(args.folder, 'movie_sample.csv'), args.batch_size, args.split)