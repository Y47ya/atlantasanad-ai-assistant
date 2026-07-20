from pathlib import Path
from docling.document_converter import DocumentConverter
from docling_core.types import DoclingDocument
from docling_core.types.doc import DocItemLabel
from src.ingestion.models.document import Document
from src.config.settings import PROJECT_ROOT
from src.ingestion.models.section import Section, ContentBlock, ContentType
from src.ingestion.tools import generate_document_id


# from tests.ingestion.parser_testor import file_path


class DoclingAdapter:

    def __init__(self):
        self.converter = DocumentConverter()

    def looks_like_heading(self, item):

        if item.label != DocItemLabel.SECTION_HEADER:
            return False

        text = item.text.strip()

        if text == "Réponse :":
            return False

        return True

    def parse(self, pdf_path: Path) -> Document:

        # result = self.converter.convert(pdf_path)
        # doc = result.document

        # Used only for debugging to reduce memory usage
        # read result's parsed content directly
        file_name = pdf_path.name.split(".")[0]
        output = Path(PROJECT_ROOT / f"tests/parsed_data/{file_name}.json")
        try:
            doc = DoclingDocument.load_from_json(output)
        except:
            result = self.converter.convert(pdf_path)
            doc = result.document
            doc.save_as_json(output)
            print("parsed file saved")
        # -------------------------------------------------

        pages_count = doc.num_pages()

        document_id = generate_document_id(pdf_path)

        document = Document(
            id=document_id,
            title=Path(pdf_path).stem,
            file_name=Path(pdf_path).name,
            pages_count=pages_count,
        )

        current_section = None

        for item, _ in doc.iterate_items():

            page = item.prov[0].page_no if item.prov else 0

            if self.looks_like_heading(item):

                current_section = Section(
                    title=item.text.strip(),
                    page=page,
                )
                document.sections.append(current_section)
                continue

            if current_section is None:
                continue

            if item.label == DocItemLabel.TEXT:
                current_section.content.append(
                    ContentBlock(
                        type=ContentType.TEXT,
                        content=item.text.strip(),
                    )
                )

            elif item.label == DocItemLabel.LIST_ITEM:
                current_section.content.append(
                    ContentBlock(
                        type=ContentType.LIST_ITEM,
                        content=item.text.strip(),
                    )
                )

            elif item.label == DocItemLabel.TABLE:
                current_section.content.append(
                    ContentBlock(
                        type=ContentType.TABLE,
                        content=item.export_to_markdown(),
                    )
                )

        return document


# file_path = Path(PROJECT_ROOT / "data/raw/Véhicule_pro.pdf")
# file_path1 = Path(PROJECT_ROOT / "data/raw/assurance_automobile_fr_version_finale.pdf")
#
# parsed_data_dir = Path(PROJECT_ROOT / "tests/parsed_data")
#
# parsed_data_dir.parent.mkdir(exist_ok=True)
# parsed_data_dir.mkdir(exist_ok=True)
#
# docliing_adapter = DoclingAdapter()
#
# # docliing_adapter.parse(file_path)
#
# result = docliing_adapter.parse(file_path)
# print(result)