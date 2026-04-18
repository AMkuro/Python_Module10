from functools import wraps
from time import perf_counter, sleep
from typing import Any, Callable


def spell_timer(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        print(f"Casting {func.__name__}...")
        start: float = perf_counter()
        result = func(*args, **kwargs)
        end: float = perf_counter()
        print(f"Spell completed in {end - start:.3f} seconds")
        return result

    return wrapper


def power_validator(min_power: int) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            power: int
            if "power" in kwargs:
                power = kwargs["power"]
            else:
                power = args[2]
            if power >= min_power:
                return func(*args, **kwargs)
            return "Insufficient power for this spell"

        return wrapper

    return decorator


def retry_spell(max_attempts: int) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            attempt: int
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if attempt < max_attempts:
                        print(
                            "Spell failed, retrying... "
                            f"(attempt {attempt}/{max_attempts})"
                        )
            return f"Spell casting failed after {max_attempts} attempts"

        return wrapper

    return decorator


class MageGuild:
    @staticmethod
    def validate_mage_name(name: str) -> bool:
        return len(name) >= 3 and all(
            ch.isalpha() or ch.isspace() for ch in name
        )

    @power_validator(10)
    def cast_spell(self, spell_name: str, power: int) -> str:
        return f"Successfully cast {spell_name} with {power} power"


def format_spell_timer(func: Callable) -> str:
    fireball = spell_timer(func)
    return f"Result: {fireball()}"


def format_retry_spell(func: Callable, max_attempts: int) -> str:
    retried_spell = retry_spell(max_attempts)(func)
    return f"Retry result: {retried_spell()}"


def format_validate_mage_name(names: list[str]) -> str:
    return "\n".join(str(MageGuild.validate_mage_name(name)) for name in names)


def format_cast_spell(spell_name: str, powers: list[int]) -> str:
    guild = MageGuild()
    return "\n".join(guild.cast_spell(spell_name, power) for power in powers)


def format_mage_guild(
    names: list[str], spell_name: str, powers: list[int]
) -> str:
    return "\n".join(
        [
            format_validate_mage_name(names),
            format_cast_spell(spell_name, powers),
        ]
    )


def test_function(func: Callable, *args: Any) -> str:
    formatters: dict[str, Callable[..., str]] = {
        "spell_timer": format_spell_timer,
        "retry_spell": format_retry_spell,
        "validate_mage_name": format_validate_mage_name,
        "cast_spell": format_cast_spell,
        "MageGuild": format_mage_guild,
    }
    print(f"\nTesting {func.__name__.replace('_', ' ')}...")
    return formatters[func.__name__](*args)


def main() -> None:
    def fireball() -> str:
        sleep(0.1)
        return "Fireball cast!"

    def muggle_spelled() -> None:
        raise RuntimeError("Spell fizzled")

    print(test_function(spell_timer, fireball))
    print(test_function(retry_spell, muggle_spelled, 3))
    print(
        test_function(
            MageGuild,
            ["Merlin", "Al3x"],
            "Lightning",
            [15, 5],
        )
    )


if __name__ == "__main__":
    main()
