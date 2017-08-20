import java.util.Map;

public class Main {
  public static void main(String[] args){
    Extractor extractor = new Extractor();
    Map<String, String> entities;

    String question = "What is the highest cost phone in Huawei?";
    entities = extractor.getEntities(question);

    for (String entity: entities.keySet()){
      System.out.println(entity + " : " + entities.get(entity));
    }
  }
}
