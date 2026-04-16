from functools import reduce, partial, lru_cache, singledispatch
import operator
from typing import Any, Callable


def spell_reducer(spells: list[int], operation: str) -> int:
    initial: int = 1 if operation == "multiply" else 0
    operations: dict[str, Callable[[int, int], int]] = {
        "add": operator.add,
        "multiply": operator.mul,
        "max": max,
        "min": min,
    }
    if operation == "max" or operation == "min":
        if not spells:
            raise ValueError(f"spells must not be empty for {operation}")
    try:
        func = operations[operation]
    except KeyError:
        raise ValueError(f"Unsupported operation: {operation}")
    return reduce(func, spells, initial)


def partial_enchanter(base_enchantment: Callable) -> dict[str, Callable]:
    power: int = 50
    elements: tuple[str, ...] = ("fire", "ice", "lightning")
    return {
        f"{element}_enchant": partial(base_enchantment, power, element)
        for element in elements
    }


@lru_cache(maxsize=None)
def memoized_fibonacci(n: int) -> int:
    if n < 2:
        return n
    return memoized_fibonacci(n - 1) + memoized_fibonacci(n - 2)


def spell_dispatcher() -> Callable:
    @singledispatch
    def dispatch(data: object) -> str:
        return f"Unknown spell type: {data!r}"

    @dispatch.register
    def _(data: int) -> str:
        return f"Damage spell with power {data}"

    @dispatch.register
    def _(data: str) -> str:
        return f"Enchantment spell: {data}"

    @dispatch.register
    def _(data: list) -> str:
        return f"Multi-cast spell: {len(data)} items"

    return dispatch


def format_spell_reducer(spells: list[int]) -> str:
    labels: dict[str, str] = {
        "add": "Sum",
        "multiply": "Product",
        "max": "Max",
        "min": "Min",
    }
    operations = ["add", "multiply", "max", "min"]
    return "\n".join(
        f"{labels[operation]}: {spell_reducer(spells, operation)}"
        for operation in operations
    )


def format_partial_enchanter(base_enchantment: Callable) -> str:
    enchanted_spells = partial_enchanter(base_enchantment)
    lines = [
        f"{name}: {spell('Sword')}" for name, spell in enchanted_spells.items()
    ]
    return "\n".join(lines)


def format_memoized_fibonacci(values: list[int]) -> str:
    return "\n".join(
        f"Fib({value}): {memoized_fibonacci(value)}" for value in values
    )


def format_spell_dispatcher(values: list[object]) -> str:
    dispatch = spell_dispatcher()
    return "\n".join(dispatch(value) for value in values)


def test_function(func: Callable, *args: Any) -> str:
    formatters: dict[str, Callable[..., str]] = {
        "spell_reducer": format_spell_reducer,
        "partial_enchanter": format_partial_enchanter,
        "memoized_fibonacci": format_memoized_fibonacci,
        "spell_dispatcher": format_spell_dispatcher,
    }
    return "\n".join(
        [
            f"\nTesting {func.__name__.replace('_', ' ')}...",
            formatters[func.__name__](*args),
        ]
    )


def main() -> None:
    def base_enchantment(power: int, element: str, target: str) -> str:
        return f"{element.title()} enchant {target} with {power}"

    print(test_function(spell_reducer, [10, 20, 30, 40]))
    print(test_function(partial_enchanter, base_enchantment))
    print(test_function(memoized_fibonacci, [10, 15]))
    print(
        test_function(
            spell_dispatcher,
            [42, "Flame", ["a", "b"], {"x": 1}],
        )
    )


if __name__ == "__main__":
    main()
