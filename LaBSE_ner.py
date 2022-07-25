from transformers import pipeline
from termcolor import colored
import torch


class Ner_Extractor:
    """
    Labeling each token in sentence as named entity

    :param model_checkpoint: name or path to model 
    :type model_checkpoint: string
    """
    
    def __init__(self, model_checkpoint: str):
        self.token_pred_pipeline = pipeline("token-classification", 
                                            model=model_checkpoint, 
                                            aggregation_strategy="average")
    
    @staticmethod
    def text_color(txt, txt_c="blue", txt_hglt="on_yellow"):
        """
        Coloring part of text 
        
        :param txt: part of text from sentence 
        :type txt: string
        :param txt_c: text color  
        :type txt_c: string        
        :param txt_hglt: color of text highlighting  
        :type txt_hglt: string
        :return: string with color labeling
        :rtype: string
        """
        return colored(txt, txt_c, txt_hglt)
    
    @staticmethod
    def concat_entities(ner_result):
        """
        Concatenation entities from model output on grouped entities
        
        :param ner_result: output from model pipeline 
        :type ner_result: list
        :return: list of grouped entities with start - end position in text
        :rtype: list
        """
        entities = []
        prev_entity = None
        prev_end = 0
        for i in range(len(ner_result)):
            
            if (ner_result[i]["entity_group"] == prev_entity) &  (ner_result[i]["start"] == prev_end):
                
                entities[-1][2] = ner_result[i]["end"]
                prev_entity = ner_result[i]["entity_group"]
                prev_end = ner_result[i]["end"]
            else:
                entities.append([ner_result[i]["entity_group"], 
                                 ner_result[i]["start"], 
                                 ner_result[i]["end"]])
                prev_entity = ner_result[i]["entity_group"]
                prev_end = ner_result[i]["end"]
        
        return entities
    
    
    def colored_text(self, text: str, entities: list):
        """
        Highlighting in the text named entities
        
        :param text: sentence or a part of corpus
        :type text: string
        :param entities: concated entities on groups with start - end position in text
        :type entities: list
        :return: Highlighted sentence
        :rtype: string
        """
        colored_text = ""
        init_pos = 0
        for ent in entities:
            # print(f"ent: {ent}")
            if ent[1] > init_pos:
                colored_text += text[init_pos: ent[1]]
                # colored_text += self.text_color(text[ent[1]: ent[2]]) + f"({ent[0]})"
                colored_text +=  '<b>' + text[ent[1]: ent[2]] + '</b>' + f"({ent[0]})"
                init_pos = ent[2]
            else:
                colored_text += '<b>' + text[ent[1]: ent[2]] + '</b>' + f"({ent[0]})"
                init_pos = ent[2]
        
        return colored_text
    
    
    def get_entities(self, text: str):
        """
        Extracting entities from text with their position in text
        
        :param text: input sentence for preparing
        :type text: string
        :return: list with entities from text
        :rtype: list
        """
        assert len(text) > 0, text
        entities = self.token_pred_pipeline(text)
        concat_ent = self.concat_entities(entities)
        
        return concat_ent
    
    
    def show_ents_on_text(self, text: str):
        """
        Highlighting named entities in input text 
        
        :param text: input sentence for preparing
        :type text: string
        :return: Highlighting text
        :rtype: string
        """
        assert len(text) > 0, text
        entities = self.get_entities(text)        
                
        return self.colored_text(text, entities)

# seqs_example = ["После заявлений президента США Джо Байдена видно, что Белый дом не понимает «основную динамику рынка».",
#                 " Таким образом отреагировал на слова американского лидера основатель Amazon Джефф Безос.", 
#                 "Об этом он написал в своем Twitter"   ]

def ner_recognition(text):

    # init model for inference\
    extractor = Ner_Extractor(model_checkpoint = "surdan/LaBSE_ner_nerel")
    
    # get highlighting sentences\n
    show_entities_in_text = extractor.show_ents_on_text(text)

    # get list of entities from sentence\
    nl_entities = extractor.get_entities(text)
    # len(l_entities), len(seqs_example)

    return show_entities_in_text

    # ## print highlighting sentences
    # for i in range(len(text)):
    #     print(next(show_entities_in_text, "End of generator"))
    #     print("-*-"*25)

