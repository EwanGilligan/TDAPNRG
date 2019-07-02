from pyfinite import genericmatrix

# Wrapper class for GF2 matrix, with the minimal functionality required for the Matrix Rank test.
cdef class GF2Matrix:
    cdef int matrix_size
    cdef genericmatrix.GenericMatrix matrix
    cdef rank

    def __init__(self, matrix_size):
        self.matrix_size = matrix_size
        XOR = lambda x, y: x ^ y
        AND = lambda x, y: x & y
        DIV = lambda x, y: x
        self.matrix = genericmatrix.GenericMatrix((matrix_size, matrix_size), zeroElement=0, identityElement=1, add=XOR, mul=AND, sub=XOR, div=DIV)
        self.rank = None

    cdef int rank(self):
        if self.rank is not None:
            return self.rank
        self.matrix.LowerGaussianElim()
        rank = self.matrix.rows
        # Iterate over the rows in reverse order.
        for i in reversed(range(self.matrix.rows)):
            # If the row contains 1, then stop
            if 1 in self.matrix.GetRow(i):
                break
            # Otherwise the row is a zero row and so the rank is reduced by 1.
            rank -= 1
        self.rank = rank
        return rank

    def __add__(self, other):
        result = GF2Matrix(self.matrix_size)
        result.matrix = self.matrix + other.matrix
        return result

    cdef set_row(self, index, row_vector):
        self.matrix.SetRow(index, row_vector)

