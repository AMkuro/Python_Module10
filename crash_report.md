# クラッシュレポート

各演習ファイルに対してエッジケーステストを実施した結果。

---

## Ex0 `lambda_spells.py`

| テスト | 結果 |
|--------|------|
| `mage_stats([])` | **CRASH** `ValueError: max() arg is an empty sequence` |
| `artifact_sorter([{"name": "X"}])` (powerキーなし) | **CRASH** `KeyError: 'power'` |
| `power_filter(None, 10)` | **CRASH** `TypeError: 'NoneType' object is not iterable` |

---

## Ex1 `higher_magic.py`

| テスト | 結果 |
|--------|------|
| `spell_combiner(None, lambda x: x)` を呼び出し | **CRASH** `TypeError: 'NoneType' object is not callable` |
| `conditional_caster(None, lambda x: x)` を呼び出し | **CRASH** `TypeError: 'NoneType' object is not callable` |
| `power_amplifier(lambda x: "hello", 3)` | クラッシュなし（文字列×3 = `"hellohellohello"` が返る、意図しない挙動） |

---

## Ex2 `scope_mysteries.py`

| テスト | 結果 |
|--------|------|
| `spell_accumulator(10)` に文字列を渡す | **CRASH** `TypeError: unsupported operand type(s) for +=: 'int' and 'str'` |
| `enchantment_factory("")` | クラッシュなし（`" Sword"` のように先頭スペースが入る） |
| `memory_vault` で存在しないキーを `recall` | クラッシュなし（`"Memory not found"` を返す） |

---

## Ex3 `functools_artifacts.py`

| テスト | 結果 |
|--------|------|
| `spell_reducer([], "add")` など全操作 | **CRASH** `ValueError: spells must not be empty for ...` |
| `spell_reducer([1,2], "unknown")` | **CRASH** `ValueError: Unsupported operation: unknown` |
| `memoized_fibonacci(-1)` | クラッシュなし（`-1` を返す、数学的に誤り） |
| `memoized_fibonacci(2000)` | **CRASH** `RecursionError: maximum recursion depth exceeded`（lru_cache があっても初回は2000段の再帰が必要） |
| `partial_enchanter(None)` | **CRASH** `TypeError: the first argument must be callable` |

---

## Ex4 `decorator_mastery.py`

| テスト | 結果 |
|--------|------|
| `spell_timer` でラップした関数が例外を送出 | **CRASH** 例外が素通り（`"Spell completed in X seconds"` も表示されない） |
| `guild.cast_spell("Fire")` (power引数なし) | **CRASH** `IndexError: tuple index out of range`（`power_validator` が `args[2]` を参照するため） |
| `MageGuild.validate_mage_name(None)` | **CRASH** `TypeError: object of type 'NoneType' has no len()` |
| `retry_spell(0)` でラップした失敗関数を呼び出し | クラッシュなし（`"Spell casting failed after 0 attempts"` を返す） |

---

## 共通ルールとの照合

仕様 IV.1 より:「例外は適切に処理し、クラッシュを避けること」

上記のうち、特に実用上問題になりやすいもの:

- `mage_stats([])` — 空リストは自然な入力として起こりうる
- `cast_spell("Fire")` で power 省略時の `IndexError` — エラーメッセージが原因を示さない
- `spell_timer` 内例外の素通り — デコレータとして不完全
