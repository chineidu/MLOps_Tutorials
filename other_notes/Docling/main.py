import json
import logging
import os
import time
from enum import StrEnum
from pathlib import Path

import easyocr
import pandas as pd
from docling.datamodel.accelerator_options import AcceleratorDevice, AcceleratorOptions
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import (
    EasyOcrOptions,
    PdfPipelineOptions,
    TableStructureOptions,
)
from docling.document_converter import DocumentConverter, PdfFormatOption

_log = logging.getLogger(__name__)


class ExportFormat(StrEnum):
    ALL = "all"
    DOCUMENT_TAGS = "document_tags"
    JSON = "json"
    MARKDOWN = "markdown"
    TABLE = "table"
    TEXT = "text"


def _download_easyocr_models() -> None:
    """Run this function once to download EasyOCR models for offline use.

    Use a VPN if GitHub release assets are blocked in your region. This will
    cache the models locally for future use.
    """
    _log.info("Downloading EasyOCR models for offline use...")
    _ = easyocr.Reader(["en"], gpu=False)


def _setup_environment() -> None:
    """Set environment variables for offline mode, timeouts, and parallel processing."""

    _log.info("Setting up environment variables...")
    # Force offline mode to use cached models and avoid network delays
    # Set to "0" if you need to download models for the first time
    os.environ["HF_HUB_OFFLINE"] = "1"

    # Set a reasonable timeout for any remaining network operations (in seconds)
    os.environ["HF_HUB_DOWNLOAD_TIMEOUT"] = "30"

    # Number of threads for parallel processing (adjust based on your system's capabilities)
    os.environ["OMP_NUM_THREADS"] = "4"

    # Set Tesseract data directory path for tesserocr OCR engine
    # On macOS with Homebrew, this is typically /opt/homebrew/opt/tesseract/share/tessdata
    os.environ["TESSDATA_PREFIX"] = "/opt/homebrew/opt/tesseract/share/tessdata"


start_time: float = time.time()
artifacts_path: str = "/Users/mac/.cache/docling/models"
# source: str = "./data/Customer Statement_repaired.pdf"
MAX_NUM_PAGES: int = 20
MAX_FILE_SIZE_MB: int = 1_024 * 1_024  # 1 MB == 1024^2 KB

print("Initializing converter (using cached models)...")


def main(export_format: ExportFormat = ExportFormat.ALL) -> None:
    """Main function to convert a PDF document using Docling and export results."""
    logging.basicConfig(level=logging.INFO)

    # Run this once to download models
    _download_easyocr_models()
    _setup_environment()

    source: str = "./data/ML_role.pdf"
    output_dir = Path("scratch")

    pipeline_options = PdfPipelineOptions()
    # --- If you want to enable OCR ---
    pipeline_options.do_ocr = True
    # --- OCR options: RapidOcrOptions|EasyOcrOptions|TesseractOcrOptions|OcrMacOptions ---
    pipeline_options.ocr_options = EasyOcrOptions()
    # Configuration for table structure extraction using the TableFormer mode
    # --- Disable GPU ---
    # pipeline_options.ocr_options.use_gpu = False
    pipeline_options.table_structure_options = TableStructureOptions(do_cell_matching=True)
    pipeline_options.accelerator_options = AcceleratorOptions(num_threads=4, device=AcceleratorDevice.AUTO)

    doc_converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options),
        }
    )

    start_time: float = time.time()

    conv_result = doc_converter.convert(
        source, max_num_pages=MAX_NUM_PAGES, max_file_size=10 * MAX_FILE_SIZE_MB, raises_on_error=False
    )

    output_dir.mkdir(parents=True, exist_ok=True)
    doc_filename: str = conv_result.input.file.stem

    _log.info(f"Converting results to the format: '{export_format.value}'")
    if export_format in [ExportFormat.ALL, ExportFormat.TABLE]:
        for table_ix, table in enumerate(conv_result.document.tables):
            table_df: pd.DataFrame = table.export_to_dataframe(doc=conv_result.document)
            print(f"## Table {table_ix}")
            print(table_df.head(3).to_markdown())

            # Save the table as CSV
            element_csv_filename = output_dir / f"{doc_filename}-table-{table_ix + 1}.csv"
            _log.info(f"Saving CSV table to {element_csv_filename}")
            table_df.to_csv(element_csv_filename)

    if export_format in [ExportFormat.ALL, ExportFormat.JSON]:
        # Export Docling document JSON format:
        with (output_dir / f"{doc_filename}.json").open("w", encoding="utf-8") as fp:
            fp.write(json.dumps(conv_result.document.export_to_dict()))
    if export_format in [ExportFormat.ALL, ExportFormat.TEXT]:
        # Export Text format (plain text via Markdown export):
        with (output_dir / f"{doc_filename}.txt").open("w", encoding="utf-8") as fp:
            fp.write(conv_result.document.export_to_markdown(strict_text=True))
    if export_format in [ExportFormat.ALL, ExportFormat.MARKDOWN]:
        # Export Markdown format:
        with (output_dir / f"{doc_filename}.md").open("w", encoding="utf-8") as fp:
            fp.write(conv_result.document.export_to_markdown())

    if export_format in [ExportFormat.ALL, ExportFormat.DOCUMENT_TAGS]:
        # Export Document Tags format:
        with (output_dir / f"{doc_filename}.doctags").open("w", encoding="utf-8") as fp:
            fp.write(conv_result.document.export_to_doctags())

    end_time = time.time() - start_time

    _log.info(f"Document converted and tables exported in {end_time:.2f} seconds.")


if __name__ == "__main__":
    main(export_format=ExportFormat.ALL)
