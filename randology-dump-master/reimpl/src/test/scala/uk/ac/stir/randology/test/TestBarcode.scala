package uk.ac.stir.randology.test

import org.scalacheck.Properties
import org.scalacheck.Prop
import org.scalacheck.Prop.BooleanOperators
import org.scalacheck.Gen
import org.scalacheck.Gen.{oneOf, listOf, alphaStr, numChar}

import uk.ac.stir.randology.EuclideanSpace._
import uk.ac.stir.randology.Metric._
import uk.ac.stir.randology.RipsComplex
import uk.ac.stir.randology.Interval
import uk.ac.stir.randology.Barcode

import uk.ac.stir.randology.test.Generators._

object TestBarcode extends Properties("Barcode") {

  property("distance non-negative") = Prop.forAll { (p: Barcode, q: Barcode) =>
    p.distance(q) >= 0
  }

  property("distance indiscernible") = Prop.forAll { (p: Barcode) =>
    p.distance(p) == 0
  }

  property("distance symmetric") = Prop.forAll { (p: Barcode, q: Barcode) =>
    p.distance(q) == q.distance(p)
  }

  property("distance sub-additive") =
    Prop.forAll { (p: Barcode, q: Barcode, r: Barcode) =>
      p.distance(r) <= p.distance(q) + q.distance(r)
    }

  property("idistance non-negative") = Prop.forAll { (p: Barcode, q: Barcode) =>
    p.idistance(q) >= 0
  }

  property("idistance indiscernible") = Prop.forAll { (p: Barcode) =>
    p.idistance(p) == 0
  }

  property("idistance sub-additive") =
    Prop.forAll { (p: Barcode, q: Barcode, r: Barcode) =>
      p.idistance(r) <= p.idistance(q) + q.idistance(r)
    }

  property("bettiNumber is the number of intervals") =
    Prop.forAll { (p: Barcode) =>
      p.bettiNumber == p.toList.length
    }

}
