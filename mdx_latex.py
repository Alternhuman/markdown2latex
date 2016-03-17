#!/usr/bin/env python
"""Extension to python-markdown to support LaTeX (rather than html) output.

Authored by Rufus Pollock: <http://www.rufuspollock.org/>

Usage:
======

1. Command Line. A script entitled markdown2latex.py is automatically
installed. For details of usage see help::

    $ markdown2latex.py -h

2. As a python-markdown extension::

    >>> import markdown
    >>> md = markdown.Markdown(None, extensions=['latex'])
    >>> # text is input string ...
    >>> latex_out = md.convert(text)

3. Directly as a module (slight inversion of std markdown extension setup)::

    >>> import markdown
    >>> import mdx_latex
    >>> md = markdown.Markdown()
    >>> latex_mdx = mdx_latex.LaTeXExtension()
    >>> latex_mdx.extendMarkdown(md, markdown.__dict__)
    >>> out = md.convert(text)

History
=======

Version: 1.0 (November 15, 2006)

  * First working version (compatible with markdown 1.5)
  * Includes support for tables

Version: 1.1 (January 17, 2007)

  * Support for verbatim and images

Version: 1.2 (June 2008)

  * Refactor as an extension.
  * Make into a proper python/setuptools package.
  * Tested with markdown 1.7 but should work with 1.6 and (possibly) 1.5
    (though pre/post processor stuff not as worked out there)

Version 1.3: (July 2008)
  * Improvements to image output (width)

Version 1.3.1: (August 2009)
  * Tiny bugfix to remove duplicate keyword argument and set zip_safe=False
  * Add [width=\textwidth] by default for included images
"""

# do some fancy importing stuff to allow use to override things in this module
# in this file while still importing * for use in our own classes
import re
#import sys
#import markdown
from markdown.postprocessors import Postprocessor
#from markdown.preprocessors import Preprocessor
from markdown.inlinepatterns import Pattern, SimpleTextPattern, SimpleTagPattern
from markdown.treeprocessors import Treeprocessor
from markdown.extensions import Extension
import markdown.inlinepatterns as inlinepatterns
#import xml.dom.minidom
from markdown.util import etree
__version__ = '1.3.1'


start_single_quote_re = re.compile("""(^|\s|")'""")
start_double_quote_re = re.compile('''(^|\s|'|`)"''')
end_double_quote_re = re.compile('"(,|\.|\s|$)')

def unescape_html_entities(text):

    if (text is None): return ""
    """
    Reverses the escaping process that Markdown does for HTML
    :param: str text The text to escape
    """
    out = text.replace('&amp;', '&')
    out = out.replace('&lt;', '<')
    out = out.replace('&gt;', '<')
    out = out.replace('&quot;', '"')
    return out
#
def escape_latex_entities(text):
    """Escape latex reserved characters using the '\\' character"""

    if(text is None): return ""

    out = text
    out = unescape_html_entities(out)
    out = out.replace('%', '\\%')
    out = out.replace('&', '\\&')
    out = out.replace('#', '\\#')
    out = out.replace('_', '\\_')
    out = out.replace('~', '\\~')
    # TODO: Check how this should work
    out = start_single_quote_re.sub('\g<1>`', out)
    out = start_double_quote_re.sub('\g<1>``', out)
    out = end_double_quote_re.sub("''\g<1>", out)
    # TODO: people should escape these themselves as it conflicts with maths
    # out = out.replace('{', '\\{')
    # out = out.replace('}', '\\}')
    # do not do '$' here because it is dealt with by convert_maths
    # out = out.replace('$', '\\$')


    #TODO:    & % $ # _ { } ~ ^ \
    # See: http://tex.stackexchange.com/a/34586/76599
    return out

