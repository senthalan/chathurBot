
package org.chathurbot.corenlpentityextractor;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import javax.ws.rs.DELETE;
import javax.ws.rs.GET;
import javax.ws.rs.POST;
import javax.ws.rs.PUT;
import javax.ws.rs.Path;
import javax.ws.rs.QueryParam;
import org.json.simple.JSONObject;
import org.chathurbot.corenlpentityextractor.Extract.*;

@Path("/entity")
public class Service {
    @GET
    @Path("/extract")
    public JSONObject get(@QueryParam("question") String question) {
        // TODO: Implementation for HTTP GET request
      Extractor extractor = new Extractor();
      Storage storage = new Storage();
      storage.setStorage();

      Service service = new Service();

      Map entities = extractor.getEntities(question);
      JSONObject result = new JSONObject();

      for (Object entity: entities.keySet()) {
        String word = (String) entity;
        String label = (String) entities.get(entity);
        if (Objects.equals(label, "NUMBER")) {
          label = "MEMORY";
          if (service.isValid(word)) {
            if (!result.containsKey(label)) {
              List<String> memory = new ArrayList<>();
              memory.add(word);
              result.put(label, memory);
            } else {
              List<String> memory = (ArrayList<String>) result.get(label);
              memory.add(word);
              result.put(label,memory);
            }
          }
        } else if (label.equals("BRAND")){
            if (storage.getBrands().contains(word)) {
              word = word.replace("_"," ");
              result.put(label, word);
            }
          } else if (label.equals("MODEL")) {
            if (storage.getModels().contains(word)) {
              word = word.replace("_"," ");
              result.put(label, word);
            }
          } else if (label.equals("ONLINE_STORE")) {
            if (storage.getOnlineStores().contains(entity)) {
              word = word.replace("_"," ");
              result.put(label, word);
            }
          } else if (label.equals("PRICE")) {
          if (!result.containsKey(label)) {
              List<String> price = new ArrayList<>();
              price.add(word);
              result.put(label, price);
            } else {
              List<String> price = (ArrayList<String>) result.get(label);
              price.add(word);
              result.put(label,price);
            }
          } else {
            result.put(label, word);
          }
        }

        return result;
    }

    boolean isValid(String word){
      boolean isValid = false;
      try {
        Double.parseDouble(word);
        isValid = true;
        if (word.charAt(0) == '.' || word.isEmpty()) {
          isValid = false;
        }
      } catch (NumberFormatException e) {

      }
      return isValid;
    }

    @POST
    @Path("/")
    public void post() {
        // TODO: Implementation for HTTP POST request
        System.out.println("POST invoked");

    }

    @PUT
    @Path("/")
    public void put() {
        // TODO: Implementation for HTTP PUT request
        System.out.println("PUT invoked");

    }

    @DELETE
    @Path("/")
    public void delete() {
        // TODO: Implementation for HTTP DELETE request
        System.out.println("DELETE invoked");
    }
}
