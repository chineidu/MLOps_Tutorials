import os

import hydra
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


@hydra.main(config_path=".", config_name="server", version_base=None)
def main(config: DictConfig) -> None:
    """Main function"""
    # Add env variables
    os.environ["ENV_NAME"] = "neidu"
    # os.environ["ENV_PASSWORD"]

    console.print(OmegaConf.to_yaml(config, resolve=True))


if __name__ == "__main__":
    config: DictConfig = OmegaConf.load("server.yaml")
    # main(config=config)
    main()
