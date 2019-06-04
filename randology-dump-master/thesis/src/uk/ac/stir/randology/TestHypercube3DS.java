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
public class TestHypercube3DS {
	
	//--- Test configuration ---//
	
	private int numberOfRuns = 10;
	private int numberOfPoints = 12000;
	private int dimension = 3;
	
	private double scale = 0.05;//0.045;
	
	private double[] filtrationValues = {0.015*scale, 0.02*scale, 0.025*scale, 0.03*scale, 0.035*scale, 0.04*scale, 0.045*scale, 0.05*scale, 0.055*scale, 0.06*scale, 0.065*scale, 0.07*scale, 0.075*scale, 0.08*scale, 0.085*scale, 0.09*scale, 0.095*scale};
	private double[] expectedValues = { 9782, 7938, 5639, 3164, 1142, 304, 77, 19, 5, 2, 1, 1, 1, 1, 1, 1, 1 };
	
	
	//--- Algorithm configuration ---//
	
	private int maximalSimplex = 1;
	AbstractPersistenceAlgorithm<Simplex> algorithm = Plex4.getDefaultSimplicialAlgorithm(maximalSimplex);
	
	private ChiSquareTest chi2 = new ChiSquareTest();
	
	//--- Implementation ---//
	
	/**
	 * 
	 * @param rng The RNG to use for the run
	 * @return the Chi^2 value
	 */
	private double singleRun(RNG rng) {
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
			observedValues[i] = barcodes.getBettiNumbersMap(filtrationValues[i]).get(0);
			//System.out.print(observedValues[i] + " ");
		}
		
		// 4. Return chi^2 test result
		double result = chi2.chiSquareTest(expectedValues, observedValues);
		//System.out.printf("%.3f\n",result);
		return result;
	}
	
	public int performTest(RNG rng) {
		int passes = 0;
		for( int i = 0; i < numberOfRuns; i++ ) {
			if (singleRun(rng) > 0.01) passes++;
		}
		return passes;
	}
	
}
