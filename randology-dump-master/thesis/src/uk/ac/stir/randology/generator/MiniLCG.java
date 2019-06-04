package uk.ac.stir.randology.generator;

public class MiniLCG extends LCG {
	public MiniLCG(long seed) {
		super("MiniLCG",61,2,256,seed);
	}
}