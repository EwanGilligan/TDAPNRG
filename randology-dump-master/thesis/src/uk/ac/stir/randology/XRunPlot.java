package uk.ac.stir.randology;


public class XRunPlot {
	
	public static void main(String[] args) {
		//PointCloudViewer2DOverlap plotApp = new PointCloudViewer2DOverlap( new uk.ac.stir.randology.generator.MiniQCG(0xDEAFBABEDEADBEEFL) );
		PointCloudViewer3DS plotApp = new PointCloudViewer3DS( new uk.ac.stir.randology.generator.QCG981(0xDEAFBABEDEADBEEFL) );
		
		plotApp.display();
	}
	
}
