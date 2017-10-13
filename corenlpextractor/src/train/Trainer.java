package train;


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
import java.io.PrintWriter;
import java.io.UnsupportedEncodingException;
import java.util.Arrays;
import java.util.List;
import java.util.Properties;

public class Trainer {
  public static void main(String[] args){
    File file = new File("/home/abilashini/Desktop/Link to Final Year Project/corenlpextractor/data.txt");
    File trainingDataFileAll= new File("/home/abilashini/Desktop/Link to Final Year Project/corenlpextractor/training-data.tsv");

    FileOutputStream fileOutputStreamAll = null;
    try {
      fileOutputStreamAll = new FileOutputStream(trainingDataFileAll);
    } catch (FileNotFoundException e) {
      e.printStackTrace();
    }

    BufferedWriter bufferedWriterAll = new BufferedWriter(new OutputStreamWriter(fileOutputStreamAll));

    try (BufferedReader br = new BufferedReader(new FileReader(file))) {
      String line;
      List<String> values;
      while ((line = br.readLine()) != null) {
        values = Arrays.asList(line.split("\\s*,\\s*"));
        bufferedWriterAll.write(values.get(0).replace("(" , "").replace("'", "").replace("http://", "") + "  " + "ONLINE_STORE");
        bufferedWriterAll.newLine();
        bufferedWriterAll.write(values.get(1).replace("'", "").replace(" ", "_") + "  " + "BRAND");
        bufferedWriterAll.newLine();
        bufferedWriterAll.write(values.get(2).replace("'", "").replace(" ", "_") + "  " + "MODEL");
        bufferedWriterAll.newLine();
        bufferedWriterAll.write("RS" + values.get(3).replace("'", "") + "  " + "PRICE");
        bufferedWriterAll.newLine();
        bufferedWriterAll.write(values.get(4).replace(")", "").replace("'", "") + "  " + "NUMBER");
        bufferedWriterAll.newLine();
      }
      bufferedWriterAll.close();
    } catch (IOException e) {
      e.printStackTrace();
    }

    Properties props = StringUtils.propFileToProperties("/home/abilashini/Desktop/Link to Final Year Project/corenlpextractor/properties.prop");
    SeqClassifierFlags flags = new SeqClassifierFlags(props);
    CRFClassifier<CoreLabel> crf = new CRFClassifier(flags);
    crf.train();
    crf.serializeClassifier("ner-model.ser.gz");
  }
}
