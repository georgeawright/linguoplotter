(define size-concept
  (def-concept :name "size" :locations (list) :classifier None
    :instance_type Chunk :structure_type Label :parent_space None
    :distance_function centroid_euclidean_distance))
(define size-space
  (def-conceptual-space :name "size" :parent_concept size-concept
    :no_of_dimensions 1 :is_basic_level True))
(define large-concept
  (def-concept :name "large" :locations (list (Location (list (list 10)) size-space))
    :classifier (ProximityClassifier) :instance_type Chunk :structure_type Label
    :parent_space size-space :distance_function centroid_euclidean_distance))
(define small-concept
  (def-concept :name "small" :locations (list (Location (list (list 1)) size-space))
    :classifier (ProximityClassifier) :instance_type Chunk :structure_type Label
    :parent_space size-space :distance_function centroid_euclidean_distance))

(def-relation :start large-concept :end more-concept :parent_concept more-concept :activation 1.0)
(def-relation :start small-concept :end less-concept :parent_concept more-concept :activation 1.0)

(define large-word
  (def-letter-chunk :name "large" :parent_space size-space
    :locations (list (Location (list (list 10)) size-space))))
(def-relation :start large-concept :end large-word :parent_concept jj-concept)
(define larg-word
  (def-letter-chunk :name "larg" :parent_space size-space
    :locations (list (Location (list (list 10)) size-space))))
(def-relation :start large-concept :end larg-word :parent_concept jjr-concept)
(def-relation :start larg-word :end -er :parent_concept jjr-concept)
(define small-word
  (def-letter-chunk :name "small" :parent_space size-space
    :locations (list (Location (list (list 1)) size-space))))
(def-relation :start small-concept :end small-word :parent_concept jj-concept)
(def-relation :start small-concept :end small-word :parent_concept jjr-concept)
(def-relation :start small-word :end -er :parent_concept jjr-concept)