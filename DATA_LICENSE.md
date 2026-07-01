# Data License and Use Restrictions

This document describes the licensing status of data, media, and other
non-code materials in the Ytenx repository.

The Apache License 2.0 in `LICENSE` applies only to first-party source code.
It does not apply to the materials described in this document.

## Scope

The following materials are not licensed under Apache License 2.0:

- Dictionary data, phonological data, and transcription files.
- Source data files under paths such as `ytenx/sync/**/*.txt` and
  `ytenx/sync/**/*.csv`.
- Generated databases, including SQLite database files derived from source
  data.
- Scanned book images and page images under `static/img/`.
- Audio recordings under `static/audio/`.
- Media files, icons, seals, logos, and other non-code assets.
- Textual content, excerpts, tables, and annotations derived from third-party
  books, websites, scans, or contributor submissions.

Possession of a copy of this repository does not grant permission to copy,
redistribute, sublicense, sell, publish, mirror, or otherwise reuse these
materials except as allowed by their respective rights holders or applicable
law.

## General Rule

Unless a data or media file is explicitly marked with a separate open license,
it should be treated as restricted material.

Restricted material may be present in this repository for the purpose of
operating, preserving, maintaining, and developing Ytenx. Such inclusion does
not imply that the material is open data, public domain, or available for
third-party redistribution.

Any reuse outside Ytenx should verify the original source and obtain permission
from the relevant rights holder when required.

## Generated Data

Generated databases and derived data files inherit the restrictions of the
underlying source materials. A generated database is not independently licensed
under Apache License 2.0 merely because the scripts that create it are licensed
as code.

## Source-Specific Notes

Ytenx integrates, compares, transcribes, or references materials from multiple
sources. The following list is descriptive and not exhaustive.

### Guangyun (廣韻)

Guangyun data and related classifications reference or derive from sources
including the Kanji Database Project, rhymedict, Guangyun character tables,
published editions, and scanned book images from library collections.

These materials are not generally licensed by Ytenx for redistribution.
Reuse must follow the terms of the original sources and rights holders.

### Zhongyuan Yinyun (中原音韻)

Zhongyuan Yinyun data references or derives from multiple textual sources,
including contributor transcriptions, Wikisource materials, scanned editions,
and editorial work by Ytenx contributors.

Materials from Wikisource or Wikimedia projects are governed by their own
licenses and attribution requirements. Other transcriptions, scans, and
editorial data remain subject to their respective source terms and contributor
permissions.

### Hongwu Zhengyun and Hongwu Zhengyun Jian (洪武正韻與洪武正韻牋)

Hongwu Zhengyun Jian data includes contributor transcriptions and editorial
work. Hongwu Zhengyun definitions or text may include material from Kanseki
Repository where noted.

Kanseki Repository material marked as CC BY-SA must be used under the
applicable Creative Commons Attribution-ShareAlike terms. Other related data
remains subject to its source and contributor permissions.

### Fen Yun Cuo Yao (分韻撮要)

Fen Yun Cuo Yao data and images reference historical editions, library scans,
Internet Archive materials, contributor transcriptions, and Ytenx editorial
work.

These materials are not generally licensed by Ytenx for redistribution. Reuse
must follow the terms of the original sources and rights holders.

### Old Chinese System (上古音系)

The Old Chinese system material is based on work by Zhengzhang Shangfang and
is made available on Ytenx according to permission granted for Ytenx
publication and editorial use.

This permission is not a general open license. The material may not be copied,
redistributed, or relicensed without appropriate authorization from the
relevant rights holders.

### Middle Chinese Tutorials, Audio, and Supplementary Materials (中古漢語教程、音頻與補充材料)

Tutorials, readings, audio files, and supplementary materials may include work
by named contributors such as Polyhedron and others.

Unless a specific open license is stated for a particular file or work, these
materials are restricted and may not be redistributed or reused outside Ytenx
without permission.

## Third-Party Assets

Third-party software assets such as Bootstrap, Glyphicons, and other libraries
or icons are governed by their own licenses and notices. Their presence in the
repository does not place them under the Ytenx code license.

## Attribution

When using materials that are separately licensed by their original sources,
users must preserve all required attribution, source links, copyright notices,
license notices, and share-alike obligations.

When the licensing status of a material is unclear, treat it as restricted and
do not redistribute it without permission.
