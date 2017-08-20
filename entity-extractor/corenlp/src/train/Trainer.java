package train;


import edu.stanford.nlp.ie.crf.CRFClassifier;
import edu.stanford.nlp.ling.CoreLabel;
import edu.stanford.nlp.sequences.SeqClassifierFlags;
import edu.stanford.nlp.util.StringUtils;
import java.util.Properties;

public class Trainer {
  public static void main(String[] args){

    Properties props = StringUtils.propFileToProperties("/home/abilashini/Desktop/Link to Final Year Project/corenlpextractor/properties.prop");
    SeqClassifierFlags flags = new SeqClassifierFlags(props);
    CRFClassifier<CoreLabel> crf = new CRFClassifier(flags);
    crf.train();
    crf.serializeClassifier("ner-model.ser.gz");
  }
}
