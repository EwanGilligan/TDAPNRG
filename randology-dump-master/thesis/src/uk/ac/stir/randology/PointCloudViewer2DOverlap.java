package uk.ac.stir.randology;


import javax.swing.*;
import org.math.plot.*;

import uk.ac.stir.randology.generator.RNG;

public class PointCloudViewer2DOverlap {
	
	public String name;
	public int numberOfPoints = 256;
	public double[] points;
	
	public PointCloudViewer2DOverlap(RNG rng) {
		this.points = new double[numberOfPoints*2];
		for( int j = 0; j < numberOfPoints*2 ; j++ ) {
			points[j] = rng.nextDouble();
		}
	}
	
    public void display() {
    
        double[] xs = new double[points.length];
        double[] ys = new double[points.length];
        
        for(int k = 0; k < numberOfPoints; k++) {
        	xs[k] = points[k+0];
        	ys[k] = points[k+1];
        	k++;
        }
        
        Plot2DPanel plot = new Plot2DPanel();
        plot.addLegend("SOUTH");
        plot.addScatterPlot(name, xs, ys);
        
        JFrame frame = new JFrame("PlotApplet");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(600, 600);
        frame.setContentPane(plot);
        frame.setVisible(true);
        
   }
}
