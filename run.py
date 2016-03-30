#!/usr/bin/env python
from markdown import Markdown
from mdx_latex import LaTeXExtension

def main():
    import argparse
    usage = \
'''usage: %prog [options] <in-file-path>

Given a file path, process it using markdown2latex and print the result on
stdout.

If using template option template should place text INSERT-TEXT-HERE in the
template where text should be inserted.
'''
    parser = argparse.ArgumentParser(description=usage)
    parser.add_argument('-t', '--template', dest='template',
                      default='', help='path to latex template file (optional)')
    (options, args) = parser.parse_args()
    if not len(args) > 0:
        parser.print_help()
        sys.exit(1)

    inpath = args[0]
    with open(inpath, 'r') as infile:

        md = markdown.Markdown()
        mkdn2latex = LaTeXExtension()
        mkdn2latex.extendMarkdown(md, markdown.__dict__)
        out = md.convert(infile.read())

        if options.template:
            with open(options.template) as tmpl_fo:
                out = template(tmpl_fo, out)

    print(out)


if __name__ == "__main__":
    text = \
"""
# This is a demo
## This is a head
### This is a subsection
#### This is a subsubsection
##### What is this?

* This is a list

End of list

1. This is an *enumeration*

This is a regular text

> This is a quotation

Inline `inline` code

```
This is code
```

    This is a code block

*This is an emphasized text*

This is a second *emphasized* text
This is **strong**


"""

    text = """[title](http://link_a.com&path=Something "Title")
<http://url.com>
<mail@mail.com>
[mail](mailto:mail@mail.com)
*Standalone text
_Standalone text

_Not standalone text_

***strongem***

"""
    text = """![image](image_url.png)"""

    md = Markdown()
    mkdn2latex = LaTeXExtension(configs={}, maketitle=True)

    mkdn2latex.extendMarkdown(md, Markdown.__dict__)

    out = md.convert(text)

    print(out)
