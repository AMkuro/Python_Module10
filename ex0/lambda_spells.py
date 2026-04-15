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


def format_artifact_sorter(artifacts: list[dict]) -> str:
    sorted_artifacts = artifact_sorter(artifacts)
    leader = sorted_artifacts[0]
    runner_up = sorted_artifacts[1]
    trailer = sorted_artifacts[-1]
    return "\n".join(
        [
            f"{leader['name']} ({leader['power']} power) comes before "
            f"{runner_up['name']} ({runner_up['power']} power)",
            f"{trailer['name']} ({trailer['power']} power) trails the ranking",
        ]
    )


def format_power_filter(mages: list[dict], min_power: int) -> str:
    strong_mages = power_filter(mages, min_power)
    names = ", ".join(mage["name"] for mage in strong_mages)
    return f"Mages at or above {min_power} power: {names}"


def format_spell_transformer(spells: list[str]) -> str:
    transformed = spell_transformer(spells)
    return f"{' '.join(transformed)}\nEach spell is wrapped in rune marks"


def format_mage_stats(mages: list[dict]) -> str:
    stats = mage_stats(mages)
    return "\n".join(
        [
            f"Max power: {stats['max_power']}",
            f"Min power: {stats['min_power']}",
            f"Average power: {stats['avg_power']:.2f}",
        ]
    )


def test_function(func: Callable, *args: Any) -> str:
    formatters: dict[str, Callable[..., str]] = {
        "artifact_sorter": format_artifact_sorter,
        "power_filter": format_power_filter,
        "spell_transformer": format_spell_transformer,
        "mage_stats": format_mage_stats,
    }
    lines: list[str] = [
        f"\nTesting {func.__name__.replace('_', ' ')}...",
        formatters[func.__name__](*args),
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
