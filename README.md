<img src="doc/jmd_logo.svg" align="center" height="110"/>

## Motivation

When writing documentation, often multiple Markdown files are required to produce for example a wiki page or similar. Producing a pdf out of multiple files is not straight forward and can take a considerable ammount of scripting. This tool aims to reduce the workload required to produce on Markdown file out of multiple files by extending `yml` metadata by two new entries:

- `parsed_document_id`: Parsed document ID specyfies which document should be in the final markdown file. If parsed_document_id matches the definition of the function call, the .md file will be included.
- `parsed_document_position`: This specyfies the postition, at which the .md file should be placed in the final .md file.

## Installing

## Usage

The script can be called by using

```bash
python3 jmd.py [options]
```

Options are:

- `--document_id`: Specyfies the ID of to be included files. (default: `doc`)
- `--output`: Output directory/filename. This shall also include the extension `.md`. Example: `doc/documentation.md`. (default: `./document.md`)
- `--base_dir`: Base directory, the tool shall look for Markdown files. (default: `.`)
- `--include_title`: Include meta data title as first level title (#). (default: `False`)

<!-- - `--header_offset`: Add an additional `#` to titles in order to manipulate final file structure. (default: `False`)
- `--meta_data_path`: Reference a file, where metadata in yml format shall be included from. (default: 'none')
- `--reduce_infile_references`: Reduce file references that are now merged. (default: `False`) **Still needs Work! What if references a file that is not included?**
- `--pandoc_references`: Output Markdown file with Pandoc ready in file references. (default: `False`)
- `--set_default_true`: Set all default false to default true to have a cleaner cmd command. (default: `False`)
- `--detect_html_tex_tags`: Detect LaTeX commands nested in html tags (default: `False`) -->

## Conventions

- `parsed_document_position: 0` is reserved for meta data.
- In wiki tools, the `#` is used for the main title. So in order for a structured text, the highest title level shall be `##`.

<!--
## Detecting HTML Tags for LaTeX

Sometimes, Sepcial Markdown files are important!

<p tex-begin="landscape"/>

<p tex-command="\textbf{This is only visible in latex!}"/>

<p tex-end="landscape"/>

## Global LaTeX Commands

Global environments on an entire file can be added via the yaml header file. Include the keywords `parse-header` and / or `parse-footer` to do so. A use case would be to put the entire file into landscape mode. this would be achieved as follows:

```markdown
---
    parsed-header: "\\Begin{landscape}"
    parsed-footer: "\\End{landscape}"
---
```

## \Begin{} & \End{}

Setting latex environments in a markdown file, basically breaks all Markdown code inside the environment. To fix this, `\Begin{}` and `\End{}` is used instead of `\begin{}` and `\end{}`. Please add the following code to your template.tex file in order to make it work:

```latex
\let\Begin\begin
\let\End\end
```
-->
