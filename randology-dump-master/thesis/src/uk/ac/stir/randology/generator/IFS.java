package uk.ac.stir.randology.generator;

// Elsherbeny-Rahal Iterated Function System
public class IFS implements RNG {
	
	private double state;
	
	public long nextLong() {
		return 0;
	}
	
    public long next64bits() {
    	return nextLong();
    }
	
	public double nextDouble() {
	    double q = 1.605 * state;
	    double s = Math.cos(q)-Math.sin(q);
	    double s1 = Math.tan(q + 1.605/2);
		state = 1.3304*Math.abs(s) / (0.344 + Math.abs(s1));
		System.out.println(state);
		return state;
	}
	
	@Override
	public String getName() {
		return "IFS";
	}

}