#
# def unescape_latex_entities(text):
#     """Limit ourselves as this is only used for maths stuff."""
#     out = text
#     out = out.replace('\\&', '&')
#     return out
#
# def makeExtension(configs=None):
#     """Creates the LaTeX markdown extension"""
#     return LaTeXExtension(configs=configs)
#
class LaTeXExtension(Extension):

    def __init__ (self, **kwargs):
        self.maketitle = kwargs.pop("maketitle", False)
        super(LaTeXExtension, self).__init__(**kwargs)
        self.reset()

    def extendMarkdown(self, md, md_globals):
        self.md = md

        # remove escape pattern -- \\(.*) -- as this messes up any embedded
        # math and we don't need to escape stuff any more for html

        remove_patterns = [inlinepatterns.ESCAPE_RE, inlinepatterns.EMPHASIS_RE]
        #i= next((index for (index,pat) in self.md.inlinePatterns.items() if pat.pattern == inlinepatterns.ESCAPE_RE), None)
        #if i is not None:
        #    print(i)
        #    del self.md.inlinePatterns[i]
        for i in ((index for (index,pat) in self.md.inlinePatterns.items() if pat.pattern in remove_patterns)):
            if i is not None:
                del self.md.inlinePatterns[i]

#         #for pat in self.md.inlinePatterns:
#         #    if pat.pattern == markdown.ESCAPE_RE:
#         #        idx = self.md.inlinePatterns.index(pat)
#         #        del self.md.inlinePatterns[idx]
#         #        break
#
        # Insert a post-processor that would actually add the footnote div
        treeprocessor = LaTeXTreeProcessor(maketitle=self.maketitle)
        #index = md.inlinePatterns.index(md_globals['IMAGE_REFERENCE_PATTERN'])
        #md.inlinePatterns.insert(1,key="emphasis", value=InlineProcessor(inlinepatterns.EMPHASIS_RE, self))
        #del md.inlinePatterns['strong']
        #del md.inlinePatterns['emphasis']
        #del md.inlinePatterns['strong_em']
        #del md.inlinePatterns['em_strong']
        #del md.inlinePatterns['emphasis2']
        #del md.inlinePatterns['not_strong'] #md.inlinePatterns.add('em', InlineProcessor(inlinepatterns.EMPHASIS_RE, md), )

        #md.inlinePatterns["emphasis"]= InlineProcessor(inlinepatterns.EMPHASIS_RE)
        """
        inlinePatterns = odict.OrderedDict()
    #inlinePatterns["backtick"] = BacktickPattern(BACKTICK_RE)
    #inlinePatterns["escape"] = EscapePattern(ESCAPE_RE, md_instance)
    #inlinePatterns["reference"] = ReferencePattern(REFERENCE_RE, md_instance)
    #inlinePatterns["link"] = LinkPattern(LINK_RE, md_instance)
    inlinePatterns["image_link"] = ImagePattern(IMAGE_LINK_RE, md_instance)
    inlinePatterns["image_reference"] = ImageReferencePattern(
        IMAGE_REFERENCE_RE, md_instance
    )
    inlinePatterns["short_reference"] = ReferencePattern(
        SHORT_REF_RE, md_instance
    )
    inlinePatterns["autolink"] = AutolinkPattern(AUTOLINK_RE, md_instance)
    inlinePatterns["automail"] = AutomailPattern(AUTOMAIL_RE, md_instance)
    inlinePatterns["linebreak"] = SubstituteTagPattern(LINE_BREAK_RE, 'br')
    if md_instance.safeMode != 'escape':
        inlinePatterns["html"] = HtmlPattern(HTML_RE, md_instance)
    inlinePatterns["entity"] = HtmlPattern(ENTITY_RE, md_instance)
    inlinePatterns["not_strong"] = SimpleTextPattern(NOT_STRONG_RE)
    inlinePatterns["em_strong"] = DoubleTagPattern(EM_STRONG_RE, 'strong,em')
    inlinePatterns["strong_em"] = DoubleTagPattern(STRONG_EM_RE, 'em,strong')
    if md_instance.smart_emphasis:
        inlinePatterns["emphasis2"] = SimpleTagPattern(SMART_EMPHASIS_RE, 'em')
    else:
        inlinePatterns["emphasis2"] = SimpleTagPattern(EMPHASIS_2_RE, 'em')
    return inlinePatterns
    """

        md.inlinePatterns["backtick"] = MacroPattern(inlinepatterns.BACKTICK_RE, macro='verb')
        #TODO md.inlinePatterns["escape"] = EscapePattern(inlinepatterns.ESCAPE_RE, md_instance)
        #TODO: Really necessary? md.inlinePatterns["reference"] = ReferencePattern(inlinepatterns.REFERENCE_RE, md_instance)
        md.inlinePatterns["link"] = LinkPattern(inlinepatterns.LINK_RE)
        md.inlinePatterns["emphasis"] = EmphasisPattern(inlinepatterns.EMPHASIS_RE)
        md.inlinePatterns["strong"] = StrongPattern(inlinepatterns.STRONG_RE)
        #TODO md.inlinePatterns["linebreak"] = LineBreakPattern(inlinepatterns.LINE_BREAK_RE)
        md.treeprocessors['latex'] = treeprocessor

