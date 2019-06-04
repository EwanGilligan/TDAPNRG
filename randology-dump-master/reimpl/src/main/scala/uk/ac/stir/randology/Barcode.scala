package uk.ac.stir.randology

import edu.stanford.math.plex4.api.Plex4
import edu.stanford.math.plex4.homology.barcodes
import edu.stanford.math.plex4.homology.barcodes.BarcodeCollection
import edu.stanford.math.plex4.homology.chain_basis.Simplex
import edu.stanford.math.plex4.homology.interfaces.AbstractPersistenceAlgorithm
import edu.stanford.math.plex4.metric.impl.ExplicitMetricSpace
import edu.stanford.math.plex4.streams.impl._

import edu.stanford.math.plex4.bottleneck.BottleneckDistance._


/** A persistent homology barcode. */
case class Barcode(
  plexBarcode: java.util.List[barcodes.Interval[java.lang.Double]]
) {
  val toList: List[Interval] = {
    import scala.collection.JavaConverters._
    plexBarcode.asScala.toList.map(Interval(_))
  }

  /** Returns the bottleneck distance between two diagrams.
   *
   *  @deprecated
   *  The JavaPlex bottleneck distance is suspect. Avoid until investigated!
   */
  def distance(that: Barcode): Double = {
    computeBottleneckDistance(this.plexBarcode, that.plexBarcode)
  }

  /** Returns a bound on the interleaving distance, approximated
   *  geometrically and normalized to be between 0 and 1.
   *
   *  This method rounds points to reference points. If the two barcodes
   *  contain different reference points, we get a bound on the interleaving
   *  distance.
   * 
   *  This approximation does not yield an exact metric
   *  (to retain symmetry, one would ensure that each index is modified
   *  exactly once).
   * 
   *  @param that the barcode to calculate the distance from
   */
  def idistance(that: Barcode): Double = {
    val theseAbsolute: List[Interval] = this.toList.filter(!_.isInfinite)
    val thoseAbsolute: List[Interval] = that.toList.filter(!_.isInfinite)
    val theseMax: Double = if (theseAbsolute.isEmpty) 1 else
      theseAbsolute.map(_.end).max
    val thoseMax: Double = if (thoseAbsolute.isEmpty) 1 else
      thoseAbsolute.map(_.end).max

    // normalize intervals to (0,1)
    val these = theseAbsolute.map { (i: Interval) =>
      Interval(i.start/theseMax, i.end/theseMax)
    }
    val those = thoseAbsolute.map { (i: Interval) =>
      Interval(i.start/thoseMax, i.end/thoseMax)
    }
    
    // try to prove that the best matching must have radius > 1/tolerance
    var done = false
    var tolerance: Int = 1
    while(!done && tolerance < 101) {
      val array: Array[Array[Boolean]] =
        Array.tabulate(tolerance+1, tolerance+1) { (r,c) => false }
      for (i <- these) {
        val r: Int = Math.floor(i.start*tolerance).toInt
        val c: Int = Math.floor(i.end*tolerance).toInt
        array(r)(c) = true
        //array(r)(c) + 1
      }
      for (i <- those) {
        val r: Int = Math.floor(i.start*tolerance).toInt
        val c: Int = Math.floor(i.end*tolerance).toInt
        array(r)(c) = false
      }
      done = !array.forall(x => x.forall(_ == false))
      //if (done) println(array.toIndexedSeq.map(_.toIndexedSeq) mkString "\n")
      tolerance = tolerance + 1
    }
    if (tolerance >= 101) 0 else 1/tolerance.toDouble
  }

  /** Returns the number of intervals in the barcode containing the
   *  filtration values in the given filtration.
   *
   *  @param filtration The given filtration.
   */
  def bettiSequence(filtration: Filtration): IndexedSeq[Int] = {
    filtration.values.map(x => toList.count(_.contains(x)))
  }

  /** The total number of intervals (with multiplicity) in the barcode. */
  val bettiNumber: Int = plexBarcode.size

}

object Barcode {
  /** Returns a [[uk.ac.stir.randology.Barcode]] consisting of the intervals in
   *  the given list. 
   *
   *  The given list must be non-empty (this is a JavaPlex limitation).
   *
   *  @param fromList The given list of intervals.
   */
  def apply(fromList: List[Interval]): Barcode = {
    require(!fromList.isEmpty, "JavaPlex does not allow empty barcodes")
    val plexBarcode: java.util.List[barcodes.Interval[java.lang.Double]] = {
      import scala.collection.JavaConverters._
      fromList.map(_.plexInterval).asJava
    }
    Barcode(plexBarcode)
  }
}
