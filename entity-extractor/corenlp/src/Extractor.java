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

//    for (CoreMap entityMention : document.get(CoreAnnotations.MentionsAnnotation.class)) {
//      System.out.println(entityMention);
//      System.out.println(entityMention.get(CoreAnnotations.TextAnnotation.class));
//    }


  public Map getEntities(String question){
    Map<String, String> entities = new HashMap<String, String>();
    Properties props = new Properties();
    props.setProperty("annotators", "tokenize, ssplit, pos, lemma, ner, entitymentions");
    props.put("ner.model", "/home/abilashini/Desktop/corenlpextractor/ner-model.ser.gz");
    StanfordCoreNLP pipeline = new StanfordCoreNLP(props);
    Annotation document = new Annotation(question);

    pipeline.annotate(document);

    List<CoreMap> sentences = document.get(CoreAnnotations.MentionsAnnotation.class);
    for (CoreMap sentence : sentences) {
      for (CoreLabel token : sentence.get(TokensAnnotation.class)) {
        if (!token.get(NamedEntityTagAnnotation.class).equals("O")){
          entities.put(token.originalText(), token.ner());
        }
      }
    }
    return entities;
  }

}