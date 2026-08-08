import base64
import io

from pypdf import PdfReader


class PDFExtractor:

    @staticmethod
    def extract_text(content: str) -> str:
        pdf_bytes = base64.b64decode(content)

        reader = PdfReader(
            io.BytesIO(pdf_bytes)
        )

        text = "\n".join(
            page.extract_text() or ""
            for page in reader.pages
        )

        print("\n===== DEVIS DECODE =====")
        print(text)
        print("========================\n")

        return text