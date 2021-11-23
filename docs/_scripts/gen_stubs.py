from pathlib import Path

import mkdocs_gen_files

NAV = mkdocs_gen_files.Nav()

for path in sorted(Path("src").glob("**/*.py")):
    doc_path = path.relative_to("src", "chained_hashing").with_suffix(".md")
    NAV[doc_path.with_suffix("").parts] = doc_path

    with mkdocs_gen_files.open(Path("reference", doc_path), "w") as fid:
        print(f"::: {'.'.join(path.relative_to('src').with_suffix('').parts)}", file=fid)

with mkdocs_gen_files.open("reference/index.md", "w") as nav_file:
    nav_file.writelines(NAV.build_literate_nav())
