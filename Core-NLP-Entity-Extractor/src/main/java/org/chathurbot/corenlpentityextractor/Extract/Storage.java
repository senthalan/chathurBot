package org.chathurbot.corenlpentityextractor.Extract;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

public class Storage {

  Set<String> models = new HashSet<>();
  Set<String> brands = new HashSet<>();
  Set<String> onlineStores = new HashSet<>();

  public void setStorage() {
    File file = new File("/home/mathuriga/CSE-ENG/FYP/chathurBotCoreNLP/chathurBot/Core-NLP-Entity-Extractor/data.txt");

    Storage storage = new Storage();
    try (BufferedReader br = new BufferedReader(new FileReader(file))) {
      String line;
      List<String> values;
      while ((line = br.readLine()) != null) {
        values = Arrays.asList(line.split("\\s*,\\s*"));

        String onlineStore = values.get(0).replace("(", "").replace("'", "").replace("http://", "");
        String brand = values.get(1).replace("'", "").replace(" ", "_");
        String model = values.get(2).replace("'", "").replace(" ", "_");

        if (!models.contains(model)) {
          models.add(model);
        }
        if (!brands.contains(brand)) {
          brands.add(brand);
        }
        if (!onlineStores.contains(onlineStore)) {
          onlineStores.add(onlineStore);
        }
      }
    } catch (IOException e) {
      e.printStackTrace();
    }
  }

//  public void setModel(String model) {
//    if (!models.contains(model)) {
//      models.add(model);
//    }
//  }
//
//  public void setBrand(String brand) {
//    if (!brands.contains(brand)) {
//      brands.add(brand);
//    }
//  }
//
//  public void setOnlineStore(String onlineStore) {
//    if (!onlineStores.contains(onlineStore)) {
//      onlineStores.add(onlineStore);
//    }
//  }

  public Set<String> getModels() {
    return models;
  }

  public Set<String> getBrands() {
    return brands;
  }

  public Set<String> getOnlineStores() {
    return onlineStores;
  }
}
