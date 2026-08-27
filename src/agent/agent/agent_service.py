from pathlib import Path
from langchain_core.messages import ToolMessage

from src.agent.tools.output_schemas.edition_devis_result import EditionDevisResult
from src.documents.pdf_service import PDFService


class AgentService:

    def __init__(
        self,
        graph,
        pdf_service: PDFService,
    ):
        self.graph = graph
        self.pdf_service = pdf_service

    def invoke(
        self,
        messages: list,
    ) -> tuple[list, list[Path]]:

        previous_count = len(messages)

        state = self.graph.invoke(
            {
                "messages": messages,
            }
        )

        messages = state["messages"]

        new_messages = messages[previous_count:]

        pdfs = self._process_documents(
            new_messages
        )

        return messages, pdfs

    def _process_documents(
            self,
            messages: list,
    ) -> list[Path]:

        pdfs = []

        for message in messages:

            if not isinstance(message, ToolMessage):
                continue

            if message.name != "edition_devis":
                continue

            content = message.content

            if isinstance(content, str):
                result = EditionDevisResult.model_validate_json(
                    content
                )
            else:
                result = EditionDevisResult.model_validate(
                    content
                )

            if result.status != "SUCCESS":
                continue

            pdf_path = self.pdf_service.save(
                content=result.message,
                prefix=f"devis_{result.policy_id}.pdf",
            )

            pdfs.append(pdf_path)

        return pdfs