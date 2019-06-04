package uk.ac.stir.randology;

import org.apache.commons.math3.stat.inference.ChiSquareTest;

import edu.stanford.math.plex4.api.Plex4;
import edu.stanford.math.plex4.homology.barcodes.BarcodeCollection;
import edu.stanford.math.plex4.homology.chain_basis.Simplex;
import edu.stanford.math.plex4.homology.interfaces.AbstractPersistenceAlgorithm;
import edu.stanford.math.plex4.metric.impl.ExplicitMetricSpace;
import edu.stanford.math.plex4.streams.impl.*;

import uk.ac.stir.randology.generator.RNG;

/**
 * This experiment calculates Betti_1 numbers in bit-string space using the longest common subsequence metric.
 * @author zak
 *
 */
public class TestLCSH1 {
	
	//--- Test configuration ---//
	
	int numberOfRuns = 10;
	int numberOfPoints = 50;
	
	private double[] filtrationValues = { 9,10,11,12,13,14 };
	private double[] expectedValues = { 1, 2, 22, 17, 2, 1 };
	
	//--- Algorithm configuration ---//
	
	private int maximalSimplex = 3;
	AbstractPersistenceAlgorithm<Simplex> algorithm = Plex4.getDefaultSimplicialAlgorithm(maximalSimplex);
	
	private ChiSquareTest chi2 = new ChiSquareTest();
	
	//--- Implementation ---//
	
	class LCS {
		private Double[][] memo = new Double[64][64];
		
		private long arg1;
		private long arg2;
		
		public LCS(long arg1, long arg2) {
			this.arg1 = arg1;
			this.arg2 = arg2;
		}
		
		private double getMemo(int j, int k) {
			if ((j > 63) || (k > 63)) return 0;
			if (memo[j][k] != null) return memo[j][k];
			double result = (arg1 << j) <= 0 && (arg2 << k) <= 0 ? 1 + getMemo(j+1,k+1) :
				            (arg1 << j) >= 0 && (arg2 << k) >= 0 ? 1 + getMemo(j+1,k+1) :
				            Math.max(getMemo(j,k+1), getMemo(j+1,k));
			memo[j][k] = result;
			return result;
		}
		
		public double result() {
			double ret = getMemo(0,0);
			return ret;
		}
	}
	
	private int getBetti(BarcodeCollection<Double> barcodes, double filter, int number) {
		return (barcodes.getBettiNumbersMap(filter).get(number) == null) ?  0 : barcodes.getBettiNumbersMap(filter).get(number);
	}
	
	private double singleRun(RNG rng) {
		// 1. Generate points
		long[] points = new long[numberOfPoints];
		for(int j = 0; j < numberOfPoints; j++) { points[j] = rng.next64bits(); }
		
		double[][] distance = new double[numberOfPoints][numberOfPoints];
		
		for(int j = 0; j < numberOfPoints; j++) for(int k = 0; k < numberOfPoints; k++) {
			distance[j][k] = 64 - new LCS(points[j],points[k]).result();
		}
		
		// 2. Create Vietoris-Rips complex
		ExplicitMetricSpace space = new ExplicitMetricSpace(distance);
		VietorisRipsStream<Integer> vrComplex = Plex4.createVietorisRipsStream(space, maximalSimplex, filtrationValues);
		vrComplex.finalizeStream();
		
		// 3. Compute Betti numbers
		BarcodeCollection<Double> barcodes = algorithm.computeIntervals(vrComplex);
		long[] observedValues = new long[filtrationValues.length];
		for (int i = 9; i <= 14; i++) {
			observedValues[i-9] = 1+getBetti(barcodes,i,1);
			//System.out.print(observedValues[i-9] + " ");
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