#          math_pp = MathTextPostProcessor()
#         table_pp = TableTextPostProcessor()
#         image_pp = ImageTextPostProcessor()
#         unescape_html_pp = UnescapeHtmlTextPostProcessor()
#         md.textPostprocessors.append(math_pp)
#         md.textPostprocessors.append(table_pp)
#         md.textPostprocessors.append(image_pp)
#         # run last TODO: Why?
#         md.textPostprocessors.append(unescape_html_pp)
#
#         footnote_extension = FootnoteExtension()
#         footnote_extension.extendMarkdown(md, md_globals)
#
    def reset(self) :
        # TODO: What would the purpose of this be?
        pass

class LaTeXTreeProcessor(Treeprocessor):

    def __init__(self, *args, **kwargs):
        self.maketitle = kwargs.pop("maketitle", False)
        super(Treeprocessor, self).__init__(*args, **kwargs)

    def run(self, root):
        '''Walk the dom converting relevant nodes to text nodes with relevant content.'''

        latex_text = self.tolatex(root)
        #return latex_text
#         # attach latex text as only element
#         # have to put it in a p tag as text node for document element does not
#         # work ...
#         #
#         # with stripTopLevelTags True (default) convert strips out first 23 and
#         # last 7 chars
#         # (this is the extra stuff added in by Markdown._transform ...)
#         # <span> = 6, </span> = 7
#         latex_text = 'X' * 17 + latex_text
#         # do not use p or li as they result in indentation
#         latex_node = doc.createElement('span', latex_text)
#         doc.appendChild(latex_node)
#

    def tolatex(self, node):
        buffer = ""
        subcontent = ""

        if node.tag == 'div':
            for n in node:
                buffer += self.tolatex(n)
            node.clear()
            node.text = buffer

        # Sections
        elif node.tag == 'h1':
            buffer +='\n\\title{%s}\n' % node.text
            if self.maketitle:
                buffer += """
% ----------------------------------------------------------------
\maketitle
% ----------------------------------------------------------------
"""
            return buffer

        elif node.tag == 'h2':
            buffer += '\n\n\\section{%s}\n' % node.text
            return buffer
        elif node.tag == 'h3':
            buffer += '\n\n\\subsection{%s}\n' % node.text
            return buffer
        elif node.tag == 'h4':
            buffer += '\n\\subsubsection{%s}\n' % node.text
            return buffer
        elif node.tag in ['p', 'h5', 'h6']:
            buffer += escape_latex_entities(node.text) if node.text else ""
            #if node.text is not None:
            #    print(node.text, len(node.text))
            for n in node:
                text = self.tolatex(n)
                n.clear()
                n.text = text
                if(hasattr(n,'tag') and n.tag == 'code'):
                    text = """\\begin{verbatim}%s\\end{verbatim}""" % n.text
                else:
                    text = n.text

                buffer += escape_latex_entities(text)
            buffer +='\n'
            return buffer

        # Lists
        elif node.tag in ['ul', 'ol']:

            macro = 'itemize' if node.tag == 'ul' else 'enumerate'
            for n in node:
                buffer += self.tolatex(n)

            buffer = """
\\begin{%s}
%s\\end{%s}
""" % (macro, buffer, macro)

            return buffer
        elif node.tag == 'li':

            if node.text != "\n":
                buffer += node.text

            for n in node:
                buffer += self.tolatex(n)
            buffer = "\item %s\n" % buffer
            return buffer

        elif node.tag == 'blockquote':
            for n in node:
                buffer += n.text
            buffer += """
\\begin{quotation}
%s\\end{quotation}
""" % buffer
            return buffer
        elif (node.tag == 'code'):
            buffer = """\\begin{verbatim}%s\\end{verbatim}""" % node.text
            return buffer
        # ignore 'code' when inside pre tags
        # (mkdn produces <pre><code></code></pre>)
        # TODO: Second condition will only be true iff the first one is too, thus it is redundant
        elif (node.tag in ['pre', 'code'] or (node.tag == 'pre' and node.parent.tag != 'pre')):

            for n in node:
                buffer += n.text
            buffer = """
\\begin{verbatim}
%s\\end{verbatim}
""" % buffer

            return buffer
        elif node.tag == 'q':
            buffer += "`%s'" % node.text
            return buffer

        # Phrase emphasis
        elif node.tag == 'em':
            buffer += "\\emph{%s}" % node.text
            return buffer

