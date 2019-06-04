package uk.ac.stir.randology.generator;

// This quadratic generator is from Webkit2, see https://gist.github.com/Protonk/5367430
public class Webkit2 implements RNG {

	private long state;
	
	
	public Webkit2(long seed) {
		state = seed;
	}
	
	public long nextLong() {
		state += (state * state) ^ 5;
		return Math.abs(state);
	}
	
    public long next64bits() {
    	return nextLong();
    }
	
	public double nextDouble() {
	    return Math.abs( (double)nextLong() / Long.MAX_VALUE );
	}
	
	@Override
	public String getName() {
		return "Webkit2";
	}

}
