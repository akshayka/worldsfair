# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
#     "polars==1.20.0",
# ]
# ///

import marimo

__generated_with = "0.10.16"
app = marimo.App(width="full")


@app.cell(hide_code=True)
def _(mo):
    mo.md("""# AI Engineer World's Fair Schedule""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""**Explore the 2024 event schedule; powered by the [marimo notebook](https://github.com/marimo-team/marimo).**""")
    return


@app.cell
def _():
    SHEET_ID = "1qgecHYn6D-94TkS-gvjSUb6dCTQ-WKZxZ3Pgzc_tJUk"
    return (SHEET_ID,)


@app.cell
def _(SHEET_ID):
    import polars as pl

    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"
    df = pl.read_csv(url)
    df = df.filter(pl.col("Date").is_not_null())
    return df, pl, url


@app.cell
def _(df, mo):
    category = mo.ui.dropdown.from_series(
        df["Category"], label="Filter by event category"
    )
    date = mo.ui.dropdown.from_series(df["Date"], label="Filter by date")
    mo.hstack([category, date], justify="start")
    return category, date


@app.cell
def _(category, date, df, mo, pl):
    _df = df.drop("Interested")
    _df = (
        _df.filter(pl.col("Category") == category.value) if category.value else _df
    )
    _df = _df.filter(pl.col("Date") == date.value) if date.value else _df
    mo.ui.table(_df, page_size=40, selection=None)
    return


@app.cell
def _():
    import marimo as mo
    return (mo,)


if __name__ == "__main__":
    app.run()
