package uk.ac.stir.randology

import uk.ac.stir.randology.Metric._

object EuclideanSpace {

  /** A point in Euclidean space. */
  case class Point(coordinates: IndexedSeq[Double])

  /** The standard Euclidean metric on points. */
  implicit val euclideanMetric: Metric[Point] = new Metric[Point] {
    override def distance(a: Point, b: Point): Double = {
      val diff = (a.coordinates, b.coordinates).zipped.map { (a1,b1) =>
        Math.abs(a1 - b1)
      }
      Math.sqrt(diff.sum)
    }
  }

}

