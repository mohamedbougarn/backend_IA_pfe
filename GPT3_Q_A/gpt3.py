import os
import openai


api="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"




class GPT3:


    def __init__(self):
        pass


    #todo define :method that use GPT3 for questin responce in CLASS named GPT3
    def get_gpt3aq(self,text):
        openai.api_key=api

        start_sequence = "\nA:"
        restart_sequence = "\n\nQ: "

        response = openai.Completion.create(
            engine="text-davinci-001",
            prompt=text,
            temperature=0.7,
            max_tokens=170,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6
        )
        content = response.choices[0].text.split('.')
        # print(content)
        return response.choices[0].text



    # todo define :method that use GPT3 for for transtalte in language  to laguage     in CLASS named GPT3

    def get_gpt3_translate(self, text, lang):

        openai.api_key = api


        response = openai.Completion.create(
            engine="text-davinci-001",
            prompt="Translate this into 1."+lang+" \n " + text+" \n 1.",
            temperature=0.3,
            max_tokens=170,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
            )
        content = response.choices[0].text.split('.')
        # print(content)
        return response.choices[0].text