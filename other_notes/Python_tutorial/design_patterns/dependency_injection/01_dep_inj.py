import json  # noqa: N999
from typing import Any, Protocol

type Data = list[dict[str, Any]]


# ========== Interfaces ==========
class DataLoader(Protocol):
    def load(self) -> Data:
        """Load the data

        Returns
        -------
        Data
            The loaded data
        """
        ...


class Transformer(Protocol):
    def transform(self, data: Data) -> Data:
        """Transform the data

        Parameters
        ----------
        data : Data
            The data to be transformed

        Returns
        -------
        Data
            The transformed data
        """
        ...


class Exporter(Protocol):
    def export(self, data: Data) -> None:
        """Save the data

        Parameters
        ----------
        data : Data
            The data to be exported
        """
        ...


# ========== Implementations ==========
class InMemoryDataLoader:
    def load(self) -> Data:
        """Load the data

        Returns
        -------
        Data
            The loaded data
        """
        return [
            {"name": "Alice", "age": 30},
            {"name": "Bob", "age": 25},
            {"name": "Neidu", "age": 35},
            {"name": "Diana", "age": 28},
        ]


class CleanMissingFieldsTransformer:
    def transform(self, data: Data) -> Data:
        """Transform the data

        Parameters
        ----------
        data : Data
            The data to be transformed

        Returns
        -------
        Data
            The transformed data
        """
        return [record for record in data if record["age"] is not None]


class RemoveNeiduTransformer:
    def transform(self, data: Data) -> Data:
        """Transform the data by removing records with name 'Neidu'

        Parameters
        ----------
        data : Data
            The data to be transformed

        Returns
        -------
        Data
            The transformed data
        """
        return [record for record in data if record["name"] != "Neidu"]


class JSONExporter:
    def __init__(self, filename: str) -> None:
        self.filename = filename

    def export(self, data: Data) -> None:
        """Save the data

        Parameters
        ----------
        data : Data
            The data to be exported
        """
        with open(self.filename, "w") as f:
            json.dump(data, f, indent=2)


# ========== Pipeline ==========
class DataPipeline:
    def __init__(
        self,
        loader: DataLoader,
        transformer: Transformer,
        exporter: Exporter,
    ) -> None:
        self.loader = loader
        self.transformer = transformer
        self.exporter = exporter

    def run(self) -> None:
        """Run the pipeline"""
        print("Running data pipeline...")
        data = self.loader.load()
        data = self.transformer.transform(data)
        self.exporter.export(data)
        print("Data pipeline finished.")


# ========== Add Dependency Injections ==========
def main() -> None:
    """Main function"""
    loader = InMemoryDataLoader()
    transformer = RemoveNeiduTransformer()
    exporter = JSONExporter("output.json")

    # Create and run the pipeline
    pipeline = DataPipeline(loader, transformer, exporter)
    pipeline.run()


if __name__ == "__main__":
    main()
