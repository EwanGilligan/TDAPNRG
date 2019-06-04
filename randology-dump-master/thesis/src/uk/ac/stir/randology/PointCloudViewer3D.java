package uk.ac.stir.randology;


import javax.swing.*;
import org.math.plot.*;

import uk.ac.stir.randology.generator.RNG;

public class PointCloudViewer3D {
	
	public String name;
	public int numberOfPoints = 5096; //4096;
	public double[][] points;
	
	public PointCloudViewer3D(String name, double[][] points) {
		this.name = name;
		this.points = points;
	}
	
	public PointCloudViewer3D(RNG rng) {
		this.points = new double[numberOfPoints][3];
		for( int j = 0; j < numberOfPoints; j++ ) for( int k = 0; k < 3; k++ ) {
			points[j][k] = rng.nextDouble();
		}
		this.name = rng.getName();
	}
	
    public void display() {
    
        double[] xs = new double[points.length];
        double[] ys = new double[points.length];
        double[] zs = new double[points.length];
        
        for(int k = 0; k < points.length; k++) {
        	xs[k] = points[k][0];
        	ys[k] = points[k][1];
        	zs[k] = points[k][2];
        }
        Plot3DPanel plot = new Plot3DPanel();
        plot.addLegend("SOUTH");
        plot.addScatterPlot(name, xs, ys, zs);
        
        JFrame frame = new JFrame("PlotApplet");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(600, 600);
        frame.setContentPane(plot);
        frame.setVisible(true);
        
   }
}
