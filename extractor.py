import fitz
import re


class PDFExtractor:

    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.doc = fitz.open(pdf_path)

    def close(self):
        self.doc.close()

    def extract(self):

        page = self.doc[0]

        words = page.get_text("words")

        drawing = self.get_drawing(words)

        paint = self.get_paint(words)

        color = self.get_color(words)

        return {
            "Drawing No": drawing,
            "Paint System": paint,
            "Top Coat Color": color
        }

    def get_drawing(self, words):

        for w in words:

            txt = w[4]

            if re.fullmatch(r"AG-[A-Z0-9\-]+", txt):

                if "_C" not in txt:

                    return txt

        return ""

    def get_paint(self, words):

        txt = self.get_all_text(words)

        m = re.search(r"\bN\d+\b", txt)

        if m:

            return m.group()

        return ""

    def get_color(self, words):

        txt = self.get_all_text(words)

        colors = [
            "Gray or Silver",
            "Grey or Silver",
            "Silver",
            "Gray",
            "None"
        ]

        for c in colors:

            if c.lower() in txt.lower():

                return c

        return ""

    def get_all_text(self, words):

        text = ""

        for w in words:

            text += w[4] + " "

        return text
테스트용 (main.py)
from extractor import PDFExtractor

pdf = PDFExtractor("AG-1-002-MOFF-04_C3.pdf")

data = pdf.extract()

print(data)

pdf.close()
