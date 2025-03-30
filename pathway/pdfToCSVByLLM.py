"""
Microservice for a generalized finance tracking app.

This version accepts any kind of finance-related file (PDFs, bank statements, screenshots, CSVs, etc.) 
and extracts the financial facts, figures, and any tabular data from it. The LLM is used to extract 
the relevant data from unstructured text, and the results are written to a CSV file with metadata attached.
This CSV can later be uploaded to a Google Drive folder for further analysis (e.g., vectorstore creation).
"""

import os
import json
import datetime
import logging
import json
import re

import tiktoken
import dotenv
import pathway as pw
from pathway.xpacks.llm.llms import prompt_chat_single_qa, LiteLLMChat
from pathway.xpacks.llm.parsers import UnstructuredParser

dotenv.load_dotenv()


@pw.udf
def join_texts(texts: list) -> str:
    """
    Join a list of text fragments into a single string.
    If an element is a tuple, take its first element as the text.
    """
    if isinstance(texts, list):
        str_texts = []
        for t in texts:
            if isinstance(t, tuple):
                # Assume the first element holds the actual text.
                str_texts.append(str(t[0]))
            else:
                str_texts.append(str(t))
        return " ".join(str_texts)
    return str(texts)

@pw.udf
def parse_json(response: str) -> list:
    # Fix improper escape sequences in JSON
    response = response.replace('\\"', '"')  # Fixes improperly escaped quotes
    response = re.sub(r'\\(?!["\\/bfnrtu])', r'\\\\', response)  # Properly escape backslashes

    # Extract the JSON array using regex
    match = re.search(r'(\[.*\])', response, re.DOTALL)
    json_str = match.group(1) if match else response

    # Ensure the extracted JSON is valid
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {e}")
        return []  # Return an empty list on failure


@pw.udf
def current_timestamp(dummy: str = "") -> str:
    """
    Return the current timestamp in ISO format.
    """
    return datetime.datetime.now().isoformat()

def build_extraction_prompt(text: str) -> str:
    """
    Build a prompt instructing the LLM to extract all financial data.
    The document may contain narrative text, facts, figures, and tables.
    The LLM should output a JSON array of objects where each object represents
    an extracted record with key-value pairs. Do not include any commentary.
    """
    prompt = (
        f"Extract all financial data from the following document. The document may contain narrative text, "
        f"facts, figures, and even tables. Please extract the information into a JSON array of objects. "
        f"Each object should represent one record of extracted data with keys corresponding to the identified fields. "
        f"Do not include any extra text or commentary—only output the JSON array. \n\n"
        # f"Document Source: {source}\n\n"
        f"Document Content:\n{text}\n\n"
        f"Output JSON array:"
    )
    return prompt

@pw.udf
def build_prompt_structure(
    texts: list[str],
    max_tokens: int = 8000,
    encoding_name: str = "cl100k_base",
):
    """
    Insert instructions for the LLM here.
    max_tokens for the context. If gpt-3.5-turbo-16k is used, set it to 16k.
    """
    docs_str = " ".join(texts)
    encoding = tiktoken.get_encoding(encoding_name)
    prompt_prefix = "Given the following financial document : \n"
    prompt_suffix = (
        f" \nfill in this schema as deduced\n"
        + """while respecting the instructions:
            - amounts should be in millions of dollars.
            - Parse quarterly data and ignore yearly records if present.
            - Your answer should be parseable by json. i.e. json.loads(response) doesn't throw any errors."""
    )

    prefix_tokens = len(list(encoding.encode_ordinary(prompt_prefix)))
    suffix_tokens = len(list(encoding.encode_ordinary(prompt_suffix)))

    # Calculate available tokens for docs_str
    available_tokens = max_tokens - (prefix_tokens + suffix_tokens)

    # Tokenize docs_str and truncate if needed
    doc_tokens = list(encoding.encode_ordinary(docs_str))
    if len(doc_tokens) > available_tokens:
        logging.warning("Document is too large for one query.")
        docs_str = encoding.decode(doc_tokens[:available_tokens])

    prompt = prompt_prefix + build_extraction_prompt(docs_str) + prompt_suffix
    return prompt


@pw.udf
def strip_metadata(docs: list[tuple[str, dict]]) -> list[str]:
    return [doc[0] for doc in docs]

