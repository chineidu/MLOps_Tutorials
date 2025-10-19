from typing import Any, Callable, Literal
from functools import wraps

type Data = dict[str, Any]
type ExporterFn = Callable[[Data], None]
type ExportFormat = Literal["pdf", "json", "csv", "xml"]

# Method 3: Using decorators to register exporters
EXPORTER_REGISTRY: dict[ExportFormat, ExporterFn] = {}

def register_exporter(format: ExportFormat) -> Callable[[ExporterFn], ExporterFn]:
    """Decorator to register an exporter function for a given format."""

    def decorator(fn: ExporterFn) -> ExporterFn:
        @wraps(fn)
        def wrapper(data: Data) -> None:
            return fn(data)

        EXPORTER_REGISTRY[format] = wrapper
        return wrapper
    
    return decorator

@register_exporter("pdf")
def export_pdf(data: Data) -> None:
    """Export to PDF"""
    print(f"Exporting data to PDF: {data}")
@register_exporter("csv")
def export_csv(data: Data) -> None:
    """Export to CSV"""
    print(f"Exporting data to CSV: {data}")
@register_exporter("json")
def export_json(data: Data) -> None:
    """Export to JSON"""
    print(f"Exporting data to JSON: {data}")
@register_exporter("xml")
def export_xml(data: Data) -> None:
    """Export to XML"""
    print(f"Exporting data to XML: {data}")

def export_data_with_pattern_3(data: Data, type: ExportFormat) -> None:
    """Export data based on type using registry pattern."""
    if not isinstance(data, dict):
        raise TypeError("data must be of type Data")

    exporter = EXPORTER_REGISTRY.get(type)
    if exporter:
        exporter(data)
    else:
        raise ValueError(f"Unknown export type: {type}")
    
if __name__ == "__main__":
    sample_data: Data = {"name": "Alice", "age": 30, "city": "New York"}

    print("=== Exporting with registry pattern 3 ===")
    export_data_with_pattern_3(sample_data, "pdf")
    export_data_with_pattern_3(sample_data, "json")
    export_data_with_pattern_3(sample_data, "csv")
    export_data_with_pattern_3(sample_data, "xml")