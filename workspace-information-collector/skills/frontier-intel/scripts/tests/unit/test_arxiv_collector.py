import unittest
import xml.etree.ElementTree as ET

from scripts.lib.collectors.arxiv import ArxivCollector


class ArxivCollectorTest(unittest.TestCase):
    def test_pdf_url_resolution(self) -> None:
        xml_payload = """
        <entry xmlns=\"http://www.w3.org/2005/Atom\">
          <id>https://arxiv.org/abs/1234.5678</id>
          <title> Test Paper </title>
          <summary> Hello world </summary>
          <link href=\"https://arxiv.org/abs/1234.5678\" rel=\"alternate\" type=\"text/html\" />
          <link title=\"pdf\" href=\"https://arxiv.org/pdf/1234.5678.pdf\" rel=\"related\" type=\"application/pdf\" />
        </entry>
        """
        entry = ET.fromstring(xml_payload)
        collector = ArxivCollector()

        pdf_url = collector._pdf_url(entry)

        self.assertEqual(pdf_url, "https://arxiv.org/pdf/1234.5678.pdf")


if __name__ == "__main__":
    unittest.main()
