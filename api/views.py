from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import deepl
from easygoogletranslate import EasyGoogleTranslate
from groq import Groq
from .s_key import openai_key, groq_key, deepl_key
from openai import OpenAI


class textApiView(APIView):
    groq_ai = Groq(api_key=groq_key)
    translator_deepl = deepl.Translator(deepl_key)
    google_translator = EasyGoogleTranslate()
    openai_translator = OpenAI(api_key=openai_key)

    def groq_translate(self, to_translate, target_lang_name):
        chat_completion = self.groq_ai.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f'give me the translation for phrase {to_translate} to {target_lang_name}. Please, give me the most commonly used variant. Dont write anything except pure translation please',
                }
            ],
            model="llama3-8b-8192",
        )
        return chat_completion.choices[0].message.content

    def deepl_translate(self, to_translate, target_lang_code):
        return self.translator_deepl.translate_text(to_translate, target_lang=target_lang_code).text

    def google_translate(self, to_translate, target_lang_code):
        return self.google_translator.translate(to_translate, target_language=target_lang_code.lower())

    def gpt_translate(self, to_translate, target_lang_name):
        chat_completion = self.openai_translator.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f'give me the translation for phrase {to_translate} to {target_lang_name}. Please, give me the most commonly used variant. Dont write anything except pure translation',
                }
            ],
            model="gpt-3.5-turbo",
        )
        # print(chat_completion.choices[0].message.content)
        return chat_completion.choices[0].message.content

    def post(self, request):
        data = request.data
        to_translate = data.get("to_translate")
        target_lang_code = data.get("target_lang_code")
        target_lang_name = data.get("target_lang_name")

        print(f'{to_translate =}', f'{target_lang_code = }', f'{target_lang_name =}')

        if to_translate == "":
            return Response({"translation": "",
                             "groq_translation": "",
                             "gpt_translation": "Disabled",
                             "deepl_translation": "Disabled", }, status=status.HTTP_200_OK)

        value = {
            "translation": self.google_translate(to_translate, target_lang_code),
            "groq_translation": self.groq_translate(to_translate, target_lang_name),
            # "gpt_translation": self.gpt_translate(to_translate, target_lang_name),
            "gpt_translation": "Disabled",
            # "deepl_translation": self.deepl_translate(to_translate, target_lang_code),
            "deepl_translation": "Disabled",
        }
        response = Response(value, status=status.HTTP_200_OK)
        return response
