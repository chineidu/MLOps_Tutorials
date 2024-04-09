import hydra
import polars as pl
from config_schema import MNISTConfig
from hydra.core.config_store import ConfigStore
from omegaconf import DictConfig, OmegaConf
from rich.console import Console
from rich.theme import Theme

custom_theme = Theme(
    {
        "info": "#76FF7B",
        "warning": "#FBDDFE",
        "error": "#FF0000",
    }
)
console = Console(theme=custom_theme)

# Setup the config store
cs = ConfigStore.instance()
cs.store(name="mnist_schema", node=MNISTConfig)


@hydra.main(config_path="./conf", config_name="config", version_base=None)
def main(config: DictConfig) -> None:
    """Main function"""
    console.print(OmegaConf.to_yaml(config, resolve=True))
    data_fp: str = config.paths.data
    fp: str = config.files.train_data
    console.print(pl.read_parquet(data_fp + fp))


if __name__ == "__main__":
    main()
