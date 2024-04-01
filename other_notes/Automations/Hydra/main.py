import hydra
from hydra.utils import instantiate
from omegaconf import DictConfig
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


class Training:
    def __init__(self, batch_size: int, epochs: int, learning_rate: float) -> None:
        self.batch_size = batch_size
        self.epochs = epochs
        self.learning_rate = learning_rate

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(batch_size={self.batch_size}, "
            f"epochs={self.epochs}, learning_rate={self.learning_rate})"
        )


@hydra.main(config_path=".", config_name="config", version_base=None)
def main(config: DictConfig) -> None:
    """Main function"""
    training_hydra: DictConfig = instantiate(config.training)
    # console.print(OmegaConf.to_yaml(config, resolve=True))
    console.print(training_hydra)


if __name__ == "__main__":
    main()
