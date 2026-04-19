from typing import Any, Callable


def spell_combiner(spell1: Callable, spell2: Callable) -> Callable:
    if not callable(spell1) or not callable(spell2):
        raise TypeError("spell1 and spell2 must be callable")

    def combined(*args, **kwargs):
        result1 = spell1(*args, **kwargs)
        result2 = spell2(*args, **kwargs)
        return (result1, result2)

    return combined


def power_amplifier(base_spell: Callable, multiplier: int) -> Callable:
    def amplified(*args, **kwargs):
        return base_spell(*args, **kwargs) * multiplier

    return amplified


def conditional_caster(condition: Callable, spell: Callable) -> Callable:
    if not callable(condition) or not callable(spell):
        raise TypeError("condition and spell must be callable")

    def caster(*args, **kwargs):
        if condition(*args, **kwargs):
            return spell(*args, **kwargs)
        return "Spell fizzled"

    return caster


def spell_sequence(spells: list[Callable]) -> Callable:
    def sequence(*args, **kwargs):
        results = []
        for spell in spells:
            results.append(spell(*args, **kwargs))
        return results

    return sequence


def format_spell_combiner(
    spell1: Callable, spell2: Callable, target: str
) -> str:
    try:
        combined = spell_combiner(spell1, spell2)
        combined_result = combined(target)
        return f"Combined spell result: {', '.join(combined_result)}"
    except TypeError as e:
        return f"Error: {e}"


def format_power_ampliifier(original_power: int, multiplier: int) -> str:
    mega_fireball = power_amplifier(lambda power: power, multiplier)
    amplified_power = mega_fireball(original_power)
    return f"Original: {original_power}, Amplified: {amplified_power}"


def format_conditional_caster(condition: Callable, spell: Callable) -> str:
    try:
        casting_magic = conditional_caster(condition, spell)
        return "\n".join(
            [
                f"Condition met: {casting_magic(6)}",
                f"Condition failed: {casting_magic(3)}",
            ]
        )
    except TypeError as e:
        return f"Error: {e}"


def format_spell_sequence(spells: list, target: str) -> str:
    combo = spell_sequence(spells)
    sequence_result = combo(target)
    return f"Sequence result: {' -> '.join(sequence_result)}"


def test_function(func: Callable, *args: Any) -> str:
    formatters: dict[str, Callable[..., str]] = {
        "spell_combiner": format_spell_combiner,
        "power_amplifier": format_power_ampliifier,
        "conditional_caster": format_conditional_caster,
        "spell_sequence": format_spell_sequence,
    }
    lines: list[str] = [
        f"\nTesting {func.__name__.replace('_', ' ')}...",
        formatters[func.__name__](*args),
    ]
    return "\n".join(lines)


def main() -> None:
    def fireball(target: str) -> str:
        return f"Fireball hits {target}"

    def heal(target: str) -> str:
        return f"Heals {target}"

    def shield(target: str) -> str:
        return f"Shields {target}"

    def has_mana(mana: int) -> bool:
        return mana >= 5

    def cast_bolt(mana: int) -> str:
        return f"Lightning cast with mana {mana}"

    print(test_function(spell_combiner, fireball, heal, "Dragon"))

    print(test_function(power_amplifier, 10, 3))

    print(test_function(conditional_caster, has_mana, cast_bolt))

    print(test_function(spell_sequence, [fireball, heal, shield], "Dragon"))


if __name__ == "__main__":
    main()
