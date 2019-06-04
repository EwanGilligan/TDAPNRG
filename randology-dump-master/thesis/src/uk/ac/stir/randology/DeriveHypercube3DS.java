package uk.ac.stir.randology;

import edu.stanford.math.plex4.api.Plex4;
import edu.stanford.math.plex4.homology.barcodes.BarcodeCollection;
import edu.stanford.math.plex4.homology.chain_basis.Simplex;
import edu.stanford.math.plex4.homology.interfaces.AbstractPersistenceAlgorithm;
import edu.stanford.math.plex4.metric.impl.EuclideanMetricSpace;
import edu.stanford.math.plex4.streams.impl.*;

import org.apache.commons.math3.stat.inference.*;

import uk.ac.stir.randology.generator.RNG;

/**
 * Unit Cube Homology Test
 * @author zak
 *
 */
@SuppressWarnings("unused")
public class DeriveHypercube3DS {
	
	//--- Test configuration ---//
	
	private int numberOfRuns = 5;
	private int numberOfPoints = 12000;
	private int dimension = 3;
	
	private double scale = 1.0; // for LFSR: 0.15, for Minstd: 0.045
	
	private double[] filtrationValues = {0.015*scale, 0.02*scale, 0.025*scale, 0.03*scale, 0.035*scale, 0.04*scale, 0.045*scale, 0.05*scale, 0.055*scale, 0.06*scale, 0.065*scale, 0.07*scale, 0.075*scale, 0.08*scale, 0.085*scale, 0.09*scale, 0.095*scale}; //{0.0175, 0.0350, 0.0525, 0.0700, 0.0875, 0.1050, 0.1060, 0.1234}; // {0.025, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.095};
	
	//--- Algorithm configuration ---//
	
	private int maximalSimplex = 1;
	AbstractPersistenceAlgorithm<Simplex> algorithm = Plex4.getDefaultSimplicialAlgorithm(maximalSimplex);
	
	//--- Implementation ---//
	
	
	private int getBetti(BarcodeCollection<Double> barcodes, double filter, int number) {
		return (barcodes.getBettiNumbersMap(filter).get(number) == null) ? 0 : barcodes.getBettiNumbersMap(filter).get(number);
	}
	
	private void testRun(RNG rng) {
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
			/*if (correct) {
				System.out.printf("%.2f %.2f %.2f\n",points[j][0], points[j][1], points[j][2]);
			}*/
			//if (correct) { System.out.print("."); if (j % 100 == 0) System.out.println(); }
			if(correct && j % 200 == 0) System.out.print("."); 
			if (correct) { j++; }
		}
		
		// 2. Create Vietoris-Rips complex
		EuclideanMetricSpace space = Plex4.createEuclideanMetricSpace(points);
		VietorisRipsStream<double[]> vrComplex = Plex4.createVietorisRipsStream(space, maximalSimplex, filtrationValues);
		vrComplex.finalizeStream();
		
		// 3. Compute Betti numbers
		BarcodeCollection<Double> barcodes = algorithm.computeIntervals(vrComplex);

		long[] observedValues = new long[filtrationValues.length];
		for (int i = 0; i < filtrationValues.length; i++) {
			observedValues[i] = getBetti(barcodes,filtrationValues[i],0);
			System.out.print(observedValues[i] + ",");
		}
		System.out.println( "x" );
	}
	
	public void perform() {
		System.out.println("Hypercube Test, d = 3, deriving phase START");
		
		// 1. Print csv header
    	for( double value : filtrationValues ) {
    		System.out.print(value + ",");
    	}
    	System.out.println("x");
    	
    	// 2. Perform runs
    	for( RNG rng : Generators.trngs ) {
    		for( int run = 0; run < numberOfRuns; run++ ) {
    			testRun(rng);
    		}
    	}

    	System.out.println("END");
	}
	
	public static void main(String[] args) {
		new DeriveHypercube3DS().perform();
	}
	
	
}
