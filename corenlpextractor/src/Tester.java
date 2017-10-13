import edu.stanford.nlp.ie.crf.CRFClassifier;
import edu.stanford.nlp.ling.CoreLabel;
import edu.stanford.nlp.sequences.SeqClassifierFlags;
import edu.stanford.nlp.util.StringUtils;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.util.Arrays;
import java.util.List;
import java.util.Map;
import java.util.Properties;

public class Tester {
  public static void main(String[] args){
    Extractor extractor = new Extractor();
    Map<String, String> entities;

    File file = new File("/home/abilashini/Desktop/Link to Final Year Project/corenlpextractor/test-questions.txt");
    File outputFile = new File("/home/abilashini/Desktop/Link to Final Year Project/corenlpextractor/output-2-gram.txt");

    if (outputFile.exists()) {
      outputFile.delete();
    }
    try {
      outputFile.createNewFile();
    } catch (IOException e) {
      e.printStackTrace();
    }
    FileOutputStream fos = null;
    try {
      fos = new FileOutputStream(outputFile);
    } catch (FileNotFoundException e) {
      e.printStackTrace();
    }

    BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(fos));

    try (BufferedReader br = new BufferedReader(new FileReader(file))) {
      String question;
      while ((question = br.readLine()) != null) {
        bw.write(question);
        bw.newLine();
        entities = extractor.getEntities(question);

        Storage storage = new Storage();
        storage.setStorage();

        for (String entity: entities.keySet()){
          String word = null;
          String label = null;
          if (entities.get(entity).equals("BRAND")){
            if (storage.getBrands().contains(entity)) {
              word = entity.replace("_"," ");
              label = entities.get(entity);
            }
          } else if (entities.get(entity).equals("MODEL")) {
            if (storage.getModels().contains(entity)) {
              word = entity.replace("_"," ");
              label = entities.get(entity);
            }
          } else if (entities.get(entity).equals("ONLINE_STORE")) {
            if (storage.getOnlineStores().contains(entity)) {
              word = entity.replace("_"," ");
              label = entities.get(entity);
            }
          } else {
            word = entity.replace("_"," ");
            label = entities.get(entity);
            if (word.split(" ").length > 1) {
              word = null;
              label = null;
            }
            if (label == "NUMBER") {
              label = "MEMORY";
              if (word.charAt(0) == '.' || word.isEmpty()) {
                label = null;
              }
            }
          }
          if (word != null && label != null) {
            bw.write(word + " : " + label);
            bw.newLine();
          }
        }
        bw.newLine();
        bw.write("------------------------------------------------------------------");
        bw.newLine();
        bw.newLine();
      }
    } catch (IOException e) {
      e.printStackTrace();
    }
    try {
      bw.flush();
      bw.close();
    } catch (IOException e) {
      e.printStackTrace();
    }

  }
}
