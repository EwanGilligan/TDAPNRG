package uk.ac.stir.randology.generator;

public class QCG981 implements RNG {
	
	private long state;
	
	// a = b-1
	// a = 9 (mod p)
	
	public QCG981(long seed) {
		state = seed % 4294967296L;
	};
	
	public long nextLong() {
		state = (10*state*state + 5*state + 1) % 4294967296L;
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
		return "QCG10-51";
	}

}
