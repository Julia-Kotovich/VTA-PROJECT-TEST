import os
from django.apps import AppConfig
from transformers import BertTokenizer, BertForQuestionAnswering
from QA_VTA.qa_vta import VTA

class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    tokenizer = None
    model = None
    model_path = None
    context_path = None
    model_root_dir = os.path.abspath('./vta_qa_model')
    capstone_qa_vta = None

    if os.path.exists(model_root_dir):
        model_path = os.path.abspath('./VTA-tools/models/mistral-7b-instruct-v0.2.Q4_K_M.gguf')
        tokenizer = BertTokenizer.from_pretrained(model_path, local_files_only=True)
        context_path = os.path.abspath('./vta_qa_model/training/newdataset/vista.json')
        model = BertForQuestionAnswering.from_pretrained(model_path, local_files_only=True)
    else:
        print(f"Directory: {model_root_dir} does not exist")

    def ready(self):
        self.capstone_qa_vta = VTA(self.model, self.tokenizer, self.context_path)
