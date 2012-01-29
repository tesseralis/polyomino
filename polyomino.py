"""
Functions and classes that involve polyominoes.
"""
import functools as _ft

def generate(n):
    """
    Generate the fixed n-ominoes.
    """
    # There are no 'nilominoes', thus, empty set
    if n == 0:
        return set()
    # The one monomino
    minos = {Polyomino([(0,0)])}
    # Iteratively add the children of the members of the set before it
    for i in range(n-1):
        minos = childset(minos)
    return minos

def childset(minos):
    """Return the set of children of the collection of polyominoes."""
    children = set()
    for mino in minos:
        children.update(mino.children())
    return children

def one_sided(minos, sort=True):
    """Remove rotations in set of minos."""
    vis = set() # visited mino rotation families
    result = set()
    for mino in minos:
        # If we haven't seen a rotation of this mino before,
        # add its rotations to the visisted list
        if mino not in vis:
            mino_rots = mino.rotations()
            vis.update(mino_rots)
            # Add the (maximal rotation of the) mino
            result.add(max(mino_rots, key=mino_key) if sort else mino)
    return result

def free(minos, sort=True):
    """Remove rotations and reflections in the set of minos."""
    vis = set() # visited transformation families
    result = set()
    for mino in minos:
        # If we haven't seen a rotation or reflection of this mino before,
        # add its transforms to the visisted list
        if mino not in vis:
            mino_trans = mino.transforms()
            vis.update(mino_trans)
            # Add the (maximal transform of the) mino
            result.add(max(mino_trans, key=mino_key) if sort else mino)
    return result

## TODO: Figure out how to have the same effect WITHIN the class
## using __eq__, __gt__, __lt__, etc
def mino_key(m):
    """Generate a standard key for a polyomino"""
    #Sort the mino by order, then shape, then 'closeness to top'
    h, w = m.shape
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
        # Create a blank grid in the shape of the mino
        h, w = self.shape
        grid = [[False]*w for row in range(h)]
        # Fill the grid with the values in the mino
        for i, j in self:
            grid[i][j] = True
        return grid

    def __hash__(self):
        # Just inherit superclass's hashing
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

    # [properties]
    # TODO: Make O(1), pre-storage?
    @property
    def shape(self):
        """Width and height of a normalized mino"""
        rows, cols = zip(*self)
        return max(rows)+1, max(cols)+1
    @property
    def width(self):
        return self.shape[1]
    @property
    def height(self):
        return self.shape[0]

    # [transformations]
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
        return Polyomino((j, i) for i, j in self)

    def reflect_skew(self):
        """Reflection across line i==-j"""
        return Polyomino((-j, -i) for i, j in self).normalize()

    # [Congruent polyominoes]
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
        # Get all the neighbors of all the cells
        nbrs = set()
        for square in self:
            nbrs.update(_neighbors(square))
        nbrs -= self
        # Add each neighbor
        for nbr in nbrs:
            new = Polyomino(self | {nbr})
            # Only normalize if we need to
            if nbr[0] == -1:
                new = new.translate(1, 0)
            elif nbr[1] == -1:
                new = new.translate(0, 1)
            childset.add(new)
        return childset
