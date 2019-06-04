package uk.ac.stir.randology.experiments

import uk.ac.stir.randology.generator._
import uk.ac.stir.randology.HypercubeTest

object Experiment1 {
  val ref: RNG = new FromBinaryFile("res/TrueRandom2", 100000)
  
  val seed1: Int = 0x4f771942
  val seed2: Int = 0xa31323c8
  
  val generators: List[RNG] = List(
    new FromBinaryFile("res/TrueRandom3", 100000),
    new FromBinaryFile("res/TrueRandom4", 100000),
    new FromBinaryFile("res/TrueRandom5", 100000),
    new Randu(seed1),
    new Randu(seed2),
    new GameRand(seed1),
    new GameRand(seed2)
  )

  val test: HypercubeTest = HypercubeTest(
    sampleSize = 300,
    cubeDimension = 3,
    homologyDimension = 0,
    ref
  )

  def main(args: Array[String]): Unit = {
    for (rng <- generators) {
      println("Running " + test)
      println(" on " + rng.getName)
      val result = test.perform(rng)
      println("p: " + result)
      println(if (result < 0.01) "FAILED\n" else "passed\n")
    }
  }

}
