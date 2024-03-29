(define more-less-concept
  (def-concept :name "more-less" :locations (list) :classifier None :instance_type Chunk
    :structure_type Relation :parent_space None
    :distance_function centroid_euclidean_distance))
(define more-less-space
  (def-conceptual-space :name "more-less" :parent_concept more-less-concept
    :no_of_dimensions 1))
(define more-concept
  (def-concept :name "more" :locations (list (Location (list (list 1)) more-less-space))
    :classifier (DifferenceClassifier 1) :instance_type Chunk :structure_type Relation
    :parent_space more-less-space :distance_function centroid_euclidean_distance))
(define less-concept
  (def-concept :name "less" :locations (list (Location (list (list -1)) more-less-space))
    :classifier (DifferenceClassifier -1) :instance_type Chunk :structure_type Relation
    :parent_space more-less-space :distance_function centroid_euclidean_distance))
(setattr more-concept "reverse" less-concept)
(setattr less-concept "reverse" more-concept)
(define most-concept
  (def-concept :name "most" :locations (list (Location (list (list 1)) more-less-space))
    :classifier (MostClassifier) :instance_type Chunk :structure_type Label
    :parent_space more-less-space :distance_function centroid_euclidean_distance))
(define least-concept
  (def-concept :name "least" :locations (list (Location (list (list -1)) more-less-space))
    :classifier (LeastClassifier) :instance_type Chunk :structure_type Label
    :parent_space more-less-space :distance_function centroid_euclidean_distance))
(define first-concept
  (def-concept :name "first" :locations (list (Location (list (list 1)) more-less-space))
    :classifier (FirstWordOfTypeClassifier) :instance_type Chunk :structure_type Label
    :parent_space more-less-space :distance_function centroid_euclidean_distance))
(define last-concept
  (def-concept :name "last" :locations (list (Location (list (list 1)) more-less-space))
    :classifier (LastWordOfTypeClassifier) :instance_type Chunk :structure_type Label
    :parent_space more-less-space :distance_function centroid_euclidean_distance))

(def-relation :start more-concept :end more-concept :parent_concept more-concept :quality 1.0)
(def-relation :start less-concept :end less-concept :parent_concept more-concept :quality 1.0)

(define more-word (def-letter-chunk :name "more" :locations (list)))
(def-relation :start more-concept :end more-word :parent_concept jj-concept)
(define less-word (def-letter-chunk :name "less" :locations (list)))
(def-relation :start less-concept :end less-word :parent_concept jj-concept)

(define increase-word
  (def-letter-chunk :name "increase" :parent_space grammar-space
    :locations (list vb-location increase-location)))
(def-relation :start more-concept :end increase-word :parent_concept vb-concept)
(define decrease-word
  (def-letter-chunk :name "decrease" :parent_space grammar-space
    :locations (list vb-location decrease-location)))
(def-relation :start less-concept :end decrease-word :parent_concept vb-concept)
(def-relation :start increase-word :end decrease-word :parent_concept opposite-concept)
(def-relation :start decrease-word :end increase-word :parent_concept opposite-concept)

(define not-more-concept
  (def-compound-concept :root not-concept :args (list more-concept)))
(define not-less-concept
  (def-compound-concept :root not-concept :args (list less-concept)))

(define more-cross_view-concept (def-concept :name "more-cross_view"))
(def-relation :start more-concept :end more-cross_view-concept
  :parent_concept outer-concept)
(define less-cross_view-concept (def-concept :name "less-cross_view"))
(def-relation :start less-concept :end less-cross_view-concept
  :parent_concept outer-concept)

(def-relation :start and :end then :parent_concept more-concept :conceptual_space grammar-space)
(def-relation :start but :end then :parent_concept more-concept :conceptual_space grammar-space)
