package uk.ac.stir.randology.generator;

/**
 * This generator returns points at uniform distance.
 * @author zak
 */
public class Uniform implements RNG {
	
	private int dimension;
	private double[] state;
	private int returnIndex = 0;
	private double stepSize;
	
	public Uniform(int steps, int dimension) {
		this.dimension = dimension;
		this.stepSize = 1/(double)steps;
		state = new double[dimension];
		for(int k = 0; k < dimension; k++) { state[k] = 0; }
	}
	
	private void advanceReturnIndex() {
		returnIndex = (returnIndex + 1) % dimension;
	}
	
	public String getName() {
		return "Uniform";
	}
	
	public long nextLong() {
		return Math.round(Long.MAX_VALUE*nextDouble());
	}
	
    public long next64bits() {
    	return nextLong();
    }
	
	public double nextDouble() {
		double ret = state[returnIndex];
		for( int k = 0; k < dimension; k++ ) {
			state[k] += stepSize;
			if (state[k] < 1) break;
			state[k] = 0;
		}
		advanceReturnIndex();
		return ret;
	}
	
}
