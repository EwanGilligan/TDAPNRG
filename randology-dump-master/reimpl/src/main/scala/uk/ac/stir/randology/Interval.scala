package uk.ac.stir.randology

import edu.stanford.math.plex4.api.Plex4
import edu.stanford.math.plex4.homology.barcodes
import edu.stanford.math.plex4.homology.barcodes.BarcodeCollection
import edu.stanford.math.plex4.homology.chain_basis.Simplex
import edu.stanford.math.plex4.homology.interfaces.AbstractPersistenceAlgorithm
import edu.stanford.math.plex4.metric.impl.ExplicitMetricSpace
import edu.stanford.math.plex4.streams.impl._

/** A left-closed persistence interval. */
case class Interval(
  plexInterval: barcodes.Interval[java.lang.Double]
) {

  /** The left endpoint of the interval. May be infinite. */
  val start: Double =
    if (plexInterval.isLeftInfinite) Double.NegativeInfinity
    else plexInterval.getStart

 /** The right endpoint of the interval. May be infinite. */
  val end: Double =
    if (plexInterval.isRightInfinite) Double.PositiveInfinity
    else plexInterval.getEnd

 /** True iff. one of the endpoints is infinite. */
  val isInfinite: Boolean =
    plexInterval.isLeftInfinite || plexInterval.isRightInfinite

  /** Returns true if the given value is contained in the persistence
   *  interval.
   */
  def contains(value: Double): Boolean =
    start <= value && value < end

}

object Interval {

  /** Returns an [[uk.ac.stir.randology.Interval]] with the given left and
   *  right endpoints.
   *
   *  Both endpoints may be infinite, but the left endpoint must be less
   *  than the right endpoint.
   * 
   *  @param start The given left endpoint.
   *  @param end The given right endpoint.
   */
  def apply(start: Double, end: Double): Interval = {
    require(start <= end, "The interval must be non-degenerate")
    val xs = new java.lang.Double(start)
    val xe = new java.lang.Double(end)
    val result: barcodes.Interval[java.lang.Double] =
      (start.isInfinite, end.isInfinite) match {
        case (true, true) =>
          barcodes.Interval.makeInterval(null, null, false, true, true, true)
        case (true, false) =>
          barcodes.Interval.makeLeftInfiniteRightOpenInterval(xe)
        case (false, true) =>
          barcodes.Interval.makeRightInfiniteRightOpenInterval(xs)
        case (false, false) =>
          barcodes.Interval.makeFiniteRightOpenInterval(xs,xe)
      }
    Interval(result)
  }

}
