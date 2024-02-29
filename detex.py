import sys
import re

if len(sys.argv) != 2:
    print("Just give me a file and I'll do the rest!")


chapter_sections = re.compile(r"(\\chapter\{|\\section\{|\\subsection\{|\\subsubsection\{|\\paragraph\{)(.*?)(\})", re.IGNORECASE)
ignored_lines = re.compile(r"^%|^\s*$|\\label\{.*\}|\\clearpage|\\IncMargin\{.*\}|\\DecMargin\{.*\}|^\\minitoc|^\\begin{enumerate}|^\\begin{itemize}|^\\end{enumerate}|^\\end{itemize}", re.IGNORECASE)
begin_ignore = re.compile(r"^\s*(\\begin{figure\**}|\\begin{algorithm\**}|\\begin{equation\**}|\\begin{table\**}|\\begin{multline\**})", re.IGNORECASE)
end_ignore = re.compile(r"^\s*(\\end{figure\**}|\\end{algorithm\**}|\\end{equation\**}|\\end{table\**}|\\end{multline\**})", re.IGNORECASE)
ref_change = re.compile(r"\\ref{.*?}|\\eqref{.*?}", re.IGNORECASE)
just_remove = re.compile(r"\s*\\cite{.*?}|^\\begin{footnotesize}|^\\end{footnotesize}|^\\td.*{.*}", re.IGNORECASE)
just_remove_with_info = re.compile(r"(\\emph{|\\textbf{|\\textit{)(.*?)(})", re.IGNORECASE)
items = re.compile(r"\s*\\item", re.IGNORECASE)
equations_inline = re.compile(r"(\$|\\\()(.{1,}?)(\$|\\\))", re.IGNORECASE)
percentage = re.compile(r"\\%", re.IGNORECASE)

content = ''

with open(sys.argv[1], 'r') as f:
    ignore_line_bool = False
    for line in f.readlines():
        if (ignored_lines.search(line)):
            continue
        if (begin_ignore.search(line)):
            ignore_line_bool = True
            continue
        if (end_ignore.search(line)):
            ignore_line_bool = False
            continue
        if ignore_line_bool:
            continue
        if (chapter_sections.search(line)):
            content += chapter_sections.sub(r"\n\2 \n", line)
            continue
        line_changed = ref_change.sub("1", line)
        line_changed = just_remove_with_info.sub(r"\2", line_changed)
        line_changed = just_remove.sub('', line_changed)
        line_changed = items.sub('-', line_changed)
        line_changed = equations_inline.sub('', line_changed)
        line_changed = percentage.sub('%', line_changed)
        content += line_changed + '\n'

content = re.sub(r'(\n\s*)+\n+', '\n\n', content)
content = re.sub(r'\ {2}', ' ', content)
content = re.sub(r'\ \.', '.', content)
content = re.sub(r'\ \,', ',', content)
content = re.sub(r'\(\)', '', content)

print(content)