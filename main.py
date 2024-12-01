import os.path

import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import JSONResponse

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


@app.post("/enrich_csvs")
async def enrich_csvs(request: EnrichRequest):
    if not os.path.exists(request.data_csv):
        return JSONResponse({"error": "Data_csv does not exist."}, status_code=400)

    if not os.path.exists(request.enrichment_csv):
        return JSONResponse({"error": "Enrichment_csv does not exist."}, status_code=400)

    data_df = pd.read_csv(request.data_csv)
    enrichment_df = pd.read_csv(request.enrichment_csv)

    enriched_data = intersect_and_annotate(data_df, enrichment_df)
    enriched_data_notnull = enriched_data.where(pd.notnull(enriched_data), None)

    return enriched_data_notnull.to_dict(orient="records")
