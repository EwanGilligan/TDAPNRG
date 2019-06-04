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
public class DeriveHypercube3D {
	
	//--- Test configuration ---//
	
	private int numberOfRuns = 10;
	private int numberOfPoints = 12000;
	private int dimension = 3;
	
	private double[] filtrationValues = {0.015, 0.02, 0.025, 0.03, 0.035, 0.04, 0.045, 0.05, 0.055, 0.06, 0.065, 0.07, 0.075, 0.08, 0.085, 0.09, 0.095}; //{0.0175, 0.0350, 0.0525, 0.0700, 0.0875, 0.1050, 0.1060, 0.1234}; // {0.025, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.095};
	
	//--- Algorithm configuration ---//
	
	private int maximalSimplex = 1;
	AbstractPersistenceAlgorithm<Simplex> algorithm = Plex4.getDefaultSimplicialAlgorithm(maximalSimplex);
	
	//--- Implementation ---//
	
	private void testRun(RNG rng) {
		// 1. Generate points
		double[][] points = new double[numberOfPoints][dimension];
		for(int j = 0; j < numberOfPoints; j++) for(int k = 0; k < dimension; k++) {
			points[j][k] = rng.nextDouble();
		}
		
		// 2. Create Vietoris-Rips complex
		EuclideanMetricSpace space = Plex4.createEuclideanMetricSpace(points);
		VietorisRipsStream<double[]> vrComplex = Plex4.createVietorisRipsStream(space, maximalSimplex, filtrationValues);
		vrComplex.finalizeStream();
		
		// 3. Compute Betti numbers
		BarcodeCollection<Double> barcodes = algorithm.computeIntervals(vrComplex);

		long[] observedValues = new long[filtrationValues.length];
		for (int i = 0; i < filtrationValues.length; i++) {
			observedValues[i] = barcodes.getBettiNumbersMap(filtrationValues[i]).get(0);
			System.out.print(observedValues[i] + ",");
		}
		System.out.println( "x" );
		/*for (int i = 1; i < filtrationValues.length-1; i++) {
			observedValues[i] = (barcodes.getBettiNumbersMap(filtrationValues[i]).get(1) == null) ? 0 : barcodes.getBettiNumbersMap(filtrationValues[i]).get(1);
			System.out.print(observedValues[i] + ",");
		}
    	System.out.println( "x" );
    	*/
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
		new DeriveHypercube3D().perform();
	}
	
	
}