# @pw.udf
# def convert_chat_output_to_payload_udf(chat_output: pw.Json) -> pw.Json:
#     # Convert the deferred pw.Json to a Python object
#     # Extract contents from each message
#     contents = [msg["content"] for msg in chat_output if msg.value("content", "").strip()]
#     return pw.Json({"prompt": {"contents": contents}})




def run(
    *,
    data_dir: str = os.environ.get("PATHWAY_DATA_DIR", "./INFO/data"),
    output_csv: str = "./data/finance_docs_extracted.csv",
    api_key: str = os.environ.get("GEMINI_API_KEY", ""),
    model_locator: str = "vertex_ai/gemini-1.5-flash",  # can be replaced by a LangChain integration if needed
    max_tokens: int = 1024,
    temperature: float = 0.0,
    **kwargs,
):
    # Read files from the input directory.
    files = pw.io.fs.read(data_dir, format="binary")
    
    # # Use the UnstructuredParser to extract text from each file.
    parser = UnstructuredParser()
    parsed_files = files.select(texts=parser(pw.this.data)).select(
        texts=strip_metadata(pw.this.texts)
    )
    # print(parser(pw.this.data))
    # query += query.select(
    #     q=model(prompt_chat_single_qa(pw.this.prompt)),
    # )
    
    # Join text fragments and preserve the source filename.
    # documents = parsed_files.select(
    #     texts=join_texts(pw.this.texts)
    # )
    # print(documents)
    
    # Build prompts for extraction.
    extraction_prompts = parsed_files.select(
         prompt_string=build_prompt_structure(pw.this.texts)
    )
        # Structure the prompt using prompt_chat_single_qa
    chat_prompts = extraction_prompts.select(
        prompt=prompt_chat_single_qa(pw.this.prompt_string)
    )

    # Call the LLM to perform the extraction.
    model = LiteLLMChat(
         api_key=api_key,
         model=model_locator,
         temperature=temperature,
        #  retry_strategy=pw.udfs.ExponentialBackoffRetryStrategy(),
        #  cache_strategy=pw.udfs.DefaultCache(),
         # Retry and cache strategies can be added as needed.
    )

    responses = chat_prompts.select(
         response=model(pw.this.prompt),
    )

    # Parse the JSON output from the LLM.
    # It is expected that the LLM returns a JSON array of objects.
    responses = responses.select(
         records=parse_json(pw.this.response)
    )

    
    # UDF to add metadata (source and timestamp) to each record in the extracted JSON.
    @pw.udf
    def add_metadata(records: list, source: str) -> list:
        ts = datetime.datetime.now().isoformat()
        new_records = []
        for record in records:
            # Convert the record to a dict if it's a pw.Json (or a string)
            if isinstance(record, dict):
                rec = record
            else:
                rec = json.loads(str(record))
            rec["source"] = source
            rec["upload_time"] = ts
            new_records.append(rec)
        return new_records

    
    enriched = responses.select(
         records_with_meta=add_metadata(pw.this.records, os.path.basename(data_dir) + ".pdf")  # Assuming the source is the filename)
    )
    
    @pw.udf
    def flatten(records_with_meta: list) -> list:
        flat = []
        for rec in records_with_meta:
            if isinstance(rec, list):
                flat.extend(rec)
            elif isinstance(rec, tuple):
                # If tuple is of form ('', dict), extract the dict.
                if len(rec) == 2 and rec[0] == "" and isinstance(rec[1], dict):
                    flat.append(rec[1])
                else:
                    # Otherwise, convert the tuple to a dict using indices as keys.
                    flat.append({str(i): v for i, v in enumerate(rec)})
            else:
                flat.append(rec)
        return flat
    
    final_table = enriched.select(
        flat_records=flatten(pw.this.records_with_meta)
    )


    # Later, when converting each flattened record into separate columns,
    # ensure that you handle cases where the record might not be a dictionary.
    final_table = final_table.select(
        source=pw.apply(lambda rec: rec.get("source", "") if isinstance(rec, dict) else "", pw.this.flat_records),
        upload_time=pw.apply(lambda rec: rec.get("upload_time", "") if isinstance(rec, dict) else "", pw.this.flat_records),
        data=pw.apply(lambda rec: json.dumps(rec) if isinstance(rec, dict) else json.dumps({}), pw.this.flat_records)
)

    # Write the enriched and flattened table to a CSV file.
    pw.io.csv.write(final_table, output_csv)
    
    pw.run(monitoring_level=pw.MonitoringLevel.NONE)


if __name__ == "__main__":
    run()
