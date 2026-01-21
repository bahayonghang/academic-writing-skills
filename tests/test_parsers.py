"""
Unit tests for parsers.py
"""

import sys
import unittest
from pathlib import Path

# Add script dirs to path
sys.path.append(str(Path(__file__).parent.parent / 'academic-writing-skills' / 'latex-paper-en' / 'scripts'))

from parsers import LatexParser, TypstParser

class TestLatexParser(unittest.TestCase):
    def setUp(self):
        self.parser = LatexParser()

    def test_split_sections(self):
        content = r"""
\documentclass{article}
\begin{document}
\section{Introduction}
Intro text.
\section{Related Work}
Related text.
\section{Method}
Method text.
\end{document}
"""
        sections = self.parser.split_sections(content)
        self.assertIn('introduction', sections)
        self.assertIn('related', sections)
        self.assertIn('method', sections)

    def test_extract_visible_text(self):
        line = r"This is \textbf{bold} and \cite{ref1} citation."
        visible = self.parser.extract_visible_text(line)
        # Should preserve text structure but might mask cite content length
        # The key is that "citation" is visible
        self.assertIn("citation", visible)
        # check if cite is masked or preserved as non-text
        # Current logic preserves the TAG but we want to check DE-AI on visible words
        pass

    def test_clean_text(self):
        content = r"Hello \textbf{World}. $x=1$. "
        cleaned = self.parser.clean_text(content)
        self.assertEqual(cleaned, "Hello World .")

class TestTypstParser(unittest.TestCase):
    def setUp(self):
        self.parser = TypstParser()

    def test_split_sections(self):
        content = """
= Introduction
Intro text.
= Related Work
Related text.
"""
        sections = self.parser.split_sections(content)
        self.assertIn('introduction', sections)
        self.assertIn('related', sections)

    def test_clean_text(self):
        content = "Hello *World*. $x=1$. // Comment"
        cleaned = self.parser.clean_text(content)
        self.assertEqual(cleaned, "Hello *World*.")

if __name__ == '__main__':
    unittest.main()
