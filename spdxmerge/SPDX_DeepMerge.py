from datetime import datetime
from spdx_tools.spdx.document_utils import create_document_without_duplicates
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
    Snippet,
    SpdxNoAssertion,
)

class SPDX_DeepMerger():

    def __init__(self,doc_list=None,docnamespace=None,name=None,authortype=None,author=None,
                 email=None,suppliertype=None,supplier=None):
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

        creation_info = CreationInfo(
            spdx_version="SPDX-2.3",
            spdx_id="SPDXRef-DOCUMENT",
            name=self.name,
            data_license="CC0-1.0",
            document_namespace=self.docnamespace,
            creators=creator,
            created=datetime.now(),
        )

        master_doc = Document(creation_info)

        for doc in self.doc_list:
            for doc_package in doc.packages:
                 if doc_package not in master_doc.packages:
                     master_doc.packages.extend([doc_package])
        for doc in self.doc_list:
            master_doc.extracted_licensing_info.extend(doc.extracted_licensing_info)

        for doc in self.doc_list:
            master_doc.files.extend(doc.files)  #TODO Need to check this its not returning list

        for doc in self.doc_list:
            master_doc.snippets.extend(doc.snippets)

        for doc in self.doc_list:
             #relationship = Relationship(master_doc.creation_info.spdx_id, RelationshipType.DESCRIBES, doc.creation_info.spdx_id)
             master_doc.relationships.extend(doc.relationships)

        for doc in self.doc_list:
            master_doc.annotations.extend(doc.annotations)

        return master_doc
