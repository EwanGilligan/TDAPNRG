package uk.ac.stir.randology.generator;

public class JavaRandom implements RNG {
	
	private java.util.Random rng;
	
	public JavaRandom(long seed) {
		rng = new java.util.Random(seed);
	}
	
	public String getName() {
		return "java.util.Random";
	}
	
	public long nextLong() {
		return rng.nextLong();
	}
	
    public long next64bits() {
    	return nextLong();
    }
	
	public double nextDouble() {
		return rng.nextDouble();
	}
	
}
