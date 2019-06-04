package uk.ac.stir.randology.generator;

// Ranmar from RngPack
public class Ranmar implements RNG {
	
	double c,cd,cm,u[],uvec[] ;
	int i97,j97 ;
	
	public static int BIG_PRIME=899999963;
	
	
	public Ranmar(long ijkl)
	{
		initialize((int) Math.abs(ijkl % BIG_PRIME));
	};
	
	
	void initialize(int ijkl)
	{
	
		int ij,kl;
		int i,ii,j,jj,k,l,m ;
		double s,t ;
	
		u = new double[97];
	        uvec = new double[97];
	
	
		ij=ijkl/30082;
		kl=ijkl-30082*ij;
	
		i = ((ij/177) % 177) + 2 ;
		j = (ij % 177) + 2 ;
		k = ((kl/169) % 178) + 1 ;
		l = kl % 169 ;
		for (ii=0; ii<97; ii++)
			{
		 	s = 0.0 ;
			t = 0.5 ;
			for (jj=0; jj<24; jj++)
				{
				m = (((i*j) % 179) * k) % 179 ;
				i = j ;
				j = k ;
				k = m ;
				l = (53*l + 1) % 169 ;
				if ( ((l*m) % 64) >= 32) s += t ;
				t *= 0.5 ;
			}
			u[ii] = s ;
		}
		c   =  362436.0 / 16777216.0 ;
		cd  = 7654321.0 / 16777216.0 ;
		cm  =16777213.0 / 16777216.0 ;
		i97 = 96 ;
		j97 = 32 ;
	
	};
	
	
	public double nextDouble() {
		double uni;
	
		uni=u[i97]-u[j97];
		if (uni<0.0) uni+=1.0;
		u[i97]=uni;
		if (--i97<0) i97=96;
		if (--j97<0) j97=96;
		c-=cd;
		if (c<0.0) c+=cm;
		uni-=c;
		if (uni<0.0) uni+=1.0;
		return(uni);
	}
	
	public long nextLong() {
		return Math.round( Long.MAX_VALUE*nextDouble() );
	}
	
    public long next64bits() {
    	throw new UnsupportedOperationException("Ranmar does not support bit output");
    }
	
	@Override
	public String getName() {
		return "Ranmar";
	};
	

};
