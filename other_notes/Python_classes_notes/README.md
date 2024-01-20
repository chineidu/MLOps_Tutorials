# Python Classes

## Table of Content

- [Python Classes](#python-classes)
  - [Table of Content](#table-of-content)
  - [Class Methods](#class-methods)

## Class Methods

```python
from typing import TypeVar, Type
from sqlalchemy import select, delete


from rich.console import Console
from typeguard import typechecked


console = Console()

P = TypeVar("P", bound="Product")


class Product:
    base_price: float = 100.0  # class attribute

    @typechecked
    def __init__(self, name: str, discount: float = 0) -> None:
        self.name = name
        if 0 <= discount <= 1:
            self.discount = discount
        else:
            raise ValueError("discount must be between 0 and 1")

    @typechecked
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name}, discount={self.discount})"

    @typechecked
    @classmethod
    def from_string(cls: Type[P], product_str) -> P:
        """Create the product from a string.
        It uses the format: "name, discount"
        """
        name, discount = product_str.split(",")
        return cls(name, float(discount))

    @typechecked
    @classmethod
    def set_base_price(cls: Type[P], new_price: float) -> None:
        """Change the base price for all the products."""
        cls.base_price = new_price

    @typechecked
    def calculate_price(self) -> float:
        """Calculate the final price using the discount."""
        final_price: float = self.base_price * (1 - self.discount)
        return final_price


Product.set_base_price(120.0)
p1 = Product(name="Airbuds", discount=0.05)
p2 = Product.from_string(product_str="Google Chromecast, 0.035")
console.print(p1, style="green")  # Product(name=Airbuds, discount=0.05)
console.print(p2, style="blue")  # Product(name=Google Chromecast, discount=0.035)

price_1 = p1.calculate_price()
price_2 = p2.calculate_price()

console.print(price_1, style="green")  # 114.0
console.print(price_2, style="blue")  # 115.8
```
