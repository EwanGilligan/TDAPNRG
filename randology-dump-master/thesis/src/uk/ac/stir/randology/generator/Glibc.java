package uk.ac.stir.randology.generator;

import java.math.BigInteger;

public class Glibc extends LCG {
	public Glibc(long seed) {
		super("Glibc48",25214903917L,11,(new BigInteger("2")).pow(48).longValue(),seed);
	}
}
