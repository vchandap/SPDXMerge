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
    def __init__(self,doc_list=None,docnamespace=None,name=None,authortype=None,author=None,
                 email=None,suppliertype=None, supplier=None):
        self.doc_list = doc_list
        self.docnamespace = docnamespace
        self.name = name
        self.authortype = authortype
        self.author = author
        self.emailaddr = email
        self.suppliertype = suppliertype
        self.supplier = supplier

    def create_document(self):
        if self.authortype in ["P", "p"]:
            creator=[Actor(ActorType.PERSON, self.author, self.emailaddr)]
        else:
            creator=[Actor(ActorType.ORGANIZATION, self.author, self.emailaddr)]

        external_references = []
        for idx, doc in enumerate(self.doc_list):
            check_sum = Checksum(ChecksumAlgorithm.SHA1,doc.comment)
            extDoc = ExternalDocumentRef(
                document_ref_id="DocumentRef-DOCUMENT-" + str(idx),
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
            creators=creator,
            created=datetime.now(),
        )
        master_doc = Document(creation_info)

        package = Package(
            spdx_id=f"SPDXRef-{self.name}-1.0",
            name=self.name,
            download_location=SpdxNoAssertion(),
        )
        package.version = "1.0"

        if self.suppliertype in ["P", "p"]:
            package.supplier = Actor(ActorType.PERSON, self.supplier, self.emailaddr)
        else:
            package.supplier = Actor(ActorType.ORGANIZATION, self.supplier, self.emailaddr)

        master_doc.packages = [package]

        master_doc.relationships = [Relationship(
            spdx_element_id="SPDXRef-DOCUMENT",
            relationship_type=RelationshipType.DESCRIBES,
            related_spdx_element_id=f"SPDXRef-{self.name}-1.0",
        )]

        return master_doc
