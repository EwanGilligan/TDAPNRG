package uk.ac.stir.randology.test

import org.scalacheck.Properties
import org.scalacheck.Prop
import org.scalacheck.Prop.BooleanOperators
import org.scalacheck.Gen
import org.scalacheck.Gen.{oneOf, listOf, alphaStr, numChar}

import uk.ac.stir.randology.EuclideanSpace._
import uk.ac.stir.randology.Metric._
import uk.ac.stir.randology.RipsComplex
import uk.ac.stir.randology.Filtration
import uk.ac.stir.randology.test.Generators._

object TestRipsComplex extends Properties("RipsComplex") {

  property("distanceMatrix agrees with metric") =
    Prop.forAll { (complex: RipsComplex[Point]) =>
      val m = complex.distanceMatrix
      val agrees =
        for (x <- m.indices; y <- m(x).indices)
        yield m(x)(y) == complex.points(x).distance(complex.points(y))
      agrees.forall(_ == true)
    }

  property("barcode(1).bettiNumber is n for n circles") =
    Prop.forAll(genCircles) { case (expected, points) =>
      val filtration = Filtration(IndexedSeq(1.0, 1.1))
      val complex = RipsComplex(1, points, filtration)
      complex.barcode(1).bettiNumber == expected
    }

}
