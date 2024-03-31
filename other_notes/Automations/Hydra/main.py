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
import hydra

config: DictConfig = OmegaConf.load("./config.yaml")


@hydra.main(config_path=None, version_base=None)
def main(config: DictConfig) -> None:
    """Main function"""
    console.print(OmegaConf.to_yaml(config))


if __name__ == "__main__":
    # main(config=config)
    main()
