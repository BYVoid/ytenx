# Importer Glossary

This project uses a romanized naming scheme for Chinese phonology and rhyme-book
concepts. The SQLite importer keeps these names so it can be checked against the
existing Django models and templates. This document records the practical meaning
of the common names as used by the schema and `scripts/build_sqlite.py`.

## Core Records

| Name | Meaning | Notes |
| --- | --- | --- |
| `dzih` | 字, character entry | Usually a single Chinese character. In entry tables it is the head character being explained. |
| `sieux` / `SieuxYonh` | 小韻, homophone group | A rhyme-book unit headed by `taj`; many `dzih` entries point to one `sieux`. |
| `taj` | 代表字, representative character | The display headword for a 小韻. |
| `ziox` | 序, index/order | Primary sequence number in the relevant source or ytenx dataset. |
| `id` | local disambiguating identifier | Used where the same `dzih` appears multiple times, e.g. `東`, `東2`. |
| `yih` | 小韻中位置 | Position of a `kyonh_dzih` entry within its 小韻. |
| `ngieh` | 字義 / gloss | Explanation text from the source. |
| `tryoh` | 註釋 / note | Annotation text, used in 中原音韻 and 上古音系 tables. |

## Phonological Structure

| Name | Meaning | Notes |
| --- | --- | --- |
| `cjeng` / `CjengMux` | 聲母, initial | Initial consonant category. |
| `cjeng_lyih` / `CjengLyih` | 聲類, initial class | Higher-level class grouping initials. |
| `cjeng_byo` | 聲符 | Phonetic component used by `dciangxkox` 上古音系 data, not the same as 聲母. |
| `yonh` / `YonhMux` | 韻母, final | Final/rime category. |
| `yonh_box` | 韻部 | Rhyme group used by 分韻撮要 and 中原音韻. |
| `yonh_miuk` / `YonhMiuk` | 韻目 | Rhyme heading/category in a rhyme book. |
| `yonh_bux` / `YonhBux` | 韻部 | 洪武正韻牋 rhyme section containing tone-specific `yonh_miuk` rows. |
| `yonh_gheh` / `YonhGheh` | 韻系 | 廣韻 rhyme-series grouping used to connect 韻目 and 韻母. |
| `yonh_cjep` / `YonhCjep` | 韻攝 | One of the broad rhyme groups such as 通、江、止. |
| `deuh` | 聲調, tone | Generally 1 平, 2 上, 3 去, 4 入 unless a source has a different finer mapping. |
| `ho` | 開合 / 呼 | In 廣韻 it is effectively open/closed; in 中原音韻 it is a four-way 呼 code. |
| `tshyuk` | 促, checked/entering counterpart | Boolean: checked/entering final vs non-checked final. |
| `tuaih` | 對 / counterpart | Paired 舒/入 final, e.g. 東一 <-> 屋一. |
| `qim_jang` | 陰陽 | 分韻撮要 yin/yang register flag. |

## Pronunciation And Transcription

| Name | Meaning | Notes |
| --- | --- | --- |
| `ngix` / `NgixQim` | 擬音, reconstructed pronunciation | Stores reconstructions by scholar/system. |
| `preng` / `PrengQim` | 拼音 / romanization | Stores romanizations such as Baxter and Polyhedron. |
| `dauh` | 推導音, derived pronunciation | Stored in `kyonh_prengqim` with `dauh` prefix and referenced by 廣韻 小韻. |
| `ipa` | IPA transcription | Used directly in 洪武正韻牋. |
| `jamo` | 諺文 / Hangul transcription | Stored alongside IPA in 洪武正韻牋. |
| `qim` | 音 | Appears in names such as `KoxQim` 古音 and `QimBjin`; meaning depends on the compound. |
| `kox_qim` / `KoxQim` | 古音 | Ancient-pronunciation entries in 洪武正韻牋. |
| `qim_bjin` / `QimBjin` | 音辨-style comparison record | Groups tone-related 洪武正韻牋 小韻 rows and related audio filename metadata. |

## Fanqie

| Name | Meaning | Notes |
| --- | --- | --- |
| `pyanx` / `PyanxTshet` | 反切 | Two-character spelling of pronunciation. |
| `tshet` | 切 | The two-character 反切 string. |
| `dciangx` / `DciangxDzih` | 反切上字 | First character of the 反切. |
| `ghrax` / `GhraxDzih` | 反切下字 | Second character of the 反切. |

## Source Location

| Name | Meaning | Notes |
| --- | --- | --- |
| `cio` / `Cio` | 書葉 / source page | Page/leaf reference. The name is used as a many-to-many relation from entries and 小韻. |
| `kyenh` | 卷 | Volume number. |
| `jep` | 葉 / page | Page or leaf number inside a volume. |
| `drak_dzuon_dang` / `DrakDzuonDang` | 澤存堂本 | 廣韻 edition/page table backing `kyonh_cio`. |
| `cioTriungZiox` | source-order index | Order of a 洪武正韻牋 小韻 or 字 entry as it appears in the book. |
| `tshiih` | 次 / order | 廣韻韻目 sequence in `KuangxYonhMiukTshiih`. |

## Variant Character Tables

| Name | Meaning | Notes |
| --- | --- | --- |
| `jihthex` | 字體 / variants | Character variant dataset. |
| `dzyen_tongx` | 全等異體 | Fully equivalent variants. |
| `krau_dep` | 語義交疊異體 | Semantically overlapping variants. |
| `krenx` | 簡體 | Simplified character relation. |
| `byan` | 繁體 | Traditional character relation. |
| `tha` | Unihan 所未收錄者 / other variants | Variant characters outside the main Unihan coverage used by the source. |

## Source Modules

| Prefix | Source |
| --- | --- |
| `kyonh` | 廣韻 |
| `trngyan` | 中原音韻 |
| `pyonh` | 分韻撮要 |
| `tcenghyonhtsen` / `tcyts` | 洪武正韻牋 |
| `dciangxkox` | 上古音系 |
| `jihthex` | Variant-character data |

## Importer-Specific Notes

`scripts/build_sqlite.py` intentionally keeps several historical behaviors from
the Django importer because the generated database must match
`testdata/golden/ytenx.sqlite`.

| Behavior | Reason |
| --- | --- |
| `kyonh_yonhmiuk_yonh` links 廣韻 韻目 to non-checked `YonhMux` rows even for 入聲 韻目. | The original Django importer compared a text `deuh` value with integer `4`, so the checked-final branch was never taken. The golden DB records that behavior. |
| Many-to-many `id` values are not considered semantic in golden comparison. | Django auto-increment ids can differ when duplicate relation inserts are ignored. The relation columns are the meaningful data. |
| `dciangxkox` chooses the first matching 廣韻 小韻 for ambiguous 反切 and logs ambiguity in the old importer. | The site only stores one nullable cross-reference in `dciangxkox_dzih.sieux_yonh_id`; the standalone importer mirrors the persisted choice. |
| `cio` rows are created on demand in 洪武正韻牋 import. | The same source page can be referenced by 字、古音、逸字 entries; duplicates are ignored. |

