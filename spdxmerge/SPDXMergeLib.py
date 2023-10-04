from spdxmerge.SPDX_ShallowMerge import SPDX_ShallowMerger
from spdxmerge.SPDX_DeepMerge import SPDX_DeepMerger

def create_merged_spdx_document(doc_list, docnamespace, name, authortype, author,
                                email, merge_type, suppliertype, supplier):
    if merge_type == "deep":
        merger = SPDX_DeepMerger(doc_list, docnamespace, name, authortype, author,
                                 email, suppliertype, supplier)
    elif merge_type == "shallow":
        merger = SPDX_ShallowMerger(doc_list, docnamespace, name, authortype, author,
                                    email, suppliertype, supplier)
    return merger.create_document()
