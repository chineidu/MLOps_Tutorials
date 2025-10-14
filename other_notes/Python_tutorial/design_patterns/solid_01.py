# Single Responsibility Principle
# A class/function should have only one reason to change, meaning it should only have one job or responsibility.

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable

# =============================================
# =========== 1.) Using Functions =============
# =============================================
# Define types
type GreetingsFn = Callable[[str], None]


# Config
@dataclass
class GreetingFnConfig:
    greetings_fns: list[GreetingsFn]


def morning_greeting(name: str) -> None:
    """Morning greeting function."""
    print(f"Good morning {name}!")


def afternoon_greeting(name: str) -> None:
    """Afternoon greeting function."""
    print(f"Hello {name}! How are you doing this afternoon?")


def evening_greeting(name: str) -> None:
    """Evening greeting function."""
    print(f"Good evening {name}! Trust you're having a great day.")


def night_greeting(name: str) -> None:
    """Night greeting function."""
    print(f"Time to recharge! Good night {name}!")


def run_greetings_function_approach(name: str, config: GreetingFnConfig) -> None:
    """Execute all configured greeting functions."""
    for fn in config.greetings_fns:
        fn(name)


def main_function_approach() -> None:
    """Run the greeting demonstration."""
    config = GreetingFnConfig(
        greetings_fns=[
            morning_greeting,
            afternoon_greeting,
            evening_greeting,
            night_greeting,
        ]
    )

    run_greetings_function_approach(name="David", config=config)


# =============================================
# ============ 2.) Using Classes ==============
# =============================================
class GreetingStrategy(ABC):
    """Abstract base class for greeting strategies."""

    @abstractmethod
    def greet(self, name: str) -> None:
        """Execute the greeting.

        Parameters
        ----------
        name : str
            Name of the person to greet.
        """
        pass


class MorningGreeting(GreetingStrategy):
    """Strategy for morning greetings."""

    def greet(self, name: str) -> None:
        """Execute the morning greeting."""
        print(f"Good morning {name}!")


class AfternoonGreeting(GreetingStrategy):
    """Strategy for afternoon greetings."""

    def greet(self, name: str) -> None:
        """Execute the afternoon greeting."""
        print(f"Hello {name}! How are you doing this afternoon?")


class EveningGreeting(GreetingStrategy):
    """Strategy for evening greetings."""

    def greet(self, name: str) -> None:
        """Execute the evening greeting."""
        print(f"Good evening {name}! Trust you're having a great day.")


class NightGreeting(GreetingStrategy):
    """Strategy for night greetings."""

    def greet(self, name: str) -> None:
        """Execute the night greeting."""
        print(f"Time to recharge! Good night {name}!")


@dataclass
class GreetingConfig:
    """Configuration for greeting strategies.

    Attributes
    ----------
    strategies : list[GreetingStrategy]
        List of greeting strategies to execute.
    """

    strategies: list[GreetingStrategy]


def run_greetings_class_approach(name: str, config: GreetingConfig) -> None:
    """Execute all configured greeting strategies.

    Parameters
    ----------
    name : str
        Name of the person to greet.
    config : GreetingConfig
        Configuration containing greeting strategies.
    """
    for strategy in config.strategies:
        strategy.greet(name)


def main_class_approach() -> None:
    """Run the greeting demonstration."""
    config = GreetingConfig(
        strategies=[
            MorningGreeting(),
            AfternoonGreeting(),
            EveningGreeting(),
            NightGreeting(),
        ]
    )

    run_greetings_class_approach(name="David", config=config)


if __name__ == "__main__":
    main_function_approach()
    print("\n" + "=" * 50 + "\n")
    main_class_approach()
    print("\n" + "=" * 50 + "\n")
