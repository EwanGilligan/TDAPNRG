package uk.ac.stir.randology.test

import org.scalacheck.Properties
import org.scalacheck.Prop
import org.scalacheck.Prop.BooleanOperators
import org.scalacheck.Gen
import org.scalacheck.Gen.{oneOf, listOf, alphaStr, numChar}
import org.scalacheck.Arbitrary
import org.scalacheck.Arbitrary._

import uk.ac.stir.randology.Metric._
import uk.ac.stir.randology.EuclideanSpace._

import uk.ac.stir.randology.test.Generators._

object TestPoint extends Properties("EuclideanSpace.Point") {

  property("distance non-negative") = Prop.forAll { (p: Point, q: Point) =>
    p.distance(q) >= 0
  }

  property("distance indiscernible") = Prop.forAll { (p: Point) =>
    p.distance(p) == 0
  }

  property("distance symmetric") = Prop.forAll { (p: Point, q: Point) =>
    p.distance(q) == q.distance(p)
  }

  property("distance sub-additive") =
    Prop.forAll { (p: Point, q: Point, r: Point) =>
      p.distance(r) <= p.distance(q) + q.distance(r)
    }

}

