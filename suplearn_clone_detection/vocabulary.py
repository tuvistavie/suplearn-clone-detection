import csv
import json
import numpy as np


class Vocabulary:
    def __init__(self, filepath, fallback_empty_value=True):
        self._parse_file(filepath)
        self.fallback_empty_value = fallback_empty_value

    def _parse_file(self, filepath):
        with open(filepath, "r", newline="") as f:
            reader = csv.DictReader(f, delimiter="\t", quoting=csv.QUOTE_NONE)
            self.rows = []
            self.has_values = "value" in reader.fieldnames
            self.headers = reader.fieldnames
            self.vocabulary = {}
            for row in reader:
                if self.has_values:
                    row["value"] = json.loads(row.get("value")) if row.get("value") else None
                self.rows.append(row)
                key = (row["type"],)
                if self.has_values:
                    key += (row["value"],)
                letter_id = np.int32(int(row["id"]))
                self.vocabulary[key] = letter_id

    def __len__(self):
        return len(self.vocabulary)

    def __getitem__(self, node):
        if not self.has_values:
            return self.vocabulary[(node["type"],)]

        key = (node["type"], node.get("value"))
        result = self.vocabulary.get(key)
        if result is not None:
            return result
        elif self.fallback_empty_value:
            return self.vocabulary[(node["type"], None)]
        else:
            raise KeyError(key)

    def save(self, path, offset=0):
        with open(path, "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.headers, delimiter="\t")
            writer.writeheader()
            for i in range(offset):
                row = dict(id=i, type="offset-{0}".format(i), metaType="padding", count=0)
                if self.has_values:
                    row["value"] = "padding"
                writer.writerow(row)
            for row in self.rows:
                row = row.copy()
                row["id"] = str(int(row["id"]) + offset)
                writer.writerow(row)
