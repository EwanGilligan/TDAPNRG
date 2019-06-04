package uk.ac.stir.randology

import edu.stanford.math.plex4.api.Plex4
import edu.stanford.math.plex4.homology.barcodes.BarcodeCollection
import edu.stanford.math.plex4.homology.chain_basis.Simplex
import edu.stanford.math.plex4.homology.interfaces.AbstractPersistenceAlgorithm
import edu.stanford.math.plex4.metric.impl.ExplicitMetricSpace
import edu.stanford.math.plex4.streams.impl._

import uk.ac.stir.randology.Metric._

/** A filtered Vietoris-Rips complex.
 *
 *  @param maximalDimension Dimension of the highest simplex in the complex.
 *  @param points The points (0-simplices) of this complex.
 *  @param filtration The filtration values of the complex.
 */
case class RipsComplex[T](
  maximalDimension: Int,
  points: IndexedSeq[T],
  filtration: Filtration
)(implicit metric: Metric[T]) {

  val distanceMatrix: Array[Array[Double]] =
    Array.tabulate (points.length, points.length) { (p,q) =>
      points(p).distance(points(q))
    }

  lazy val plexAlgorithm: AbstractPersistenceAlgorithm[Simplex] =
    Plex4.getDefaultSimplicialAlgorithm(maximalDimension + 1)

  lazy val plexSpace: ExplicitMetricSpace =
    new ExplicitMetricSpace(distanceMatrix)

  lazy val plexComplex: VietorisRipsStream[Integer] = {
    val result = Plex4.createVietorisRipsStream(
      plexSpace,
      maximalDimension + 1,
      filtration.values.toArray
    )
    result.finalizeStream
    result
  }

  lazy val plexBarcodes: BarcodeCollection[java.lang.Double] = {
    plexAlgorithm.computeIntervals(plexComplex)
  }

  def barcode(dimension: Int): Barcode = {
    require(
      dimension <= maximalDimension,
      "The dimension cannot exceed the maximal dimension of the complex"
    )
    val result = plexBarcodes.getIntervalsAtDimension(dimension)
    Barcode(result)
  }

}
