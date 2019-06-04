package uk.ac.stir.randology.generator;

// XorShift64 is due to Marsaglia http://www.jstatsoft.org/article/view/v008i14
// it passes all of DieHard
public class XorShift64 implements RNG {
	
	private long state;
	
	public XorShift64(long seed) {
		state = seed;
	};
	
	public long nextLong() {
		state ^= (state << 21);
		state ^= (state >>> 35);
		state ^= (state << 4);
		return state;
	}
	
    public long next64bits() {
    	return nextLong();
    }
	
	public double nextDouble() {
	    return Math.abs( (double)nextLong() / Long.MAX_VALUE );
	}
	
	@Override
	public String getName() {
		return "XorShift";
	}

}
