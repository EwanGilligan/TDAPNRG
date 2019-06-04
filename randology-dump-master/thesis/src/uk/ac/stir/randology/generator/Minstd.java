package uk.ac.stir.randology.generator;

public class Minstd extends LCG {
	public Minstd(long seed) {
		super("Minstd",16807,0,2147483647L,seed);
	}
}
//16807
//48271
//2147483647
//(new BigInteger("2")).pow(31).longValue()