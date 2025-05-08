from rich import print

from api import *


if __name__ == "__main__":
    # get static data
    # use dify knowledge api to update knowledge base

    # debug
    knowledge_base_list = get_knowledge_base_list()
    print(knowledge_base_list)
    # target_database_id = "d3fcb424-2901-4629-906c-52e21284b03e"
    # # get document id list
    # id_list = get_all_document_id_from_knowledge_base(target_database_id)
    # print(id_list)

    # # delete all
    # for id in id_list:
    #     delete_document(target_database_id, id)

    # # debug: create all files in crawler/MRE_root/housing/data/zh/news
    # path = "/Users/mac/ncku/GDSC3rd/ncku-chatbot/crawler/MRE_root/housing/data/zh/dorm-rules"
    # for file in os.listdir(path):
    #     result = create_document_from_file(
    #         dataset_id=target_database_id,
    #         file_path=f"{path}/{file}",
    #         name=file
    #     )
    #     print(result)

    # detail = get_knowledge_base_detail_by_id("7ce7860a-a505-4f9f-87bf-353d1ebefb37")
    # print(detail)
