package uk.ac.stir.randology;

import edu.stanford.math.plex4.api.Plex4;
import edu.stanford.math.plex4.homology.barcodes.BarcodeCollection;
import edu.stanford.math.plex4.homology.chain_basis.Simplex;
import edu.stanford.math.plex4.homology.interfaces.AbstractPersistenceAlgorithm;
import edu.stanford.math.plex4.metric.impl.EuclideanMetricSpace;
import edu.stanford.math.plex4.streams.impl.*;

import java.util.LinkedList;

import org.apache.commons.math3.distribution.NormalDistribution;
import org.apache.commons.math3.stat.inference.*;

import uk.ac.stir.randology.generator.RNG;

/**
 * Unit Cube Homology Test
 * @author zak
 *
 */
@SuppressWarnings("unused")
public class DeriveHypercube7DSp {
	
	//--- Test configuration ---//
	
	private int numberOfRuns = 20;
	private int numberOfPoints = 12000;
	private int dimension = 7;
	
	private double scale = 0.2; // lowest so far: 0.02, for LFSR: 0.15, for Minstd: 0.045
	private double m = 4.0;
	private double[] filtrationValues = {0.015*scale*m, 0.02*scale*m, 0.025*scale*m, 0.03*scale*m, 0.035*scale*m, 0.04*scale*m, 0.045*scale*m, 0.05*scale*m, 0.055*scale*m, 0.06*scale*m, 0.065*scale*m };
	private double[] avg = { 11993,11971,11900,11724,11334,10558,9182,6983,3991,1690,595,185,52,15,4,2,2 };
    private double[] sdv = { 2,4,7,15,22,35,45,55,60,32,24,12,7,3,2,1,1 };
	
	//--- Algorithm configuration ---//
	
	private int maximalSimplex = 1;
	AbstractPersistenceAlgorithm<Simplex> algorithm = Plex4.getDefaultSimplicialAlgorithm(maximalSimplex);
	
	//--- Implementation ---//
	
	
	private int getBetti(BarcodeCollection<Double> barcodes, double filter, int number) {
		return (barcodes.getBettiNumbersMap(filter).get(number) == null) ? 0 : barcodes.getBettiNumbersMap(filter).get(number);
	}
	
	private double[] testRun(RNG rng) {
		// 1. Generate points
		double[][] points = new double[numberOfPoints][dimension];
		int j = 0;
		while (j < numberOfPoints) {
			for(int k = 0; k < dimension; k++) {
				points[j][k] = rng.nextDouble();
			}
			boolean correct = true;
			for(int k = 0; k < dimension; k++) {
				correct &= (points[j][k] < scale);
			}
			if(correct && j % 200 == 0) System.out.print("."); 
			if (correct) { j++; }
		}
		
		// 2. Create Vietoris-Rips complex
		EuclideanMetricSpace space = Plex4.createEuclideanMetricSpace(points);
		VietorisRipsStream<double[]> vrComplex = Plex4.createVietorisRipsStream(space, maximalSimplex, filtrationValues);
		vrComplex.finalizeStream();
		
		// 3. Compute Betti numbers
		BarcodeCollection<Double> barcodes = algorithm.computeIntervals(vrComplex);
		
		double[] scores = new double[filtrationValues.length];
		long[] observedValues = new long[filtrationValues.length];
		for (int i = 0; i < filtrationValues.length; i++) {
			observedValues[i] = getBetti(barcodes,filtrationValues[i],0);
			double z = (observedValues[i] - avg[i]) / sdv[i];
			scores[i] = z;
			System.out.printf("%.4f ", Math.abs(z));
		}
		System.out.println( "x" );
		
		return scores;
	}
	
	public void perform() {
		System.out.println("Hypercube Test, d = 7");
		
		double[][] scores = new double[filtrationValues.length][numberOfRuns];
		
		// 1. Print csv header
    	for( double value : filtrationValues ) {
    		System.out.print(value + ",");
    	}
    	System.out.println("x");
    	
    	// 2. Perform runs
    	for( RNG rng : Generators.fullTest ) {
    		System.out.println("\n" + rng.getName() + ":");
    		for( int run = 0; run < numberOfRuns; run++ ) {
    			double[] results = testRun(rng);
    			for( int fv = 0; fv < filtrationValues.length; fv++ ) {
    				scores[fv][run] = results[fv];
    			}
    		}
			for( int fv = 0; fv < filtrationValues.length-1; fv++ ) {
				KolmogorovSmirnovTest ks = new KolmogorovSmirnovTest();
				double pvalue = ks.kolmogorovSmirnovTest(new NormalDistribution(), scores[fv]);
				//System.out.printf("fv: %.4f, p: %.4f\n", filtrationValues[fv] ,pvalue);
				if (pvalue < 0.001) System.out.printf("FAILED interval %d with p=%.4f\n", fv, pvalue);
			}
    	}
    	System.out.println("END");
	}
	
	public static void main(String[] args) {
		new DeriveHypercube7DSp().perform();
	}
	
	
}
