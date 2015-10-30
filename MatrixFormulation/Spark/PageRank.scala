import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._
import org.apache.spark.SparkConf
import org.apache.spark.rdd.RDD
import scala.collection.mutable.ArraySeq

//Distributed Version of Page Rank Algorithm in spark using scala
object PageRank {

        def main(args: Array[String]) {
                 
                 //create Spark Context
                 val conf = new SparkConf().setAppName("Simple Application").set("spark.storage.memoryFraction","0.25").set("spark.driver.maxResultSize","0")
                 val sc = new SparkContext(conf)

                 val dataRDD = sc.textFile("../Graph/web-Google.txt")

		 //Number of Iterations
                 val iters = 100
                 
                 //Beta value for random walk through one edge
                 val beta = 0.8
           
                 //Directed Edges
                 val links = dataRDD.map{ s => val parts = s.split("\\t");(parts(0),parts(1))}.distinct().groupByKey().cache()

                 //Number of unique nodes in data
		 val nodes = dataRDD.flatMap(line => for(index <- 0 until line.split("\\t").length) yield line.split("\\t")(index)).distinct()

                 //Count of number of unique nodes
		 val numberOfNodes = nodes.count()
                 
                 //Initialize rank of each node to 1/numberOfUniqueNodes
                 var ranks = nodes.map(x => (x.toString,(x.toString,1.0/numberOfNodes)))

                 //Iterative calculation of Page Rank
                 for (i <- 1 to iters) {
                      //Contribution from each node to its directed edges
		      val contribs = ranks.leftOuterJoin(links).values.flatMap{ case (rank,urls) =>
				var deadEnd : ArraySeq[String] = ArraySeq()
				var calUrls = urls.getOrElse(deadEnd).asInstanceOf[Seq[String]]
				var isEmpty : Boolean = false        
				val size = calUrls.size
				var result = Array((rank._1,0.0))
				for( index <- 0 until calUrls.size) yield { result = result ++ Array((calUrls(index), rank._2/size)) }
				result            
		        }
                      //Summing up each contribution for each node and adding contribution of random teleportation
		      ranks = contribs.reduceByKey(_ + _).map(x => (x._1,(x._1,(1-beta)/numberOfNodes + beta*x._2)))
		      //Sum of all Page Ranks is 1. so adding the leaking page rank to each node
                      val rankSum = ranks.values.map(x => x._2).reduce(_+_)
		      ranks = ranks.mapValues(v => (v._1,v._2 + (1-rankSum)/numberOfNodes))
		} 

                //Page Rank of one particular node with name 99
                val result = ranks.filter(x => x._1 == "99").map(x => x._2._2)

                println("Page Rank for Node with name 99 is " + result.collect().mkString(","))


       }
}


