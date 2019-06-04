package uk.ac.stir.randology.test

import org.scalacheck.Properties
import org.scalacheck.Prop
import org.scalacheck.Prop.BooleanOperators
import org.scalacheck.Gen
import org.scalacheck.Gen.{oneOf, listOf, alphaStr, numChar}

import uk.ac.stir.randology.Filtration

import uk.ac.stir.randology.test.Generators._

object TestFiltration extends Properties("Filtration") {

  property("linear has correct length") =
    Prop.forAll(Gen.choose(2,100)) { (steps: Int) =>
      Filtration.linear(0.0,1.0, steps).values.length == steps
    }

}
