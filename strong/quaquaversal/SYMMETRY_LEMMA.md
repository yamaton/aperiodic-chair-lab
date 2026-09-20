# Forced prism hierarchies imply a finite symmetry group

This is a conditional written lemma. It does **not** establish that any
candidate local rule forces a hierarchy. No Lean verification or external
review is claimed.

Suppose a tiling has, at every level n, a partition into supertiles whose
supports are congruent to 2^n P, where P is the quaquaversal prism. Suppose
also that every symmetry of the marked tiling preserves each of these
partitions. Unique recognizable grouping is one way to obtain this property.
Then the tiling's Euclidean symmetry group is finite, even if infinitely
many tile orientations occur and there are infinite-level boundary faults.

## Proof by packing

Let D be the diameter of P, let rho>0 be the radius of an interior ball of P,
and let h be the number of Euclidean self-isometries of P. Here D=sqrt(5),
rho=(sqrt(3)−1)/2 works, and h=2 for the unmarked scalene right prism.
Markings can only reduce the stabilizer.

Set K=ceil(((1+D+rho)/rho)^3). Suppose the symmetry group contained hK+1
distinct elements g_i. Choose a point x and let R=max_i |g_i x−x|. Choose
n so lambda=2^n >= max(1,R), and take any level-n supertile S containing x.

Every g_i S is a member of the same level-n partition and contains g_i x.
Its chosen inscribed ball has radius lambda*rho, its center is within
lambda*D of g_i x, and thus this ball lies inside the ball about x of radius
R+lambda*(D+rho). Distinct supertile supports have disjoint interiors, hence
these inscribed balls have disjoint interiors. Comparing volumes shows that
at most K distinct images g_i S are possible.

For any particular image S', at most h distinct g_i can map S to S': after
composing one fixed such map inversely, these maps give distinct Euclidean
self-isometries of the bounded polyhedron S. Thus the hK+1 selected elements
would give at most hK elements, a contradiction.

Consequently the whole symmetry group is finite. This excludes nonzero
translations and infinite-order screws. It also excludes infinite groups
of finite-order symmetries without requiring a separate crystallographic
group argument.

## Why the hypotheses matter

Merely displaying an infinite hierarchy is insufficient: the hierarchy must
be preserved by the symmetries being excluded. A periodic tiling can be
given an arbitrary nonperiodic grouping which its translations do not
preserve. Likewise, a rule that forces only one or finitely many grouping
levels does not satisfy the lemma.

The proof uses an interior ball for each supertile support, but does not
require x to lie deep inside any supertile. It therefore avoids assuming
that all hierarchy boundaries eventually disappear around a given point.
