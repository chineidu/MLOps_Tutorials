class Config:
    _instance = None

    def __init__(self) -> None:
        self.db_url = "sqlite:///:memory:"
        self.debug = True

    def __new__(cls) -> "Config":
        """Ensure only one instance of Config is created."""
        if cls._instance is None:
            print("Creating new instance")
            cls._instance = super().__new__(cls)
        return cls._instance


def main() -> None:
    """Demonstrate the singleton behavior of Config class."""
    # Create the first instance
    s1 = Config()
    # Attempt to create a second instance but should return the first one.
    # This references the first instance and only works in single-threaded scenarios.
    s2 = Config()

    print(s1 is s2)
    print(id(s1))
    print(id(s2))


if __name__ == "__main__":
    main()
