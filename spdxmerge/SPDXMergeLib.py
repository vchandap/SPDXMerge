from spdxmerge.SPDX_ShallowMerge import SPDX_ShallowMerger

def create_merged_spdx_document(doc_list, docnamespace, name, authortype, author,
                                email, merge_type, suppliertype, supplier):
    if merge_type == "deep":
        print("TODO")
    elif merge_type == "shallow":
        merger = SPDX_ShallowMerger(doc_list, docnamespace, name, authortype, author,
                                    email, suppliertype, supplier)
    return merger.create_document()
