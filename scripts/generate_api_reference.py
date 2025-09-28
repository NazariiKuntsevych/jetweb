from pathlib import Path

import mkdocs_gen_files

nav = mkdocs_gen_files.Nav()
code_root_path = Path(__file__).parent.parent.joinpath("jetweb")
doc_root_path = Path("reference", "api")

for path in sorted(code_root_path.rglob("*.py")):
    file_path = path.relative_to(code_root_path)
    doc_path = path.relative_to(code_root_path).with_suffix(".md")

    if not file_path.parts or path.stem == "__init__" or path.is_dir():
        continue

    nav[file_path.parts] = doc_path.as_posix()

    with mkdocs_gen_files.open(doc_root_path.joinpath(doc_path), "w") as fd:
        ident = ".".join(["jetweb", *file_path.with_suffix("").parts])
        fd.write(f"::: {ident}")

with mkdocs_gen_files.open(doc_root_path.joinpath("reference.md"), "w") as nav_file:
    nav_file.writelines(nav.build_literate_nav())
