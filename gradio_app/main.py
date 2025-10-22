import gradio as gr
import pandas as pd
from typing import Union, Tuple, List
import requests


API_URL = "http://localhost:8080/api/v1/summary"
API_URL_EVALUATE = "http://localhost:8080/api/v1/evaluate"
def get_summary(text, abstract, paper_id):
    try:
        # Ensure paper_id is an int (gr.Number already gives numeric, but double-check)
        paper_id = int(paper_id)
    except (TypeError, ValueError):
        return "Error: paper_id must be an integer."

    payload = {
        "text": text,
        "abstract": abstract,
        "paper_id": paper_id,
    }

    try:
        resp = requests.post(API_URL, json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        return data.get("summary", "No summary field in response.")
    except requests.RequestException as e:
        return f"Request error: {e}"
    except ValueError:
        return "Error: Could not parse JSON response."


def evaluate_results(text, abstract, paper_id):
    payload_evaluate = {
        "generated_text": text,
        "abstract": abstract,
        "paper_id": paper_id,
    }    

    try:
        resp = requests.post(API_URL_EVALUATE, json=payload_evaluate, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        if isinstance(data, list):
            metrics = data
        validated = [
            {"name": m.get("name"), "score": float(m.get("score", 0.0))}
            for m in metrics
            if isinstance(m, dict) and "name" in m
        ]
        return data.get("metrics", "No response.")
        return validated
        
    except requests.RequestException as e:
        return f"Request error: {e}"
    except ValueError:
        return "Error: Could not parse JSON response."
    

with gr.Blocks(title="Social Science Paper Summarizer") as demo:
    gr.Markdown("Enter fields for SummaryRequest")
    with gr.Row():
        text_in = gr.Textbox(label="Text", lines=6, placeholder="Main body or content to summarize")
        abstract_in = gr.Textbox(label="Abstract", lines=4, placeholder="Paper abstract or context")
    paper_id_in = gr.Number(label="Paper ID", precision=0, value=1)

    out = gr.Textbox(label="Summary (response)", lines=8)
    metrics = gr.Textbox(label="Metrics Evaluation", lines=8)
    btn = gr.Button("Submit")
    btn_evaluate = gr.Button("Evaluate")
    btn.click(get_summary, inputs=[text_in, abstract_in, paper_id_in], outputs=out)
    btn_evaluate.click(evaluate_results, inputs=[abstract_in, out, paper_id_in], outputs=metrics)
demo.launch()


# def load_csv(file):
#     if file is None:
#         return pd.DataFrame()
#     df = pd.read_csv(file)
#     return df.head(2)  # show only first 5 rows

# def on_cell_select(evt: gr.SelectData, table: pd.DataFrame):
#     if table is None or len(table) == 0:
#         return {"error": "No data loaded"}

#     idx_raw: Union[Tuple[int, int], List[int], int] = evt.index

#     # evt.index is usually (row, col)
#     if isinstance(idx_raw, (tuple, list)):
#         row_idx = idx_raw[0]
#     else:
#         row_idx = idx_raw

#     # Ensure it's an int and valid
#     try:
#         row_idx = int(row_idx)
#     except Exception:
#         return {"error": f"Invalid selection index: {idx_raw!r}"}

#     if not (0 <= row_idx < len(table)):
#         return {"error": "Invalid selection"}

#     row = table.iloc[row_idx]
#     return row.to_dict()

# def main():
#     with gr.Blocks() as demo:
#         gr.Markdown("## Click a cell to view the entire row")
#         file_input = gr.File(label="Upload CSV")
#         table = gr.DataFrame(
#             value=None,
#             label="First 5 rows",
#             interactive=False,
#             wrap=True,
#             type="pandas"
#         )
#         row_json = gr.JSON(label="Selected Row")

#         file_input.change(fn=load_csv, inputs=file_input, outputs=table)
#         table.select(fn=on_cell_select, inputs=table, outputs=row_json)

#     demo.launch()

# if __name__ == "__main__":
#     main()

    # main("/home/gsemi/summaryapp/data/train.csv")