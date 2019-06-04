package uk.ac.stir.randology.generator;

import java.math.BigInteger;

public class Randu extends LCG {
	public Randu(long seed) {
		super("Randu",65539,0,(new BigInteger("2")).pow(31).longValue(),seed);
	}
}
