from pathlib import Path

from setuptools import find_namespace_packages, setup

# Load packages from requirements.txt
BASE_DIR = Path(__file__).parent
with open(Path(BASE_DIR, "requirements.txt")) as file:
    required_packages = [ln.strip() for ln in file.readlines()]

dev_packages = ["pre-commit==3.3.2"]

style_packages = ["black==22.3.0", "isort==5.10.1", "mypy==1.2.0", "pylint==2.15.10"]

test_packages = ["pytest==7.1.2", "pytest-cov==2.10.1"]
NAME = "custom_app"

setup(
    name=NAME,
    version=0.1,
    description="MLOps Tutorial Using Python",
    author="Chinedu Ezeofor",
    author_email="neidu@email.com",
    url="https://github.com/chineidu/MLOps_Tutorials",
    python_requires=">=3.9",
    packages=find_namespace_packages(),
    install_requires=[required_packages],
    extras_require={
        "dev": dev_packages + style_packages + test_packages,
        "test": test_packages,
    },
)
