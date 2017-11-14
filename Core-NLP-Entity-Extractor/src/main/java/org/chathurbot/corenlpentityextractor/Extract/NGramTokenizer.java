package org.chathurbot.corenlpentityextractor.Extract;

import java.io.IOException;
import java.io.Reader;
import java.io.StringReader;
import org.apache.lucene.analysis.TokenStream;
import org.apache.lucene.analysis.shingle.ShingleFilter;
import org.apache.lucene.analysis.standard.StandardFilter;
import org.apache.lucene.analysis.standard.StandardTokenizer;
import org.apache.lucene.analysis.tokenattributes.CharTermAttribute;
import org.apache.lucene.util.Version;

public class NGramTokenizer {

  public String tokenize(String question) {

    Reader reader = new StringReader(question);
    StandardTokenizer source = new StandardTokenizer(reader);
    TokenStream tokenStream = new StandardFilter(source);
    ShingleFilter shingleFilter = new ShingleFilter(tokenStream, 2, 2);

    CharTermAttribute charTermAttribute = shingleFilter.addAttribute(CharTermAttribute.class);
    StringBuilder stringBuilder = new StringBuilder();

    try {
      shingleFilter.reset();
      while (shingleFilter.incrementToken()) {
        String string = charTermAttribute.toString();
        stringBuilder.append(string.replace(" ", "_"));
        stringBuilder.append(" ");
      }
    } catch (IOException e) {
      e.printStackTrace();
    }

    return stringBuilder.toString();
  }
}
