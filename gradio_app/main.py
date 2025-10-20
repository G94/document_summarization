import gradio as gr
import pandas as pd
from typing import Union, Tuple, List

def load_csv(file):
    if file is None:
        return pd.DataFrame()
    df = pd.read_csv(file)
    return df.head(2)  # show only first 5 rows

def on_cell_select(evt: gr.SelectData, table: pd.DataFrame):
    if table is None or len(table) == 0:
        return {"error": "No data loaded"}

    idx_raw: Union[Tuple[int, int], List[int], int] = evt.index

    # evt.index is usually (row, col)
    if isinstance(idx_raw, (tuple, list)):
        row_idx = idx_raw[0]
    else:
        row_idx = idx_raw

    # Ensure it's an int and valid
    try:
        row_idx = int(row_idx)
    except Exception:
        return {"error": f"Invalid selection index: {idx_raw!r}"}

    if not (0 <= row_idx < len(table)):
        return {"error": "Invalid selection"}

    row = table.iloc[row_idx]
    return row.to_dict()

def main():
    with gr.Blocks() as demo:
        gr.Markdown("## Click a cell to view the entire row")
        file_input = gr.File(label="Upload CSV")
        table = gr.DataFrame(
            value=None,
            label="First 5 rows",
            interactive=False,
            wrap=True,
            type="pandas"
        )
        row_json = gr.JSON(label="Selected Row")

        file_input.change(fn=load_csv, inputs=file_input, outputs=table)
        table.select(fn=on_cell_select, inputs=table, outputs=row_json)

    demo.launch()

if __name__ == "__main__":
    main()

    # main("/home/gsemi/summaryapp/data/train.csv")