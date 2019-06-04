package uk.ac.stir.randology

/** A list of filtration values. */
case class Filtration(values: IndexedSeq[Double]) {
  require(
    values.sorted == values,
    "The filtration values must be in ascending order"
  )
  require(
    values.length > 1,
    "The filtration must not be empty"
  )
}

object Filtration {
  /** Returns a filtration with the given number of elements, starting and
   *  ending near a given value.
   *
   *  The filtration is constructed via linear interpolation.
   *
   *  @param start The value at which the filtration starts.
   *  @param end The value at which the filtration ends.
   *  @param steps The number of values in the filtration.
   */
  def linear(start: Double, end: Double, steps: Int): Filtration = {
    require(end > start, "The filtration must end after it starts")
    require(steps > 0, "The filtration must have at least one step")
    val stepSize: Double = (end - start)/steps
    Filtration { (0 until steps).map(s => stepSize*s + start) }
  }
}