#         elif ournode.nodeName == 'p':
#             buffer += '\n%s\n' % subcontent.strip()
#         # Footnote processor inserts all of the footnote in a sup tag
#         elif ournode.nodeName == 'sup':
#             buffer += '\\footnote{%s}' % subcontent.strip()
#         elif ournode.nodeName == 'strong':
#             buffer += '\\textbf{%s}' % subcontent.strip()
#         elif ournode.nodeName == 'em':
#             buffer += '\\emph{%s}' % subcontent.strip()
#         else:
#             buffer = subcontent
#         return buffer

        else:
            print("I do not know %s" % node.tag)
            return node.text


#         if ournode.type == 'text':
#             text = escape_latex_entities(ournode.value)
#             return text
#
#         if ournode.childNodes or ournode.nodeName in ['blockquote']:
#             for child in ournode.childNodes :
#                 subcontent += self.tolatex(child)
#
#         if ournode.nodeName == 'h1':
#             buffer += '\n\\title{%s}\n' % subcontent
#             buffer += '''
# % ----------------------------------------------------------------
# \maketitle
# % ----------------------------------------------------------------
# '''
#         elif ournode.nodeName == 'h2':
#             buffer += '\n\n\\section{%s}\n' % subcontent
#         elif ournode.nodeName == 'h3':
#             buffer += '\n\n\\subsection{%s}\n' % subcontent
#         elif ournode.nodeName == 'h4':
#             buffer += '\n\\subsubsection{%s}\n' % subcontent
#         elif ournode.nodeName == 'ul':
#             # no need for leading \n as one will be provided by li
#             buffer += '''
# \\begin{itemize}%s
# \\end{itemize}
# ''' % subcontent
#         elif ournode.nodeName == 'ol':
#             # no need for leading \n as one will be provided by li
#             buffer += '''
# \\begin{enumerate}%s
# \\end{enumerate}
# ''' % subcontent
#         elif ournode.nodeName == 'li':
#             buffer += '''
#   \\item %s''' % subcontent.strip()
#         elif ournode.nodeName == 'blockquote':
#             # use quotation rather than quote as quotation can support multiple
#             # paragraphs
#             buffer += '''
# \\begin{quotation}
# %s
# \\end{quotation}
# ''' % subcontent.strip()
#         # ignore 'code' when inside pre tags
#         # (mkdn produces <pre><code></code></pre>)
#         elif (ournode.nodeName == 'pre' or
#             (ournode.nodeName == 'pre' and ournode.parentNode.nodeName != 'pre')):
#             buffer += '''
# \\begin{verbatim}
# %s
# \\end{verbatim}
# ''' % subcontent.strip()
#         elif ournode.nodeName == 'q':
#             buffer += "`%s'" % subcontent.strip()
#         elif ournode.nodeName == 'p':
#             buffer += '\n%s\n' % subcontent.strip()
#         # Footnote processor inserts all of the footnote in a sup tag
#         elif ournode.nodeName == 'sup':
#             buffer += '\\footnote{%s}' % subcontent.strip()
#         elif ournode.nodeName == 'strong':
#             buffer += '\\textbf{%s}' % subcontent.strip()
#         elif ournode.nodeName == 'em':
#             buffer += '\\emph{%s}' % subcontent.strip()
#         else:
#             buffer = subcontent
#         return buffer

