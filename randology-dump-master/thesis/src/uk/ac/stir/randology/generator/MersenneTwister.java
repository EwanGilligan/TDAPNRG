package uk.ac.stir.randology.generator;

/**
 * Wraps Sean Luke's Mersenne Twister implementation in an RNG. 
 * @author zak
 */
public class MersenneTwister implements RNG {
	
	private MersenneImpl rng;
	
	public MersenneTwister(long seed) {
		rng = new MersenneImpl(seed);
	}
	
	public String getName() {
		return "MersenneTwister";
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
