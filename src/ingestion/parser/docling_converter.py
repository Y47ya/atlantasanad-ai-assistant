from pathlib import Path

from docling.backend.pypdfium2_backend import PyPdfiumDocumentBackend
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions, EasyOcrOptions
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling_core.types import DoclingDocument
from docling_core.types.doc import DocItemLabel
from src.ingestion.models.document import Document
from src.config.settings import PROJECT_ROOT
from src.ingestion.models.section import Section, ContentBlock, ContentType
from src.ingestion.parser.base_parser import BaseParser
from src.ingestion.tools import generate_document_id
from docling.datamodel.pipeline_options import TableFormerMode



# from tests.ingestion.parser_testor import file_path


class DoclingAdapter(BaseParser):

    def __init__(self):
        pipeline_options = PdfPipelineOptions()
        pipeline_options.do_ocr = False
        pipeline_options.do_table_structure = True
        pipeline_options.table_structure_options.mode = TableFormerMode.ACCURATE
        pipeline_options.table_structure_options.do_cell_matching = False

        self.converter = DocumentConverter(
            format_options={
                InputFormat.PDF: PdfFormatOption(
                    pipeline_options=pipeline_options,
                    backend=PyPdfiumDocumentBackend,
                )
            }
        )

    def looks_like_heading(self, item):

        if item.label != DocItemLabel.SECTION_HEADER:
            return False

        text = item.text.strip()

        if text == "Réponse :":
            return False

        return True

    def parse(self, pdf_path: Path) -> Document:

        file_name = pdf_path.stem
        json_path = Path(PROJECT_ROOT / "data" / "parsed_data" / f"{file_name}.json")

        # result = self.converter.convert(pdf_path)
        # doc = result.document
        # full_text = doc.export_to_markdown()
        # print(full_text)

        # Used only for debugging to reduce memory usage
        # read result's parsed content directly
        if json_path.exists():
            print(f"Loading parsed document: {json_path.stem}")
            doc = DoclingDocument.load_from_json(json_path)

        else:
            print(f"Parsing PDF: {pdf_path}")

            result = self.converter.convert(pdf_path)
            doc = result.document
            doc.save_as_json(json_path)
        # -------------------------------------------------

        pages_count = doc.num_pages()

        document_id = generate_document_id(pdf_path)

        document = Document(
            id=document_id,
            title=Path(pdf_path).stem,
            file_name=Path(pdf_path).name,
            pages_count=pages_count,
        )

        current_section = Section(page=1)
        document.sections.append(current_section)

        for item, _ in doc.iterate_items():

            page = item.prov[0].page_no if item.prov else 0

            # Start a new section
            if self.looks_like_heading(item):

                current_section = Section(page=page)

                current_section.content.append(
                    ContentBlock(
                        type=ContentType.TEXT,
                        content=item.text.strip(),
                    )
                )

                document.sections.append(current_section)
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


# file_name = "Véhicule_pro"
# file_name = "Conditions Générales Auto+ 04.2024_Word"
# file_name = "assurance_automobile_fr_version_finale"
file_name = "Auto+_véhicules_utilitaires"

file_path = Path(PROJECT_ROOT / f"data/raw/{file_name}.pdf")

output = Path(PROJECT_ROOT / f"data/parsed_data/{file_name}.json")


docling_adapter = DoclingAdapter()

# docliing_adapter.parse(file_path)

result = docling_adapter.parse(file_path)
