/*
 * WordCount Map-Reduce example with binning
 * binning strategy is based on the magnitude of the wordcount
 *  # of occurrences 1-10 will be stored under result/10
 *  # of occurrences 11-100 will be stored under result/100
 *  similarly 1000, 10000, 100000, 1000000 will be there
 *  utilimately if occurrences exceeds 1 million,
 *  the results will be put into a directory named "toomany"
 *
 * Big Data Analytics, Hadoop Binning assignment
 * Due 03/07/2015
 *
 * Robert Wen (robert.wen@nyu.edu)
 * NetID: qw476
 * N12246277
 *
 */

import java.io.IOException;
import java.util.*;

import org.apache.hadoop.fs.Path;
import org.apache.hadoop.conf.*;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapred.*;
import org.apache.hadoop.util.*;
import org.apache.hadoop.mapred.lib.MultipleTextOutputFormat;

public class WordCountBinning {

  public static class Map extends MapReduceBase implements Mapper<LongWritable, Text, Text, IntWritable> {
    private final static IntWritable one = new IntWritable(1);
    private Text word = new Text();

    /* map class, just like the wordcount */
    public void map(LongWritable key, Text value, OutputCollector<Text, IntWritable> output, Reporter reporter) throws IOException {
      String line = value.toString();
      StringTokenizer tokenizer = new StringTokenizer(line);
      while (tokenizer.hasMoreTokens()) {
        word.set(tokenizer.nextToken());
        output.collect(word, one);
      }
    }
  }

  public static class Reduce extends MapReduceBase implements Reducer<Text, IntWritable, Text, IntWritable> {
    /* reduce class, just like the wordcount */
    public void reduce(Text key, Iterator<IntWritable> values, OutputCollector<Text, IntWritable> output, Reporter reporter) throws IOException {
      int sum = 0;
      while (values.hasNext()) {
        sum += values.next().get();
      }
      output.collect(key, new IntWritable(sum));
    }
  }

  public static class OrganizeByCountNumber extends MultipleTextOutputFormat<Text, IntWritable>
  {
    @Override
    protected String generateFileNameForKeyValue(Text key, IntWritable value, String name)
    {
      int wordcount = value.get();

      if (wordcount <= 10) {
        return "10/" + name;
      } else if (wordcount <= 100) {
        return "100/" + name;
      } else if (wordcount <= 1000) {
        return "1000/" + name;
      } else if (wordcount <= 10000) {
        return "10000/" + name;
      } else if (wordcount <= 100000) {
        return "100000/" + name;
      } else if (wordcount <= 1000000) {
        return "1000000/" + name;
      } else {
        return "toomany" + name;
      }
    }
  }

  public static void main(String[] args) throws Exception {
    JobConf conf = new JobConf(WordCountBinning.class);
    conf.setJobName("wordcluster");

    conf.setOutputKeyClass(Text.class);
    conf.setOutputValueClass(IntWritable.class);

    conf.setMapperClass(Map.class);
    conf.setCombinerClass(Reduce.class);
    conf.setReducerClass(Reduce.class);

    conf.setInputFormat(TextInputFormat.class);

    /* override the default TextOutputFormat class with self-defined class */
    conf.setOutputFormat(OrganizeByCountNumber.class);

    FileInputFormat.setInputPaths(conf, new Path(args[0]));
    FileOutputFormat.setOutputPath(conf, new Path(args[1]));

    JobClient.runJob(conf);
  }
}

