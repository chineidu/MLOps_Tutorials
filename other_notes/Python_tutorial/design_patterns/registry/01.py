from typing import Any, Callable, Literal

type Data = dict[str, Any]
type ExporterFn = Callable[[Data], None]
type ExportFormat = Literal["pdf", "json", "csv", "xml"]

def export_pdf(data: Data) -> None:
    """Export to PDF"""
    print(f"Exporting data to PDF: {data}")


def export_csv(data: Data) -> None:
    """Export to CSV"""
    print(f"Exporting data to CSV: {data}")


def export_json(data: Data) -> None:
    """Export to JSON"""
    print(f"Exporting data to JSON: {data}")


def export_xml(data: Data) -> None:
    """Export to XML"""
    print(f"Exporting data to XML: {data}")


# Without using any pattern
def export_data_without_pattern(data: Data, type: ExportFormat) -> None:
    """Export data based on type."""
    if not isinstance(data, dict):
        raise TypeError("data must be of type Data")

    if type == "pdf":
        export_pdf(data)
    elif type == "json":
        export_json(data)
    elif type == "csv":
        export_csv(data)
    elif type == "xml":
        export_xml(data)
    else:
        raise ValueError(f"Unknown export type: {type}")


# Using Registry Pattern
# Method 1: Using a dictionary as a registry
EXPORTERS: dict[Literal["pdf", "json", "csv", "xml"], ExporterFn] = {
    "pdf": export_pdf,
    "json": export_json,
    "csv": export_csv,
    "xml": export_xml,
}


def export_data_with_pattern_1(data: Data, type: ExportFormat) -> None:
    """Export data based on type using registry pattern."""
    if not isinstance(data, dict):
        raise TypeError("data must be of type Data")

    exporter = EXPORTERS.get(type)
    if exporter:
        exporter(data)
    else:
        raise ValueError(f"Unknown export type: {type}")


# Method 2: Using case-switch (Python 3.10+)
def export_data_with_pattern_2(data: Data, type: ExportFormat) -> None:
    """Export data based on type using match-case (Python 3.10+)."""
    if not isinstance(data, dict):
        raise TypeError("data must be of type Data")

    match type:
        case "pdf":
            export_pdf(data)
        case "json":
            export_json(data)
        case "csv":
            export_csv(data)
        case "xml":
            export_xml(data)
        case _:
            raise ValueError(f"Unknown export type: {type}")


if __name__ == "__main__":
    sample_data: Data = {"name": "Alice", "age": 30, "city": "New York"}

    print("=== Exporting without pattern ===")
    export_data_without_pattern(sample_data, "pdf")
    export_data_without_pattern(sample_data, "json")
    export_data_without_pattern(sample_data, "csv")
    export_data_without_pattern(sample_data, "xml")
    
    print()
    print("=== Exporting with registry pattern 1 ===")
    export_data_with_pattern_1(sample_data, "pdf")
    export_data_with_pattern_1(sample_data, "json")
    export_data_with_pattern_1(sample_data, "csv")
    export_data_with_pattern_1(sample_data, "xml")

    print()
    print("=== Exporting with registry pattern 2 ===")
    export_data_with_pattern_2(sample_data, "pdf")
    export_data_with_pattern_2(sample_data, "json")
    export_data_with_pattern_2(sample_data, "csv")
    export_data_with_pattern_2(sample_data, "xml")
