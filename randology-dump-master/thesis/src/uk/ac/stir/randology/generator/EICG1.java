package uk.ac.stir.randology.generator;

public class EICG1 extends EIG {
	public EICG1(long seed) {
		super("EICG1",16807,1,2147483647L,seed);
	}
}
//48271
//2147483647
//(new BigInteger("2")).pow(31).longValue()