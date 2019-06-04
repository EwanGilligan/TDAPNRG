package uk.ac.stir.randology.generator;

// XorShift64 is due to Marsaglia http://www.jstatsoft.org/article/view/v008i14
// it passes all of DieHard
public class MiniXor implements RNG {
	
	private long state;
	
	public MiniXor(long seed) {
		state = seed;
	};
	
	public long nextLong() {
		state ^= (state << 7);
		state ^= (state >> 5);
		state ^= (state << 3);
		return state;
	}
	
    public long next64bits() {
    	return nextLong() % 256;
    }
	
	public double nextDouble() {
	    return Math.abs( (double)nextLong() / 256 );
	}
	
	@Override
	public String getName() {
		return "MiniXor";
	}

}
