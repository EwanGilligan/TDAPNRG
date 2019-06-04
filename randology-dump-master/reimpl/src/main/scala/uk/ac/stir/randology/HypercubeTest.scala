package uk.ac.stir.randology

import smile.stat.hypothesis.KSTest

import uk.ac.stir.randology.generator._
import uk.ac.stir.randology.EuclideanSpace._

/** The Unit Hypercube Homology Test.
 *
 *  The homology of a subcube with the given side length will be calculated.
 *  A smaller side length can detect lower-scale features, but will need
 *  to generate more numbers.
 *
 *  @param sampleSize The number of points to sample from the hypercube.
 *  @param cubeDimension The dimension the hypercube.
 *  @param homologyDimension The dimension of the largest simplex to consider.
 *  @param ref The [[uk.ac.stir.randology.generator.RNG]] used to estimate the
 *             reference distribution.
 *  @param subcubeSide The given side length.
 *  @param distributionSize The size of the compared distributions.
 */
case class HypercubeTest(
  sampleSize: Int,
  cubeDimension: Int,
  homologyDimension: Int,
  ref: RNG,
  subcubeSide: Double = 1.0,
  distributionSize: Int = 30
) {

  /** The filtration used by the test, covering all relevant scales. */  
  val filtration: Filtration = {
    if (homologyDimension == 0) {
      // a cube sample would be connected above this value with high probability
      val maxValue =
        subcubeSide *
        10.0 / Math.pow( sampleSize.toDouble, 1.0/cubeDimension.toDouble)
      Filtration.linear(0, maxValue, 20)
    } else Filtration.linear(0, subcubeSide/cubeDimension.toDouble, 20)
  }

  def getReferencePoint: Point = {
    val coords = for (x <- 1 to cubeDimension) yield (ref.nextDouble * subcubeSide)
    Point(coords)
  }

  def getReferencePoints: IndexedSeq[Point] =
    for (x <- 1 to sampleSize) yield getReferencePoint

  def getReferenceBarcode: Barcode = {
    val complex =
      RipsComplex(homologyDimension, getReferencePoints, filtration)
    complex.barcode(homologyDimension)
  }

  lazy val referenceDistribution: IndexedSeq[Double] = {
    val refs1 =
      for (x <- 1 to distributionSize) yield
      getReferenceBarcode
    val refs2 =
      for (x <- 1 to distributionSize) yield
      getReferenceBarcode
    for (b1 <- refs1; b2 <- refs2) yield getDistance(b1,b2)
  }

  def getCoordinate(rng: RNG): Double = {
    var result = rng.nextDouble
    while (result > subcubeSide) result = rng.nextDouble
    result
  }

  def getPoint(rng: RNG): Point = {
    val coords = for (x <- 1 to cubeDimension) yield getCoordinate(rng)
    Point(coords)
  }

  def getPoints(rng: RNG): IndexedSeq[Point] =
    for (x <- 1 to sampleSize) yield getPoint(rng)

  def getBarcode(rng: RNG): Barcode = {
    val complex =
      RipsComplex(homologyDimension, getPoints(rng), filtration)
    complex.barcode(homologyDimension)
  }

  def distribution(rng: RNG): IndexedSeq[Double] = {
    val refs =
      for (x <- 1 to distributionSize) yield
      getReferenceBarcode
    val rngs =
      for (x <- 1 to distributionSize) yield
      getBarcode(rng)
    for (b1 <- refs; b2 <- rngs) yield getDistance(b1,b2)
  }

  /** Returns the L^2 distance between the given barcodes, relative to the
   *  filtration used by the test.
   *
   *  @param barcode1 A given barcode.
   *  @param barcode2 Another given barcode.
   */
  def getDistance(barcode1: Barcode, barcode2: Barcode): Double = {
    val seq1: IndexedSeq[Int] = barcode1.bettiSequence(filtration)
    val seq2: IndexedSeq[Int] = barcode2.bettiSequence(filtration)
    val diff: Double = 
      (seq1,seq2).zipped.toIndexedSeq.map(p => Math.pow(p._1 - p._2, 2)).sum
    diff / filtration.values.length
  }

  /** Returns the p-value of the Hypercube Homology Test on the given generator. 
   *
   *  @param rng The given generator.
   */
  def perform(rng: RNG): Double = {
    val result = KSTest.test(
      referenceDistribution.toArray,
      distribution(rng).toArray
    )
    result.pvalue
  }
 
}
