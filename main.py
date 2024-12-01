from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import io

app = FastAPI()


class EnrichRequest(BaseModel):
    data_csv: str
    enrichment_csv: str


def intersect_and_annotate(data_csv: pd.DataFrame, enrichment_csv: pd.DataFrame) -> pd.DataFrame:
    data_columns = ['chromosome', 'position', 'ref', 'alt']
    enrichment_columns = data_columns + ['info']

    if set(data_columns) - set(data_csv.columns):
        raise ValueError("Data_csv is missing required columns.")
    if set(enrichment_columns) - set(enrichment_csv.columns):
        raise ValueError("Enrichment_csv is missing required columns.")

    enriched_data = pd.merge(
        data_csv,
        enrichment_csv,
        on=data_columns,
        how="left"
    )

    return enriched_data


def get_csv_data(csv_path: str) -> pd.DataFrame:
    try:
        with open(csv_path) as data_file:
            data = data_file.read()
            return pd.read_csv(io.StringIO(data))
    except FileNotFoundError:
        raise FileNotFoundError
    except Exception:
        raise Exception("Unexpected error opening {csv_path}")


@app.post("/enrich_csvs")
async def enrich_csvs(request: EnrichRequest):
    data_df = get_csv_data(request.data_csv)
    enrichment_df = get_csv_data(request.enrichment_csv)

    enriched_data = intersect_and_annotate(data_df, enrichment_df)
    enriched_data_notnull = enriched_data.where(pd.notnull(enriched_data), None)

    return enriched_data_notnull.to_dict(orient="records")
