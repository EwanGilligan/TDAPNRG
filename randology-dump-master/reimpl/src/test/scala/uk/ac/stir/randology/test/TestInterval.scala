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

import uk.ac.stir.randology.test.Generators._

object TestInterval extends Properties("Interval") {

  property("\b(start,end) yields the appropriate interval") =
    Prop.forAll { (start: Double, length: Double) =>
      val xs = Math.abs(start)
      val xe = xs + Math.abs(length) + 1
      val i: Interval = Interval(xs,xe)
      val result = i.start == xs && i.end == xe
      if(!result) { println(xs,xe); println(i.start,i.end); println }
      result
    }

}
