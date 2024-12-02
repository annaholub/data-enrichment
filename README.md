# CSV Enrichment API

This project is a FastAPI-based microservice designed for enriching genomic data in CSV files. It merges two CSV files based on common columns and appends information from the enrichment dataset to the primary dataset.

## Features

- **Merge CSV Files**: Combines two CSV files using common columns (`chromosome`, `position`, `ref`, `alt`) and appends the `info` column from the enrichment file.
- **Validation**: Ensures both CSV files contain the required columns.
- **JSON Output**: Returns enriched data in a JSON format, replacing missing values with `null`.

## API Endpoint

### `/enrich_csvs`
- **Method**: `POST`

**Description**: Enriches a CSV file with data from another CSV file.

**Request Body**:
```json
{
  "data_csv": "data/data.csv",
  "enrichment_csv": "data/enrichment.csv"
}
```
**Response**:
```json
[
  {
    "chromosome": "chr1",
    "position": 12345,
    "ref": "A",
    "alt": "G",
    "info": "info_1"
  },
  {
    "chromosome": "chr2",
    "position": 67890,
    "ref": "T",
    "alt": "C",
    "info": null
  }
]
```
**Run the application:**
```bash
uvicorn main:app --reload
```

**Run tests:**
```bash
python -m unittest test_main.py
```

