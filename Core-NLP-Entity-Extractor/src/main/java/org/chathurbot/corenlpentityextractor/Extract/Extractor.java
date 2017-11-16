package org.chathurbot.corenlpentityextractor.Extract;

import edu.stanford.nlp.ling.CoreAnnotations;
import edu.stanford.nlp.ling.CoreAnnotations.NamedEntityTagAnnotation;
import edu.stanford.nlp.ling.CoreAnnotations.SentencesAnnotation;
import edu.stanford.nlp.ling.CoreAnnotations.TokensAnnotation;
import edu.stanford.nlp.ling.CoreLabel;
import edu.stanford.nlp.pipeline.*;
import edu.stanford.nlp.util.ArrayMap;
import edu.stanford.nlp.util.CoreMap;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Properties;

public class Extractor {

  public Map getEntities(String question){
    Map<String, String> entities = new HashMap<>();
    Properties props1 = new Properties();
    props1.setProperty("annotators", "tokenize, ssplit, pos, lemma, ner, entitymentions");
    props1.put("ner.model", "/home/senthalan/project/fyp/new/chathurBot/Core-NLP-Entity-Extractor/resources/ner-single-word-entities.ser.gz");
    StanfordCoreNLP pipelineAll = new StanfordCoreNLP(props1);

    Properties props2 = new Properties();
    props2.setProperty("annotators", "tokenize, ssplit, pos, lemma, ner, entitymentions");
    props2.put("ner.model", "/home/senthalan/project/fyp/new/chathurBot/Core-NLP-Entity-Extractor/resources/ner-multiple-word-entities.ser.gz");
    StanfordCoreNLP pipelineModel = new StanfordCoreNLP(props2);

    NGramTokenizer tokenizer = new NGramTokenizer();
    String wordCombinations = tokenizer.tokenize(question);

    Annotation singleWordEntities = new Annotation(question);
    pipelineAll.annotate(singleWordEntities);
    Annotation multiWordEntities = new Annotation(wordCombinations);
    pipelineModel.annotate(multiWordEntities);

    Storage storage = new Storage();
    storage.setStorage();

    List<CoreMap> sentences2 = multiWordEntities.get(CoreAnnotations.MentionsAnnotation.class);
    for (CoreMap sentence : sentences2) {
      for (CoreLabel token : sentence.get(TokensAnnotation.class)) {
        if (!token.get(NamedEntityTagAnnotation.class).equals("O")) {
          if (token.ner().equals("MODEL") && storage.getModels().contains(token.originalText())) {
            entities.put(token.originalText(), token.ner());
          }
          if (token.ner().equals("RANK") && storage.getRank().contains(token.originalText())) {
            entities.put(token.originalText(), token.ner());
          }
        }
      }
    }

    List<CoreMap> sentences1 = singleWordEntities.get(CoreAnnotations.MentionsAnnotation.class);
    for (CoreMap sentence : sentences1) {
      for (CoreLabel token : sentence.get(TokensAnnotation.class)) {
        if (!token.get(NamedEntityTagAnnotation.class).equals("O")) {
          entities.put(token.originalText(), token.ner());
        }
      }
    }


    return entities;
  }
}