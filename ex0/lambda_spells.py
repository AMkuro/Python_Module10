from typing import Any, Callable


def artifact_sorter(artifacts: list[dict]) -> list[dict]:
    return sorted(artifacts, key=lambda x: -x["power"])


def power_filter(mages: list[dict], min_power: int) -> list[dict]:
    return list(filter(lambda x: x["power"] >= min_power, mages))


def spell_transformer(spells: list[str]) -> list[str]:
    return list(map(lambda x: f"* {x} *", spells))


def mage_stats(mages: list[dict]) -> dict:
    return {
        "max_power": max(mages, key=lambda x: x["power"])["power"],
        "min_power": min(mages, key=lambda x: x["power"])["power"],
        "avg_power": round(
            sum(map(lambda mage: mage["power"], mages)) / len(mages), 2
        ),
    }


def test_function(func: Callable, *args: Any) -> str:
    lines: list[str] = [
        f"\nTesting {func.__name__.replace('_', ' ')}...",
        f"before: {args[0]}",
        f"after: {func(*args)}",
    ]
    return "\n\n".join(lines)


def main() -> None:
    artifacts = [
        {"name": "Shadow Blade", "power": 73, "type": "relic"},
        {"name": "Storm Crown", "power": 103, "type": "accessory"},
        {"name": "Earth Shield", "power": 97, "type": "accessory"},
        {"name": "Wind Cloak", "power": 114, "type": "relic"},
    ]
    mages = [
        {"name": "Phoenix", "power": 99, "element": "wind"},
        {"name": "Rowan", "power": 82, "element": "lightning"},
        {"name": "Nova", "power": 75, "element": "fire"},
        {"name": "Casey", "power": 68, "element": "lightning"},
        {"name": "Ember", "power": 84, "element": "fire"},
    ]
    spells = ["tornado", "darkness", "meteor", "fireball"]
    print(test_function(artifact_sorter, artifacts))
    print(test_function(power_filter, mages, 80))
    print(test_function(spell_transformer, spells))
    print(test_function(mage_stats, mages))


if __name__ == "__main__":
    main()
