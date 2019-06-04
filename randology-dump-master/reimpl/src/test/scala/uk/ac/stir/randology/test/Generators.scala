package uk.ac.stir.randology.test

import org.scalacheck.Gen
import org.scalacheck.Gen.{oneOf, listOf, alphaStr, numChar}
import org.scalacheck.Arbitrary
import org.scalacheck.Arbitrary._

import uk.ac.stir.randology.EuclideanSpace._
import uk.ac.stir.randology.Filtration
import uk.ac.stir.randology.RipsComplex
import uk.ac.stir.randology.Interval
import uk.ac.stir.randology.Barcode

object Generators {

  def genPoint: Gen[Point] = Gen.sized { size =>
    for (
      list <- Gen.listOfN(size, Gen.choose(-1.0, 1.0))
    ) yield Point(list.toIndexedSeq)
  }
  implicit def arbPoint: Arbitrary[Point] = Arbitrary(genPoint)

  def genFiltration: Gen[Filtration] = Gen.sized { size =>
    for( xs <- Gen.listOfN(size+2, arbitrary[Double]) )
    yield Filtration(xs.sorted.toIndexedSeq)
  }
  implicit def arbFiltration: Arbitrary[Filtration] = Arbitrary(genFiltration)

  def genRipsComplex: Gen[RipsComplex[Point]] = Gen.sized { size =>
    for(
      points <- Gen.listOfN(size+1, genPoint);
      filtration <- genFiltration
    ) yield RipsComplex(3, points.toIndexedSeq, filtration)
  }
  implicit def arbRipsComplex: Arbitrary[RipsComplex[Point]] =
    Arbitrary(genRipsComplex)

  def genSmallRipsComplex: Gen[RipsComplex[Point]] =
    for(
      points <- Gen.listOfN(10, genPoint);
      filtration <- genFiltration
    ) yield RipsComplex(3, points.toIndexedSeq, filtration)

  def genInterval: Gen[Interval] =
    for (
      start <- arbitrary[Double];
      length <- arbitrary[Double]
    ) yield Interval(Math.abs(start), Math.abs(start) + Math.abs(length) + 1)
  implicit def arbInterval: Arbitrary[Interval] = Arbitrary(genInterval)

  def genBarcode: Gen[Barcode] = Gen.sized { size =>
    val limited = Math.min(size + 1, 10) // otherwise, tests would take > 200s
    for (
      list <- Gen.listOfN(limited, genInterval)
    ) yield Barcode(list)
  }
  implicit def arbBarcode: Arbitrary[Barcode] = Arbitrary(genBarcode)

  def genCircles: Gen[(Int, IndexedSeq[Point])] =
  for (number <- Gen.choose(1,10)) yield {
    def circleAround(n: Int): IndexedSeq[Point] = IndexedSeq(
      Point(IndexedSeq(n, n)),
      Point(IndexedSeq(n+1,n)),
      Point(IndexedSeq(n+1,n+1)),
      Point(IndexedSeq(n,n+1))
    )
    (number, (1 to number).flatMap(circleAround))
  }

}