class LinkPattern(SimpleTextPattern):

    @staticmethod
    def dequote(string):
        """Remove quotes from around a string."""
        if ((string.startswith('"') and string.endswith('"')) or
           (string.startswith("'") and string.endswith("'"))):
            return string[1:-1]
        else:
            return string

    def handleMatch(self, m):
        #el = util.etree.Element("a")
        text = escape_latex_entities(m.group(2))
        #title = m.group(13)
        href = escape_latex_entities(m.group(9))
        if href:
            if href[0] == "<":
                href = href[1:-1]
            #TODO el.set("href", self.sanitize_url(self.unescape(href.strip())))
        else:
            href = ""

        if text:
            return "\\href{%s}{%s}" % (href, text)

        return "\\href{%s}" % href

class EmphasisPattern(SimpleTextPattern):
    def handleMatch(self, m):
        return "\\textit{%s}" % m.group(3)

class StrongPattern(SimpleTextPattern):
    def handleMatch(self, m):
        return "\\textbf{%s}" % m.group(3)

class LineBreakPattern(SimpleTextPattern):
    def handleMatch(self, m):
        return "\\\\"

class MacroPattern(SimpleTextPattern):
    def __init__(self, *args, **kwargs):
        self.macro = kwargs.pop('macro', '')
        super(MacroPattern, self).__init__(*args, **kwargs)
    def handleMatch(self, m):
        return "\\%s{%s}" % (self.macro, m.group(3).replace('\n', ''))

class InlineProcessor(Pattern):
    def __init__(self, *args, **kwargs):
        super(InlineProcessor, self).__init__(*args, **kwargs)
        self.compiled_re = re.compile(inlinepatterns.EMPHASIS_RE)

    def getCompiledRegExp(self):
        print("Here")
        return self.compiled_re
        #return re.compile(inlinepatterns.EMPHASIS_RE)

    def handleMatch(self, m):
        print("Here")
        el = etree.Element('')
        el.text = "Emphasized handled text"
        return el

