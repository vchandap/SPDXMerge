from datetime import datetime
from spdx_tools.spdx.constants import DOCUMENT_SPDX_ID
from spdx_tools.spdx.model import (
    Actor,
    ActorType,
    Checksum,
    ChecksumAlgorithm,
    CreationInfo,
    Document,
    ExternalDocumentRef,
    ExternalPackageRef,
    ExternalPackageRefCategory,
    File,
    FileType,
    Package,
    PackagePurpose,
    PackageVerificationCode,
    Relationship,
    RelationshipType,
    SpdxNoAssertion,
)

class SPDX_ShallowMerger():
    def __init__(self,doc_list=None,docnamespace=None,name=None,author=None,email=None):
        self.doc_list = doc_list
        self.docnamespace = docnamespace
        self.name = name
        self.author = author
        self.emailaddr = email

    def create_document(self):
        external_references = []
        for idx, doc in enumerate(self.doc_list):
            check_sum = Checksum(ChecksumAlgorithm.SHA1,doc.comment)
            extDoc = ExternalDocumentRef(
                document_ref_id=doc.creation_info.spdx_id,
                document_uri=doc.creation_info.document_namespace,
                checksum=check_sum
            )
            external_references.append(extDoc)

        creation_info = CreationInfo(
            spdx_version="SPDX-2.3",
            spdx_id=DOCUMENT_SPDX_ID,
            name=self.name,
            data_license="CC0-1.0",
            document_namespace=self.docnamespace,
            external_document_refs=external_references,
            creators=[Actor(ActorType.PERSON, self.author, self.emailaddr)],
            created=datetime.now(),
        )
        master_doc = Document(creation_info)

        package = Package(
            spdx_id=f"SPDXRef-{self.name}-1.0",
            name=self.name,
            download_location=SpdxNoAssertion(),
        )
        package.version = "1.0"
        master_doc.packages = [package]

        return master_doc
