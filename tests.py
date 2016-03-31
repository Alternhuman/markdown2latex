#!/usr/bin/env python
import unittest
from markdown import Markdown
from mdx_latex import LaTeXExtension

class LaTeXTest(unittest.TestCase):
    def setUp(self):
        self.md = Markdown()
        mkdn2latex = LaTeXExtension(configs={}, maketitle=True)

        mkdn2latex.extendMarkdown(self.md, Markdown.__dict__)

@unittest.skip("Not ready yet")
class TestEscapePattern(LaTeXTest):

    def test_re(self):
        text = "<"
        print(self.md.convert(text))
        self.assertEqual(1,1)

class TestReferencePattern(LaTeXTest):

    def test_re(self):
        texts = [("""[text][with_a_ref]

[with_a_ref]: http://theref.org
        """, "\\href{http://theref.org}{text}"),
        ("""[text][3]

[3]: something.org""","\\href{something.org}{text}")
        ]
        for text, result in texts: 
            self.assertEqual(self.md.convert(text),result)

if __name__ == '__main__':
    unittest.main()