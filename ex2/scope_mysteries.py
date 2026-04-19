from typing import Any, Callable


def mage_counter() -> Callable:
    count: int = 0

    def counter() -> int:
        nonlocal count
        count += 1
        return count

    return counter


def spell_accumulator(initial_power: int) -> Callable:
    total_power: int = initial_power

    def add_power(amount: int) -> int:
        nonlocal total_power
        if not isinstance(amount, int):
            raise TypeError(f"amount must be int, got {type(amount).__name__}")
        total_power += amount
        return total_power

    return add_power


def enchantment_factory(enchantment_type: str) -> Callable:
    def apply_enchantment(item_name: str) -> str:
        return f"{enchantment_type} {item_name}"

    return apply_enchantment


def memory_vault() -> dict[str, Callable]:
    memory_dict: dict[Any, Any] = {}

    def store(key: Any, value: Any) -> None:
        memory_dict[key] = value

    def recall(key: Any) -> Any:
        return memory_dict.get(key, "Memory not found")

    return {"store": store, "recall": recall}


def format_mage_counter(call_count: int) -> str:
    counter = mage_counter()
    return "\n".join(
        f"Call {index}: {counter()}" for index in range(1, call_count + 1)
    )


def format_spell_accumulator(initial_power: int, amounts: list[int]) -> str:
    accumulator = spell_accumulator(initial_power)
    lines = [f"Start: {initial_power}"]
    for amount in amounts:
        try:
            lines.append(f"After adding {amount}: {accumulator(amount)}")
        except TypeError as e:
            lines.append(f"Error: {e}")
    return "\n".join(lines)


def format_enchantment_factory(enchantment_type: str, items: list[str]) -> str:
    enchant = enchantment_factory(enchantment_type)
    return "\n".join(enchant(item) for item in items)


def format_memory_vault(
    stored_values: list[tuple[Any, Any]], recall_keys: list[Any]
) -> str:
    vault = memory_vault()
    store = vault["store"]
    recall = vault["recall"]

    lines: list[str] = []
    for key, value in stored_values:
        store(key, value)
        lines.append(f"Stored: {key} -> {value}")
    for key in recall_keys:
        lines.append(f"Recall {key}: {recall(key)}")
    return "\n".join(lines)


def test_function(func: Callable, *args: Any) -> str:
    formatters: dict[str, Callable[..., str]] = {
        "mage_counter": format_mage_counter,
        "spell_accumulator": format_spell_accumulator,
        "enchantment_factory": format_enchantment_factory,
        "memory_vault": format_memory_vault,
    }
    return "\n".join(
        [
            f"\nTesting {func.__name__.replace('_', ' ')}...",
            formatters[func.__name__](*args),
        ]
    )


def main() -> None:
    print(test_function(mage_counter, 3))
    print(test_function(spell_accumulator, 10, [5, 20]))
    print(test_function(enchantment_factory, "Flaming", ["Sword", "Shield"]))
    print(
        test_function(
            memory_vault,
            [("potion", 3), ("scroll", 7)],
            ["potion", "missing"],
        )
    )


if __name__ == "__main__":
    main()
