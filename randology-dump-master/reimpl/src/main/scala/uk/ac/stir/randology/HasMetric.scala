package uk.ac.stir.randology

import scala.language.implicitConversions

object Metric {

  /** A distance metric defined on the given type. 
   *
   *  @tparam T The given type.
   */
  trait Metric[T] {
    /** Returns the distance between the given objects 
     *
     *  Contract:
     *  1. distance(a,b) >= 0 with equality iff. a == b
     *  2. distance(a,b) == distance(b,a)
     *  3. distance(a,b) + distance(b,c) >= distance(a,c)
     *
     *  @param a The first given object.
     *  @param b The second given object.
     */
    def distance(a: T, b: T): Double
  }

  case class WithMetric[T](a: T)(implicit metric: Metric[T]) {
    def distance(b: T): Double = metric.distance(a,b)
  }

  implicit def withMetric[T](a: T)(implicit metric: Metric[T]):
    WithMetric[T] = WithMetric(a)

}

