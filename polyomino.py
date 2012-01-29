"""
Functions and classes that involve polyominoes.
"""
import functools as _ft

def generate(n):
    """
    Generate all n-ominoes.
    """
    if n == 0:
        return set()
    minos = {Polyomino([(0,0)])}
    for i in range(n-1):
        minos_new = set()
        for mino in minos:
            minos_new.update(mino.children())
        minos = minos_new
    return minos

def one_sided(minos, sort=True):
    """Remove rotations in set of minos."""
    vis = set()
    result = set()
    for mino in minos:
        if mino not in vis:
            vis.update(mino.rotations())
            result.add(max(mino.rotations(), key=mino_key) if sort else mino)
    return result

def free(minos, sort=True):
    """Remove rotations and reflections in the set of minos."""
    vis = set()
    result = set()
    for mino in minos:
        if mino not in vis:
            vis.update(mino.transforms())
            result.add(max(mino.transforms(), key=mino_key) if sort else mino)
    return result

# Internalize!
def mino_key(m):
    h, w = m.shape()
    
    return (len(m), h/w, sum(2**(i+j*w) for i, j in m))

def _neighbors(point):
    """
    Get left, right, upper, lower neighbors of this point.
    """
    i, j = point
    return {(i-1, j), (i+1, j), (i, j-1), (i, j+1)}

##@_ft.total_ordering
class Polyomino(frozenset):
    """
    Represent a fixed polyomino in space as a set of point tuples.
    """
    def grid(self):
        """Return boolean-grid representation of this polyomino."""
        h, w = self.shape()
        grid = [[False]*w for row in range(h)]
        for i, j in self:
            grid[i][j] = True
        return grid

    def __hash__(self):
        return super().__hash__()
    
    def __str__(self, cell="[]", empty="  "):
        """
        Pretty string of the polyomino.
        """
        grid = self.grid()
        result = []
        for row in grid:
            result.append("".join(cell if c else empty for c in row))
        return '\n'.join(result)

    def __eq__(self, other):
        """
        Equality to another mino.
        """
        return super().__eq__(other)
        
    def shape(self):
        """Width and height of a normalized mino"""
        rows, cols = zip(*self)
        return max(rows)+1, max(cols)+1

    def normalize(self):
        """
        Return a polyomino in normal form (min x,y is zero)
        """
        rows, cols = zip(*self)
        imin, jmin = min(rows), min(cols)
        return Polyomino((i-imin, j-jmin) for i, j in self)

    def translate(self, numrows, numcols):
        """Translate by numrows and numcols"""
        return Polyomino((i+numrows, j+numcols) for i, j in self)

    def rotate_left(self):
        """Rotate counterclockwise"""
        return Polyomino((-j, i) for i, j in self).normalize()

    def rotate_half(self):
        """Rotate 180 degrees"""
        return Polyomino((-i, -j) for i, j in self).normalize()
    
    def rotate_right(self):
        """Rotate clockwise"""
        return Polyomino((j, -i) for i, j in self).normalize()

    def reflect_vert(self):
        """Reflect vertically"""
        return Polyomino((-i, j) for i, j in self).normalize()

    def reflect_horiz(self):
        """Reflect horizontally"""
        return Polyomino((i, -j) for i, j in self).normalize()

    def reflect_diag(self):
        """Reflection across line i==j"""
        return Polyomino((j, i) for i, j in self).normalize()

    def reflect_skew(self):
        """Reflection across line i==-j"""
        return Polyomino((-j, -i) for i, j in self).normalize()

    def rotations(self):
        """Return rotations of this mino."""
        return [self,
                self.rotate_left(),
                self.rotate_half(),
                self.rotate_right()]

    def transforms(self):
        """Return transformations of this mino."""
        return [self,
                self.rotate_left(),
                self.rotate_half(),
                self.rotate_right(),
                self.reflect_vert(),
                self.reflect_horiz(),
                self.reflect_diag(),
                self.reflect_skew()]

    # TODO: more "pythonic" way of keeping track of symmetry?
    def symmetry(self):
        """
        Return the symmetry sigil of the polyomino.
        '?': No symmetries
        '|-\/': Reflective symmetry across axis
        '%': Twofold rotational symmetry
        '@': Fourfold rotational symmetry
        '+X': Twofold reflective symmetry
        'O': All symmetries
        """
        sym = ''
        if self == self.reflect_horiz():
            sym += '|'
        if self == self.reflect_vert():
            sym += '-'
        if self == self.reflect_diag():
            sym += '\\'
        if self == self.reflect_skew():
            sym += '/'
        if self == self.rotate_half():
            sym += '%'
        if self == self.rotate_left():
            sym += '@'
        if '|-' in sym:
            sym += '+'
        if '\\/' in sym:
            sym += 'X'
        if '@+X' in sym:
            sym += 'O'
        if not sym:
            sym = '?'
        return sym

    def children(self):
        """
        Returns all polyominoes obtained by adding a square to this one.
        """
        childset = set()
        for nbr in set.union(*(_neighbors(square) for square in self)):
            if nbr not in self:
                new = Polyomino(self | {nbr})
                # Only normalize if we need to
                if -1 in nbr:
                    new = new.normalize()
                childset.add(new)
        return childset
