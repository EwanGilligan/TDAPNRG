package uk.ac.stir.randology.generator;

public class QCG631 implements RNG {
	
	private long state;
	
	public QCG631(long seed) {
		state = seed % 4294967296L;
	};
	
	public long nextLong() {
		state = (6*state*state + 3*state + 1) % 4294967296L;
		return state;
	}
	
    public long next64bits() {
    	return nextLong();
    }
	
	public double nextDouble() {
	    return Math.abs( (double)nextLong() / 4294967296L );
	}
	
	@Override
	public String getName() {
		return "QCG631";
	}

}
