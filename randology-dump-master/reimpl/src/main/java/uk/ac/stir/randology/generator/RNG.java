package uk.ac.stir.randology.generator;

public interface RNG {
	
	public String getName();
	public long nextLong();
	public double nextDouble();
	
	public long next64bits();
}