# class UnescapeHtmlTextPostProcessor(Postprocessor):
#
#     def run(self, text):
#         return unescape_html_entities(text)
#
# # ========================= MATHS =================================
#
# class MathTextPostProcessor(Postprocessor):
#
#     def run(self, instr):
#         """Convert all math sections in {text} whether latex, asciimathml or
#         latexmathml formatted to latex.
#
#         This assumes you are using $$ as your mathematics delimiter (*not* the
#         standard asciimathml or latexmathml delimiter).
#         """
#         def repl_1(matchobj):
#             text = unescape_latex_entities(matchobj.group(1))
#             tmp = text.strip()
#             if tmp.startswith('\\[') or tmp.startswith('\\begin'):
#                 return text
#             else:
#                 return '\\[%s\\]\n' % text
#         def repl_2(matchobj):
#            text = unescape_latex_entities(matchobj.group(1))
#            return '$%s$' % text
#         # $$ ..... $$
#         pat = re.compile('^\$\$([^\$]*)\$\$\s*$', re.MULTILINE)
#         out = pat.sub(repl_1, instr)
#         # $100 million
#         pat2 = re.compile('([^\$])\$([^\$])')
#         out = pat2.sub('\g<1>\\$\g<2>', out)
#         # Jones, $$x=3$$, is ...
#         pat3 = re.compile('\$\$([^\$]*)\$\$')
#         out = pat3.sub(repl_2, out)
#         # some extras due to asciimathml
#         out = out.replace('\\lt', '<')
#         out = out.replace(' * ', ' \\cdot ')
#         out = out.replace('\\del', '\\partial')
#         return out
#
#
# # ========================= TABLES =================================
#
# class TableTextPostProcessor(Postprocessor):
#
#     def run(self, instr):
#         """This is not very sophisticated and for it to work it is expected
#         that:
#             1. tables to be in a section on their own (that is at least one blank
#             line above and below)
#             2. no nesting of tables
#         """
#         converter = Table2Latex()
#         new_blocks = []
#         for block in instr.split("\n\n") :
#             stripped = block.strip()
#             # <table catches modified verions (e.g. <table class="..">
#             if stripped.startswith('<table') and stripped.endswith('</table>'):
#                 latex_table = converter.convert(stripped).strip()
#                 new_blocks.append(latex_table)
#             else :
#                 new_blocks.append(block)
#         return '\n\n'.join(new_blocks)
#
# class Table2Latex:
#     """
#     Convert html tables to Latex.
#
#     TODO: escape latex entities.
#     """
#
#     def colformat(self):
#         # centre align everything by default
#         out = '|c' * self.maxcols + '|'
#         return out
#
#     def get_text(self, element):
#         if element.nodeType == element.TEXT_NODE:
#             return escape_latex_entities(element.data)
#         result = ''
#         if element.childNodes:
#             for child in element.childNodes :
#                 text = self.get_text(child)
#                 if text.strip() != '':
#                     result += text
#         return result
#
#     def process_cell(self, element):
#         # works on both td and th
#         colspan = 1
#         subcontent = self.get_text(element)
#         buffer = ''
#         if element.tagName == 'th':
#             subcontent = '\\textbf{%s}' % subcontent
#         if element.hasAttribute('colspan'):
#             colspan = int(element.getAttribute('colspan'))
#             buffer += ' \multicolumn{%s}{|c|}{%s}' % (colspan, subcontent)
#         # we don't support rowspan because:
#         #   1. it needs an extra latex package \usepackage{multirow}
#         #   2. it requires us to mess around with the alignment tags in
#         #   subsequent rows (i.e. suppose the first col in row A is rowspan 2
#         #   then in row B in the latex we will need a leading &)
#         # if element.hasAttribute('rowspan'):
#         #     rowspan = int(element.getAttribute('rowspan'))
#         #     buffer += ' \multirow{%s}{|c|}{%s}' % (rowspan, subcontent)
#         else:
#             buffer += ' %s' % subcontent
#         notLast = ( element.nextSibling and
#                 element.nextSibling.nodeType == element.ELEMENT_NODE and
#                 element.nextSibling.tagName in [ 'td', 'th' ])
#         if notLast:
#             buffer += ' &'
#         self.numcols += colspan
#         return buffer
#
#     def tolatex(self, element):
#         if element.nodeType == element.TEXT_NODE:
#             return ''
#
#         buffer = ''
#         subcontent = ''
#         if element.childNodes:
#             for child in element.childNodes :
#                 text = self.tolatex(child)
#                 if text.strip() != '':
#                     subcontent += text
#         subcontent = subcontent.strip()
#
#         if element.tagName == 'thead':
#             buffer += '''%s
# ''' % subcontent
#
#         elif element.tagName == 'tr':
#             self.maxcols = max(self.numcols, self.maxcols)
#             self.numcols = 0
#             buffer += '\n\\hline\n%s \\\\' % subcontent
#
#         elif element.tagName == 'td' or element.tagName == 'th':
#             buffer = self.process_cell(element)
#         else:
#             # print '"%s"' % subcontent
#             buffer += subcontent
#         return buffer
#
#     def convert(self, instr):
#         self.numcols = 0
#         self.maxcols = 0
#         dom = xml.dom.minidom.parseString(instr)
#         core = self.tolatex(dom.documentElement)
#
#         captionElements = dom.documentElement.getElementsByTagName('caption')
#         caption = ''
#         if captionElements:
#             caption = self.get_text(captionElements[0])
#
#         colformatting = self.colformat()
#         table_latex = \
# '''
# \\begin{table}
# \\begin{tabular}{%s}
# %s
# \\hline
# \\end{tabular}
# \\\\[5pt]
# \\caption{%s}
# \\end{table}
# ''' % (colformatting, core, caption)
#         return table_latex
#
#
# # ========================= IMAGES =================================
#
# class ImageTextPostProcessor(Postprocessor):
#
#     def run(self, instr):
#         """Process all img tags
#
#         Similar to process_tables this is not very sophisticated and for it
#         to work it is expected that img tags are put in a section of their own
#         (that is separated by at least one blank line above and below).
#         """
#         converter = Img2Latex()
#         new_blocks = []
#         for block in instr.split("\n\n") :
#             stripped = block.strip()
#             # <table catches modified verions (e.g. <table class="..">
#             if stripped.startswith('<img'):
#                 latex_img = converter.convert(stripped).strip()
#                 new_blocks.append(latex_img)
#             else :
#                 new_blocks.append(block)
#         return '\n\n'.join(new_blocks)
#
#
# class Img2Latex(object):
#
#     def convert(self, instr):
#         dom = xml.dom.minidom.parseString(instr)
#         img = dom.documentElement
#         src = img.getAttribute('src')
#         alt = img.getAttribute('alt')
#         out = \
# '''
# \\begin{figure}
# \\centering
# \\includegraphics[width=\\textwidth]{%s}
# \\caption{%s}
# \\end{figure}
# ''' % (src, alt)
#         return out
#
#
# '''
# ========================= FOOTNOTES =================================
#
# LaTeX footnote support.
#
# Implemented via modification of original markdown approach (place footnote
# definition in footnote market <sup> as opposed to putting a reference link).
# '''
#
#
# class FootnoteExtension (Extension):
#     DEF_RE = re.compile(r'(\ ?\ ?\ ?)\[\^([^\]]*)\]:\s*(.*)')
#     SHORT_USE_RE = re.compile(r'\[\^([^\]]*)\]', re.M) # [^a]
#
#     def __init__ (self, configs=None):
#         super(FootnoteExtension, self).__init__(configs=configs)
#         self.reset()
#
#     def extendMarkdown(self, md, md_globals):
#         self.md = md
#
#         # Stateless extensions do not need to be registered
#         md.registerExtension(self)
#
#         # Insert a preprocessor before ReferencePreprocessor
#         index = md.preprocessors.index(md_globals['REFERENCE_PREPROCESSOR'])
#         preprocessor = FootnotePreprocessor(self)
#         preprocessor.md = md
#         md.preprocessors.insert(index, preprocessor)
#
#         # Insert an inline pattern before ImageReferencePattern
#         FOOTNOTE_RE = r'\[\^([^\]]*)\]' # blah blah [^1] blah
#         index = md.inlinePatterns.index(md_globals['IMAGE_REFERENCE_PATTERN'])
#         md.inlinePatterns.insert(index, FootnotePattern(FOOTNOTE_RE, self))
#
#     def reset(self) :
#         self.used_footnotes={}
#         self.footnotes = {}
#
#     def setFootnote(self, id, text) :
#         self.footnotes[id] = text
#
#
# class FootnotePreprocessor :
#
#     def __init__ (self, footnotes) :
#         self.footnotes = footnotes
#
#     def run(self, lines) :
#
#         self.blockGuru = markdown.BlockGuru()
#         lines = self._handleFootnoteDefinitions (lines)
#
#         # Make a hash of all footnote marks in the text so that we
#         # know in what order they are supposed to appear.  (This
#         # function call doesn't really substitute anything - it's just
#         # a way to get a callback for each occurence.
#
#         text = "\n".join(lines)
#         self.footnotes.SHORT_USE_RE.sub(self.recordFootnoteUse, text)
#
#         return text.split("\n")
#
#     def recordFootnoteUse(self, match) :
#
#         id = match.group(1)
#         id = id.strip()
#         nextNum = len(list(self.footnotes.used_footnotes.keys())) + 1
#         self.footnotes.used_footnotes[id] = nextNum
#
#
#     def _handleFootnoteDefinitions(self, lines) :
#         """Recursively finds all footnote definitions in the lines.
#
#             @param lines: a list of lines of text
#             @returns: a string representing the text with footnote
#                       definitions removed """
#
#         i, id, footnote = self._findFootnoteDefinition(lines)
#
#         if id :
#
#             plain = lines[:i]
#
#             detabbed, theRest = self.blockGuru.detectTabbed(lines[i+1:])
#
#             self.footnotes.setFootnote(id,
#                                        footnote + "\n"
#                                        + "\n".join(detabbed))
#
#             more_plain = self._handleFootnoteDefinitions(theRest)
#             return plain + [""] + more_plain
#
#         else :
#             return lines
#
#     def _findFootnoteDefinition(self, lines) :
#         """Finds the first line of a footnote definition.
#
#             @param lines: a list of lines of text
#             @returns: the index of the line containing a footnote definition """
#
#         counter = 0
#         for line in lines :
#             m = self.footnotes.DEF_RE.match(line)
#             if m :
#                 return counter, m.group(2), m.group(3)
#             counter += 1
#         return counter, None, None
#
#
# class FootnotePattern(markdown.Pattern):
#
#     def __init__ (self, pattern, footnotes) :
#         markdown.Pattern.__init__(self, pattern)
#         self.footnotes = footnotes
#
#     def handleMatch(self, m, doc) :
#         sup = doc.createElement('sup')
#         id = m.group(2)
#         # stick the footnote text in the sup
#         self.footnotes.md._processSection(sup, self.footnotes.footnotes[id].split("\n"))
#         return sup
#
# def template(template_fo, latex_to_insert):
#     tmpl = template_fo.read()
#     tmpl = tmpl.replace('INSERT-TEXT-HERE', latex_to_insert)
#     return tmpl
#     # title_items = [ '\\title', '\\end{abstract}', '\\thanks', '\\author' ]
#     # has_title_stuff = False
#     # for it in title_items:
#     #    has_title_stuff = has_title_stuff or (it in tmpl)
#
# def main():
#     import argparse
#     usage = \
# '''usage: %prog [options] <in-file-path>
#
# Given a file path, process it using markdown2latex and print the result on
# stdout.
#
# If using template option template should place text INSERT-TEXT-HERE in the
# template where text should be inserted.
# '''
#     parser = argparse.ArgumentParser(description=usage)
#     parser.add_argument('-t', '--template', dest='template',
#                       default='', help='path to latex template file (optional)')
#     (options, args) = parser.parse_args()
#     if not len(args) > 0:
#         parser.print_help()
#         sys.exit(1)
#
#     inpath = args[0]
#     with open(inpath, 'r') as infile:
#
#         md = markdown.Markdown()
#         mkdn2latex = LaTeXExtension()
#         mkdn2latex.extendMarkdown(md, markdown.__dict__)
#         out = md.convert(infile.read())
#
#         if options.template:
#             with open(options.template) as tmpl_fo:
#                 out = template(tmpl_fo, out)
#
#     print(out)
